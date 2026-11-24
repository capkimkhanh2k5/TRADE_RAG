#!/usr/bin/env python3
"""
Phase 3 Test Suite: Module 4 — Customs & Trade Compliance
==========================================================
Covers:
1. Customs Declaration & Customs Declaration Item DocType JSON schema & permissions
2. HS code validation/normalization and cascading Vietnam duty/tax math (Duty + TTDB + VAT)
3. CustomsDeclaration controller validation & human-in-the-loop HS approval gate
4. Standardized HS proposal + specialist approval/rejection workflow
5. Strict 6-state workflow state machine (Preparing -> Ready -> Declared -> Processing -> Cleared/Rejected)
6. Cross-module Document Readiness gate between document_engine and customs_engine
7. Exact Section 3.2 contract payload, Red Channel physical inspection, and overdue SLA scanner
8. hooks.py registration & api.py facade integration
"""

import json
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
APP_ROOT = os.path.join(REPO_ROOT, "apps", "logistics_wizard")
if APP_ROOT not in sys.path:
    sys.path.insert(0, APP_ROOT)

from logistics_wizard import api as lw_api
from logistics_wizard import hooks as lw_hooks
from logistics_wizard.customs_engine import (
    advance_customs_workflow,
    approve_hs_code,
    calculate_declaration_totals,
    calculate_item_taxes,
    can_transition,
    create_customs_declaration,
    get_case_customs_declarations,
    get_case_customs_status,
    in_memory_customs_store,
    is_valid_hs_code,
    normalize_hs_code,
    propose_hs_code,
    scheduled_check_overdue_customs,
)
from logistics_wizard.doctype.customs_declaration.customs_declaration import CustomsDeclaration
from logistics_wizard.document_engine import (
    in_memory_document_store,
    init_case_document_checklist,
)


class TestPhase3CustomsSchemaAndTaxCalc(unittest.TestCase):
    """Validate Module 4 DocType schemas and pure tax/HS calculation logic."""

    def test_customs_declaration_schema_and_permissions(self):
        parent_path = os.path.join(
            APP_ROOT,
            "logistics_wizard",
            "doctype",
            "customs_declaration",
            "customs_declaration.json",
        )
        child_path = os.path.join(
            APP_ROOT,
            "logistics_wizard",
            "doctype",
            "customs_declaration_item",
            "customs_declaration_item.json",
        )
        with open(parent_path, "r", encoding="utf-8") as fh:
            parent = json.load(fh)
        with open(child_path, "r", encoding="utf-8") as fh:
            child = json.load(fh)

        self.assertEqual(parent["name"], "Customs Declaration")
        self.assertEqual(parent["autoname"], "naming_series:")
        self.assertEqual(child["name"], "Customs Declaration Item")
        self.assertEqual(child["istable"], 1)

        p_fields = {f["fieldname"]: f for f in parent["fields"]}
        for fname in (
            "trade_case",
            "trade_type",
            "declaration_no",
            "customs_office_code",
            "workflow_status",
            "customs_lane",
            "clearance_status",
            "origin_verified",
            "customs_value_verified",
            "items",
            "total_customs_value",
            "total_duty_tax",
        ):
            self.assertIn(fname, p_fields)

        c_fields = {f["fieldname"] for f in child["fields"]}
        for fname in (
            "suggested_hs_code",
            "hs_confidence_score",
            "hs_legal_basis",
            "hs_source",
            "hs_approval_status",
            "approved_hs_code",
            "approved_by",
            "approved_at",
            "import_duty_rate",
            "special_consumption_tax_rate",
            "vat_rate",
            "total_tax_amount",
        ):
            self.assertIn(fname, c_fields)

        roles = {p["role"] for p in parent["permissions"]}
        for role in ("System Manager", "Purchase User", "Sales User", "Stock User"):
            self.assertIn(role, roles)

    def test_hs_code_validation_and_normalization(self):
        self.assertTrue(is_valid_hs_code("8517.62.99"))
        self.assertTrue(is_valid_hs_code("85176299"))
        self.assertTrue(is_valid_hs_code("8517"))
        self.assertFalse(is_valid_hs_code("85"))
        self.assertFalse(is_valid_hs_code("HS-8517"))
        self.assertEqual(normalize_hs_code("85176299"), "8517.62.99")
        self.assertEqual(normalize_hs_code("851762"), "8517.62")

    def test_cascading_vietnam_duty_sct_vat_calculation(self):
        # 10,000 USD, 20% import duty = 2,000 -> base 12,000, 30% SCT = 3,600 -> base 15,600, 10% VAT = 1,560
        taxes = calculate_item_taxes(
            customs_value=10000.0,
            import_duty_rate=20.0,
            special_consumption_tax_rate=30.0,
            vat_rate=10.0,
        )
        self.assertEqual(taxes["import_duty_amount"], 2000.0)
        self.assertEqual(taxes["special_consumption_tax_amount"], 3600.0)
        self.assertEqual(taxes["vat_amount"], 1560.0)
        self.assertEqual(taxes["total_tax_amount"], 7160.0)

        totals = calculate_declaration_totals(
            [
                {"qty": 10, "unit_price": 1000, "import_duty_rate": 20, "special_consumption_tax_rate": 30, "vat_rate": 10},
                {"qty": 5, "unit_price": 400, "import_duty_rate": 0, "special_consumption_tax_rate": 0, "vat_rate": 8},
            ]
        )
        self.assertEqual(totals["total_customs_value"], 12000.0)
        self.assertEqual(totals["total_duty_tax"], 7320.0)


class TestPhase3CustomsControllerAndWorkflow(unittest.TestCase):
    """Validate HS approval gate, 6-state workflow, Section 3.2 contract, and SLA scanner."""

    def setUp(self):
        in_memory_customs_store.reset()
        in_memory_document_store.reset()

    def tearDown(self):
        in_memory_customs_store.reset()
        in_memory_document_store.reset()

    def test_controller_office_lookup_and_hs_approval_gate(self):
        # Office code lookup + tax rollup
        cd = CustomsDeclaration(
            {
                "trade_case": "IMP-2026-0001",
                "customs_office_code": "02CI",
                "workflow_status": "Preparing",
                "items": [
                    {
                        "item_name": "Industrial Sensor",
                        "qty": 50,
                        "unit_price": 200,
                        "suggested_hs_code": "9026.80.10",
                        "hs_approval_status": "Proposed",
                        "import_duty_rate": 5,
                        "vat_rate": 10,
                    }
                ],
            }
        )
        cd.validate()
        self.assertIn("Cát Lái", cd.customs_office_name)
        self.assertEqual(cd.total_customs_value, 10000.0)
        self.assertEqual(cd.total_duty_tax, 1550.0)

        # Attempting to declare without specialist HS approval must raise error
        cd.workflow_status = "Declared"
        cd.declaration_no = "106000111222"
        with self.assertRaises(Exception):
            cd.validate()

    def test_hs_proposal_and_human_specialist_approval_flow(self):
        created = create_customs_declaration(
            case_id="IMP-2026-0101",
            trade_type="Import",
            customs_office_code="03CC",
            items=[
                {
                    "item_name": "Fiber Switch",
                    "qty": 20,
                    "unit_price": 500,
                    "import_duty_rate": 0,
                    "vat_rate": 10,
                }
            ],
        )
        self.assertTrue(created["success"])
        decl_name = created["name"]

        # 1. Propose HS (must remain Proposed, never auto-approved)
        prop = propose_hs_code(
            decl_name,
            item_idx=1,
            suggested_hs_code="85176221",
            confidence_score=96.2,
            legal_basis="GIR 1, Circular 31/2022/TT-BTC",
            source="AI/RAG Suggestion",
        )
        self.assertTrue(prop["success"])
        self.assertEqual(prop["suggested_hs_code"], "8517.62.21")
        self.assertEqual(prop["hs_approval_status"], "Proposed")

        # 2. Reject HS proposal
        rej = approve_hs_code(
            decl_name,
            item_idx=1,
            action="reject",
            notes="Cần kiểm tra lại tốc độ cổng quang",
            user="specialist@example.com",
        )
        self.assertTrue(rej["success"])
        self.assertEqual(rej["hs_approval_status"], "Rejected")
        self.assertIsNone(rej["approved_hs_code"])

        # 3. Approve HS with specialist override code
        appr = approve_hs_code(
            decl_name,
            item_idx=1,
            action="approve",
            approved_hs_code="85176299",
            notes="Đã đối chiếu catalogue kỹ thuật",
            user="specialist@example.com",
        )
        self.assertTrue(appr["success"])
        self.assertEqual(appr["hs_approval_status"], "Approved")
        self.assertEqual(appr["approved_hs_code"], "8517.62.99")
        self.assertEqual(appr["approved_by"], "specialist@example.com")

    def test_six_state_workflow_and_invalid_transitions(self):
        self.assertTrue(can_transition("Preparing", "Ready"))
        self.assertTrue(can_transition("Ready", "Declared"))
        self.assertTrue(can_transition("Declared", "Processing"))
        self.assertTrue(can_transition("Processing", "Cleared"))
        self.assertTrue(can_transition("Rejected", "Preparing"))
        self.assertFalse(can_transition("Preparing", "Cleared"))
        self.assertFalse(can_transition("Cleared", "Preparing"))

        created = create_customs_declaration(
            case_id="EXP-2026-0201",
            trade_type="Export",
            customs_office_code="02CI",
            items=[{"item_name": "Solar Panel 550W", "qty": 500, "unit_price": 120, "import_duty_rate": 0, "vat_rate": 0}],
        )
        name = created["name"]
        propose_hs_code(name, 1, "85414300", confidence_score=98.0, legal_basis="Biểu thuế XNK 2026")

        # Illegal direct jump Preparing -> Cleared
        bad_jump = advance_customs_workflow(name, "Cleared")
        self.assertFalse(bad_jump["success"])

        # Preparing -> Ready
        r1 = advance_customs_workflow(name, "Ready")
        self.assertTrue(r1["success"])

        # Ready -> Declared blocked until HS approved
        blocked = advance_customs_workflow(name, "Declared", declaration_no="306888999000", customs_lane="Red")
        self.assertFalse(blocked["success"])
        self.assertIn("Human Approval", blocked["error"])

        # Approve HS -> Declared -> Rejected -> Preparing -> Ready -> Declared -> Processing (Red) -> Cleared
        approve_hs_code(name, 1, action="approve", user="broker@example.com")
        r2 = advance_customs_workflow(
            name,
            "Declared",
            declaration_no="306888999000",
            customs_lane="Red",
            origin_verified=1,
            customs_value_verified=1,
            as_of_date="2026-11-10",
        )
        self.assertTrue(r2["success"])

        r_rej = advance_customs_workflow(name, "Rejected", rejection_reason="Thiếu bản dịch catalogue")
        self.assertTrue(r_rej["success"])
        self.assertEqual(r_rej["clearance_status"], "REJECTED")

        # Re-open Rejected -> Preparing -> Ready -> Declared -> Processing -> Cleared
        self.assertTrue(advance_customs_workflow(name, "Preparing")["success"])
        self.assertTrue(advance_customs_workflow(name, "Ready")["success"])
        self.assertTrue(
            advance_customs_workflow(
                name, "Declared", declaration_no="306888999000", customs_lane="Red", as_of_date="2026-11-10"
            )["success"]
        )
        self.assertTrue(advance_customs_workflow(name, "Processing", as_of_date="2026-11-15")["success"])

        # Red channel physical inspection + overdue SLA detection
        red_status = get_case_customs_status("EXP-2026-0201", as_of_date="2026-11-15")
        self.assertEqual(red_status["status"], "PHYSICAL INSPECTION (RED CHANNEL)")
        self.assertEqual(red_status["channel"], "Red")
        self.assertEqual(red_status["inspection"], "Physical Inspection")
        self.assertTrue(red_status["is_overdue"])
        self.assertEqual(red_status["processing_days"], 5)

        scan = scheduled_check_overdue_customs(as_of_date="2026-11-15")
        self.assertEqual(scan["overdue_count"], 1)
        self.assertEqual(scan["overdue_declarations"][0]["trade_case"], "EXP-2026-0201")

        # Final clearance
        cleared = advance_customs_workflow(name, "Cleared", as_of_date="2026-11-16")
        self.assertTrue(cleared["success"])
        self.assertEqual(cleared["clearance_status"], "CLEARED")

        final_status = get_case_customs_status("EXP-2026-0201", as_of_date="2026-11-16")
        self.assertEqual(final_status["readiness_pct"], 100)
        self.assertEqual(final_status["clearance_status"], "CLEARED")
        self.assertFalse(final_status["is_overdue"])

        # Verify all exact Section 3.2 keys
        for key in (
            "status",
            "readiness_pct",
            "hs_classification",
            "hs_approval_status",
            "origin_verified",
            "customs_value_verified",
            "declaration_status",
            "declaration_no",
            "channel",
            "license",
            "inspection",
            "clearance_status",
        ):
            self.assertIn(key, final_status)

    def test_cross_module_document_gate_blocks_ready_when_critical_docs_missing(self):
        # Create overdue critical documents for IMP-2026-0301
        init_case_document_checklist(
            case_id="IMP-2026-0301",
            trade_type="Import",
            incoterm="CIF",
            shipping_mode="Ocean",
            eta_date="2020-01-10",  # Far in the past -> critical overdue docs
        )
        created = create_customs_declaration(
            case_id="IMP-2026-0301",
            items=[{"item_name": "Valve", "qty": 10, "unit_price": 100, "import_duty_rate": 5, "vat_rate": 10}],
        )
        blocked = advance_customs_workflow(created["name"], "Ready")
        self.assertFalse(blocked["success"])
        self.assertIn("missing_critical_docs", blocked)

        # Explicit override allows proceeding when authorized
        overridden = advance_customs_workflow(created["name"], "Ready", force_skip_doc_check=True)
        self.assertTrue(overridden["success"])

    def test_hooks_and_api_facade_integration(self):
        self.assertIn(
            "logistics_wizard.customs_engine.api.scheduled_check_overdue_customs",
            lw_hooks.scheduler_events["daily"],
        )
        for fn_name in (
            "get_case_customs_status",
            "get_case_customs_declarations",
            "create_customs_declaration",
            "propose_hs_code",
            "approve_hs_code",
            "advance_customs_workflow",
            "scheduled_check_overdue_customs",
        ):
            self.assertTrue(callable(getattr(lw_api, fn_name, None)), f"api.{fn_name} missing")

        # Live overview overlay check
        created = create_customs_declaration(
            case_id="IMP-2026-0999",
            items=[{"item_name": "Module", "qty": 5, "unit_price": 200, "import_duty_rate": 0, "vat_rate": 10}],
        )
        propose_hs_code(created["name"], 1, "85176299")
        approve_hs_code(created["name"], 1, action="approve")
        ov = lw_api.get_trade_case_overview_data("IMP-2026-0999")
        self.assertEqual(ov["customs_readiness"]["hs_classification"], "8517.62.99")
        self.assertEqual(ov["customs_readiness"]["hs_approval_status"], "Approved by Customs Specialist")
        self.assertEqual(len(get_case_customs_declarations("IMP-2026-0999")), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
