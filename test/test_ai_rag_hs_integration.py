"""
Unit & Governance Acceptance Tests for AI/RAG -> Module 4 HS Code Integration
=============================================================================
Verifies:
1. Bilingual Vietnamese/English query normalization & HS hint extraction.
2. Graph-based hierarchy enrichment (Heading 4 -> Subheading 6 -> HS 8) + legal notes.
3. Strict Human-in-the-Loop Governance:
   - `suggest_hs_code_with_rag` ALWAYS sets `hs_approval_status = 'Proposed'`.
   - `automatic_hs_decision` is ALWAYS False and `requires_human_approval` is ALWAYS True.
   - Transition to `Declared` remains BLOCKED after AI/RAG suggestion until a human
     Customs Specialist explicitly runs `approve_hs_code`.
4. Full E2E flow: Create Declaration -> AI/RAG Suggest -> Blocked Declared ->
   Specialist Approve -> Advance to Ready -> Declared succeeds.
5. UI wiring & Purple Ban verification across `customs_declaration.js`, `hooks.py`,
   `unified_logistics_hub.js`, and `unified_logistics_hub.bundle.js`.
"""

import os
import re
import sys
import unittest

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apps", "logistics_wizard"))
if APP_ROOT not in sys.path:
    sys.path.insert(0, APP_ROOT)

from logistics_wizard.customs_engine.ai_hs_advisor import (
    extract_query_terms,
    recommend_hs_codes,
    strip_accents,
)
from logistics_wizard.customs_engine.api import (
    advance_customs_workflow,
    approve_hs_code,
    create_customs_declaration,
    in_memory_customs_store,
    suggest_hs_code_with_rag,
)


MOCK_TARIFF_NODES = [
    {
        "id": "tt31:SXVI-T-8413",
        "type": "heading",
        "code": "8413",
        "level": 4,
        "chapter": "84",
        "section": "XVI",
        "description": "Bơm chất lỏng, có hoặc không lắp dụng cụ đo; máy nâng chất lỏng",
    },
    {
        "id": "tt31:SXVI-T-841370",
        "type": "subheading",
        "code": "841370",
        "level": 6,
        "chapter": "84",
        "section": "XVI",
        "description": "Bơm ly tâm khác",
    },
    {
        "id": "tt31:SXVI-T-84137042",
        "type": "subheading",
        "code": "84137042",
        "level": 8,
        "chapter": "84",
        "section": "XVI",
        "description": "Với đường kính cửa hút không quá 200 mm, hoạt động bằng điện",
    },
    {
        "id": "tt31:SXVI-T-84137049",
        "type": "subheading",
        "code": "84137049",
        "level": 8,
        "chapter": "84",
        "section": "XVI",
        "description": "Loại khác",
    },
    {
        "id": "tt31:SXVI-T-8471",
        "type": "heading",
        "code": "8471",
        "level": 4,
        "chapter": "84",
        "section": "XVI",
        "description": "Máy xử lý dữ liệu tự động và các khối chức năng của chúng",
    },
    {
        "id": "tt31:SXVI-T-847130",
        "type": "subheading",
        "code": "847130",
        "level": 6,
        "chapter": "84",
        "section": "XVI",
        "description": "Máy xử lý dữ liệu tự động loại xách tay, khối lượng không quá 10 kg",
    },
    {
        "id": "tt31:SXVI-T-84713020",
        "type": "subheading",
        "code": "84713020",
        "level": 8,
        "chapter": "84",
        "section": "XVI",
        "description": "Máy tính xách tay kể cả notebook và subnotebook",
    },
    {
        "id": "tt31:SXVI-T-8541",
        "type": "heading",
        "code": "8541",
        "level": 4,
        "chapter": "85",
        "section": "XVI",
        "description": "Điốt, tranzito và các thiết bị bán dẫn tương tự; thiết bị bán dẫn cảm quang kể cả tế bào quang điện",
    },
    {
        "id": "tt31:SXVI-T-85414300",
        "type": "subheading",
        "code": "85414300",
        "level": 8,
        "chapter": "85",
        "section": "XVI",
        "description": "Tế bào quang điện đã được lắp ráp thành mô-đun hoặc thành tấm (pin mặt trời)",
    },
    {
        "id": "tt31:SXVI-N-CH84_NOTE_5",
        "type": "note",
        "chunk_type": "chapter_note",
        "chapter": "84",
        "section": "XVI",
        "description": "Chú giải 6 Chương 84: Định nghĩa máy xử lý dữ liệu tự động thuộc nhóm 84.71.",
    },
    {
        "id": "tt31:SXVI-N-SXVI_NOTE_2",
        "type": "note",
        "chunk_type": "section_note",
        "chapter": "84",
        "section": "XVI",
        "description": "Chú giải 2 Phần XVI: Nguyên tắc phân loại bộ phận của máy thuộc Chương 84 và 85.",
    },
]

MOCK_TARIFF_EDGES = [
    {"source": "tt31:SXVI-T-8413", "target": "tt31:SXVI-T-841370", "relation": "CONTAINS"},
    {"source": "tt31:SXVI-T-841370", "target": "tt31:SXVI-T-84137042", "relation": "CONTAINS"},
    {"source": "tt31:SXVI-T-841370", "target": "tt31:SXVI-T-84137049", "relation": "CONTAINS"},
    {"source": "tt31:SXVI-T-8471", "target": "tt31:SXVI-T-847130", "relation": "CONTAINS"},
    {"source": "tt31:SXVI-T-847130", "target": "tt31:SXVI-T-84713020", "relation": "CONTAINS"},
    {"source": "tt31:SXVI-T-8541", "target": "tt31:SXVI-T-85414300", "relation": "CONTAINS"},
    {"source": "tt31:SXVI-T-8471", "target": "tt31:SXVI-N-CH84_NOTE_5", "relation": "CONSTRAINED_BY"},
    {"source": "tt31:SXVI-T-8413", "target": "tt31:SXVI-N-SXVI_NOTE_2", "relation": "CONSTRAINED_BY"},
]


class TestAiRagHsIntegration(unittest.TestCase):
    def setUp(self):
        in_memory_customs_store.reset()

    def test_strip_accents_and_bilingual_query_expansion(self):
        self.assertEqual(strip_accents("Máy bơm nước điện"), "may bom nuoc dien")
        q = extract_query_terms("Industrial Centrifugal Electric Water Pump")
        self.assertIn("8413", q["hs_hints"])
        self.assertIn("ly", q["expanded_tokens"])
        self.assertIn("bom", q["expanded_tokens"])

    def test_recommend_hs_from_hierarchy_and_legal_notes_vietnamese(self):
        res = recommend_hs_codes(
            item_description="Bơm ly tâm nước hoạt động bằng điện, đường kính cửa hút 150 mm",
            corpus_nodes=MOCK_TARIFF_NODES,
            corpus_edges=MOCK_TARIFF_EDGES,
        )
        self.assertTrue(res["success"])
        self.assertTrue(res["requires_human_approval"])
        self.assertFalse(res["automatic_hs_decision"])
        self.assertEqual(res["primary_recommendation"]["hs_code"], "8413.70.42")
        self.assertIn("8413", res["primary_recommendation"]["full_hierarchy_path"])
        self.assertIn("Chú giải 2 Phần XVI", res["primary_recommendation"]["legal_basis"])

    def test_recommend_hs_from_english_commercial_invoice(self):
        res = recommend_hs_codes(
            item_description="Solar Photovoltaic Panel Module 550W",
            corpus_nodes=MOCK_TARIFF_NODES,
            corpus_edges=MOCK_TARIFF_EDGES,
        )
        self.assertTrue(res["success"])
        self.assertEqual(res["primary_recommendation"]["hs_code"], "8541.43.00")

        res_laptop = recommend_hs_codes(
            item_description="Business Laptop Notebook 14 inch",
            corpus_nodes=MOCK_TARIFF_NODES,
            corpus_edges=MOCK_TARIFF_EDGES,
        )
        self.assertTrue(res_laptop["success"])
        self.assertEqual(res_laptop["primary_recommendation"]["hs_code"], "8471.30.20")
        self.assertIn("Chú giải 6 Chương 84", res_laptop["primary_recommendation"]["legal_basis"])

    def test_empty_description_returns_validation_error(self):
        res = recommend_hs_codes(
            item_description="   ",
            corpus_nodes=MOCK_TARIFF_NODES,
            corpus_edges=MOCK_TARIFF_EDGES,
        )
        self.assertFalse(res["success"])
        self.assertTrue(res["requires_human_approval"])
        self.assertFalse(res["automatic_hs_decision"])

    def test_strict_human_in_the_loop_governance_e2e(self):
        # 1. Create declaration with unapproved item
        created = create_customs_declaration(
            case_id="IMP-2026-9901",
            trade_type="Import",
            customs_office_code="02CI",
            items=[
                {
                    "item_name": "Máy tính xách tay Notebook Pro 14",
                    "description": "Khối lượng 1.4 kg, CPU ARM",
                    "qty": 50,
                    "unit_price": 900,
                    "vat_rate": 10,
                }
            ],
        )
        self.assertTrue(created["success"])
        decl_name = created["name"]

        # 2. Run AI/RAG HS recommendation -> auto-propose into declaration item #1
        rag_res = suggest_hs_code_with_rag(
            declaration_name=decl_name,
            item_idx=1,
            auto_propose=True,
            use_llm=False,
            prefer_postgres=False,
            corpus_nodes=MOCK_TARIFF_NODES,
            corpus_edges=MOCK_TARIFF_EDGES,
        )
        self.assertTrue(rag_res["success"])
        self.assertTrue(rag_res["proposal_applied"])
        self.assertTrue(rag_res["requires_human_approval"])
        self.assertFalse(rag_res["automatic_hs_decision"])
        self.assertEqual(rag_res["proposal_result"]["suggested_hs_code"], "8471.30.20")
        self.assertEqual(rag_res["proposal_result"]["hs_source"], "AI/RAG Suggestion")
        # STRICT CHECK: AI/RAG MUST NEVER APPROVE!
        self.assertEqual(rag_res["proposal_result"]["hs_approval_status"], "Proposed")

        stored = in_memory_customs_store.get(decl_name)
        self.assertIsNone(stored["items"][0].get("approved_hs_code"))
        self.assertIsNone(stored["items"][0].get("approved_by"))

        # 3. Advance Preparing -> Ready succeeds, but Ready -> Declared MUST BE BLOCKED!
        r_ready = advance_customs_workflow(decl_name, "Ready", force_skip_doc_check=True)
        self.assertTrue(r_ready["success"])

        r_decl_blocked = advance_customs_workflow(
            decl_name,
            "Declared",
            declaration_no="106999888777",
            customs_lane="Green",
            force_skip_doc_check=True,
        )
        self.assertFalse(r_decl_blocked["success"])
        self.assertIn("HS", r_decl_blocked["error"])

        # 4. Customs Specialist explicitly approves the proposed HS code
        approved = approve_hs_code(
            declaration_name=decl_name,
            item_idx=1,
            action="approve",
            notes="Đã đối chiếu catalogue và Chú giải 6 Chương 84 TT31.",
            user="customs.specialist@company.vn",
        )
        self.assertTrue(approved["success"])
        self.assertEqual(approved["hs_approval_status"], "Approved")
        self.assertEqual(approved["approved_hs_code"], "8471.30.20")
        self.assertEqual(approved["approved_by"], "customs.specialist@company.vn")

        # 5. Now Ready -> Declared succeeds cleanly!
        r_decl_ok = advance_customs_workflow(
            decl_name,
            "Declared",
            declaration_no="106999888777",
            customs_lane="Green",
            force_skip_doc_check=True,
        )
        self.assertTrue(r_decl_ok["success"])
        self.assertEqual(r_decl_ok["workflow_status"], "Declared")

    def test_ui_wiring_and_purple_ban(self):
        cd_js_path = os.path.join(
            APP_ROOT, "logistics_wizard", "doctype", "customs_declaration", "customs_declaration.js"
        )
        hooks_path = os.path.join(APP_ROOT, "logistics_wizard", "hooks.py")
        hub_js_path = os.path.join(APP_ROOT, "logistics_wizard", "public", "js", "unified_logistics_hub.js")
        hub_bundle_path = os.path.join(
            APP_ROOT, "logistics_wizard", "public", "js", "unified_logistics_hub.bundle.js"
        )

        with open(cd_js_path, encoding="utf-8") as f:
            cd_js = f.read()
        with open(hooks_path, encoding="utf-8") as f:
            hooks_py = f.read()
        with open(hub_js_path, encoding="utf-8") as f:
            hub_js = f.read()
        with open(hub_bundle_path, encoding="utf-8") as f:
            hub_bundle = f.read()

        self.assertIn("suggest_hs_code_with_rag", cd_js)
        self.assertIn("approve_hs_code", cd_js)
        self.assertIn("Gợi ý mã HS (AI/RAG)", cd_js)
        self.assertIn("Phê duyệt / Từ chối HS (Chuyên viên)", cd_js)
        self.assertIn('"Customs Declaration": "doctype/customs_declaration/customs_declaration.js"', hooks_py)

        # Dual-file Hub sync check
        self.assertIn("suggest_hs_code_with_rag", hub_js)
        self.assertIn("suggest_hs_code_with_rag", hub_bundle)
        self.assertIn("approve_hs_code", hub_js)
        self.assertIn("approve_hs_code", hub_bundle)

        # Purple Ban enforcement on new Customs JS
        purple_pattern = re.compile(r"(purple|violet|indigo|magenta|#6366f1|#8b5cf6|#7c3aed|#a855f7)", re.IGNORECASE)
        self.assertIsNone(purple_pattern.search(cd_js), "Purple Ban violated in customs_declaration.js")


if __name__ == "__main__":
    unittest.main()
