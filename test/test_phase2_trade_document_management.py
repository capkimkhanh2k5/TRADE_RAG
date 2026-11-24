#!/usr/bin/env python3
"""
Phase 2 Test Suite: Module 3 — Trade Document Management
=========================================================
Covers:
1. Trade Document & Trade Document Version DocType JSON schema & permissions
2. TradeDocument controller validation (date ordering, auto-versioning v1->v2->v3,
   status transitions Required/Missing -> Received, re-upload downgrading Verified -> Received,
   auto-Expired past expiry_date, mandatory file check for Verified)
3. Checklist auto-generation & idempotency across Import/CIF/Air vs Export/FOB/Ocean
4. Exact Section 3.1 contract payload from docs/todoTradeCase.md
   (ready_count, total_count, percentage, current_stage, missing_urgent, 4 categories)
5. Verification workflow (verify, reject, mark_na, mark_missing) & expiry/overdue scheduler
6. Frappe hooks.py, api.py exports, and live document_readiness overlay in Trade Case Overview
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
from logistics_wizard.doctype.trade_document.trade_document import TradeDocument
from logistics_wizard.document_engine import (
    CANONICAL_CATEGORIES,
    compute_document_readiness_payload,
    evaluate_document_state,
    generate_case_document_checklist,
    get_case_documents_list,
    get_case_documents_status,
    in_memory_document_store,
    init_case_document_checklist,
    on_trade_case_after_insert,
    scheduled_check_expiring_documents,
    upload_trade_document_version,
    verify_trade_document,
)


class TestPhase2TradeDocumentSchema(unittest.TestCase):
    """Validate DocType JSON schemas and role permissions for Module 3."""

    def test_trade_document_doctype_schema_and_permissions(self):
        path = os.path.join(
            APP_ROOT, "logistics_wizard", "doctype", "trade_document", "trade_document.json"
        )
        with open(path, "r", encoding="utf-8") as fh:
            schema = json.load(fh)

        self.assertEqual(schema["name"], "Trade Document")
        self.assertEqual(schema["autoname"], "naming_series:")
        self.assertEqual(schema["module"], "Logistics Wizard")

        field_map = {f["fieldname"]: f for f in schema["fields"]}
        required_fields = [
            "naming_series",
            "trade_case",
            "trade_type",
            "shipment_tracking",
            "document_code",
            "document_name",
            "category",
            "is_mandatory",
            "required_before_stage",
            "status",
            "document_number",
            "issuer",
            "issue_date",
            "expiry_date",
            "deadline",
            "verified_by",
            "verified_at",
            "file_url",
            "current_version",
            "versions",
        ]
        for fname in required_fields:
            self.assertIn(fname, field_map, f"Missing field '{fname}' on Trade Document")

        self.assertEqual(field_map["versions"]["fieldtype"], "Table")
        self.assertEqual(field_map["versions"]["options"], "Trade Document Version")
        self.assertEqual(field_map["trade_case"]["options"], "Trade Case")

        roles = {p["role"] for p in schema["permissions"]}
        for expected_role in ("System Manager", "Purchase User", "Sales User", "Stock User"):
            self.assertIn(expected_role, roles)

    def test_trade_document_version_child_schema(self):
        path = os.path.join(
            APP_ROOT,
            "logistics_wizard",
            "doctype",
            "trade_document_version",
            "trade_document_version.json",
        )
        with open(path, "r", encoding="utf-8") as fh:
            schema = json.load(fh)

        self.assertEqual(schema["name"], "Trade Document Version")
        self.assertEqual(schema["istable"], 1)
        field_names = {f["fieldname"] for f in schema["fields"]}
        for fname in ("version_number", "file_url", "uploaded_by", "uploaded_at", "change_notes"):
            self.assertIn(fname, field_names)


class TestPhase2TradeDocumentController(unittest.TestCase):
    """Validate TradeDocument controller lifecycle and edge cases."""

    def test_version_history_increments_and_advances_status(self):
        doc = TradeDocument(
            {
                "trade_case": "IMP-2026-0001",
                "document_code": "DOC-INV",
                "document_name": "Commercial Invoice",
                "category": "Commercial",
                "is_mandatory": 1,
                "status": "Required",
                "file_url": "/files/inv_v1.pdf",
                "versions": [],
            }
        )
        doc._pending_change_notes = "Initial scan"
        doc._pending_uploaded_by = "buyer@example.com"
        doc.validate()

        self.assertEqual(doc.current_version, 1)
        self.assertEqual(doc.status, "Received")
        self.assertEqual(len(doc.versions), 1)
        self.assertEqual(doc.versions[0]["file_url"], "/files/inv_v1.pdf")
        self.assertEqual(doc.versions[0]["uploaded_by"], "buyer@example.com")

        # Re-validating same file should NOT create duplicate version
        doc.validate()
        self.assertEqual(doc.current_version, 1)
        self.assertEqual(len(doc.versions), 1)

        # Verify, then upload v2 -> should downgrade Verified -> Received & clear verified_by
        doc.status = "Verified"
        doc.verified_by = "qa@example.com"
        doc.validate()
        self.assertEqual(doc.status, "Verified")

        doc.file_url = "/files/inv_v2.pdf"
        doc._pending_change_notes = "Corrected unit price"
        doc.validate()
        self.assertEqual(doc.current_version, 2)
        self.assertEqual(len(doc.versions), 2)
        self.assertEqual(doc.status, "Received")
        self.assertIsNone(doc.verified_by)

        # Upload v3
        doc.file_url = "/files/inv_v3.pdf"
        doc.validate()
        self.assertEqual(doc.current_version, 3)
        self.assertEqual(len(doc.versions), 3)

    def test_expiry_date_before_issue_date_raises_error(self):
        doc = TradeDocument(
            {
                "trade_case": "IMP-2026-0002",
                "document_code": "DOC-CO",
                "document_name": "Certificate of Origin",
                "category": "Compliance",
                "status": "Received",
                "issue_date": "2026-10-15",
                "expiry_date": "2026-10-01",
            }
        )
        with self.assertRaises(Exception):
            doc.validate()

    def test_past_expiry_date_auto_marks_expired(self):
        doc = TradeDocument(
            {
                "trade_case": "IMP-2026-0003",
                "document_code": "DOC-CO",
                "document_name": "Certificate of Origin",
                "category": "Compliance",
                "status": "Verified",
                "file_url": "/files/co.pdf",
                "issue_date": "2026-01-01",
                "expiry_date": "2026-06-01",
                "_as_of_date": "2026-07-01",
            }
        )
        doc.validate()
        self.assertEqual(doc.status, "Expired")

    def test_mandatory_document_cannot_be_verified_without_file(self):
        doc = TradeDocument(
            {
                "trade_case": "IMP-2026-0004",
                "document_code": "DOC-BL",
                "document_name": "Bill of Lading",
                "category": "Transport",
                "is_mandatory": 1,
                "status": "Verified",
                "file_url": "",
            }
        )
        with self.assertRaises(Exception):
            doc.validate()


class TestPhase2ChecklistAndReadinessEngine(unittest.TestCase):
    """Validate checklist generation, Section 3.1 contract, verification, and scheduler."""

    def setUp(self):
        in_memory_document_store.reset()

    def tearDown(self):
        in_memory_document_store.reset()

    def test_import_cif_air_checklist_and_idempotency(self):
        first = init_case_document_checklist(
            case_id="IMP-2026-0101",
            trade_type="Import",
            incoterm="CIF",
            shipping_mode="Air",
            eta_date="2026-12-10",
        )
        self.assertTrue(first["success"])
        self.assertGreaterEqual(first["created_count"], 8)

        # Second call must be idempotent
        second = init_case_document_checklist(
            case_id="IMP-2026-0101",
            trade_type="Import",
            incoterm="CIF",
            shipping_mode="Air",
            eta_date="2026-12-10",
        )
        self.assertTrue(second["success"])
        self.assertEqual(second["created_count"], 0)
        self.assertEqual(second["existing_count"], first["created_count"])

        docs = {d["document_code"]: d for d in get_case_documents_list("IMP-2026-0101")}
        # Air Import CIF must include AWB, DO, and mandatory Insurance
        self.assertIn("DOC-AWB", docs)
        self.assertIn("DOC-DO", docs)
        self.assertIn("DOC-INS", docs)
        self.assertEqual(docs["DOC-INS"]["is_mandatory"], 1)
        self.assertEqual(docs["DOC-INS"]["status"], "Required")

    def test_export_fob_ocean_checklist_rules(self):
        res = generate_case_document_checklist(
            case_id="EXP-2026-0201",
            trade_type="Export",
            incoterm="FOB",
            shipping_mode="Ocean",
            eta_date="2026-12-20",
        )
        self.assertTrue(res["success"])
        docs = {d["document_code"]: d for d in get_case_documents_list("EXP-2026-0201")}
        self.assertIn("DOC-BL", docs)
        self.assertIn("DOC-BKG", docs)
        self.assertIn("DOC-CUS-EXP", docs)
        # Under FOB, marine insurance is optional (N/A)
        self.assertIn("DOC-INS", docs)
        self.assertEqual(docs["DOC-INS"]["is_mandatory"], 0)
        self.assertEqual(docs["DOC-INS"]["status"], "N/A")

    def test_section_3_1_readiness_contract_and_alerts(self):
        init_case_document_checklist(
            case_id="IMP-2026-0301",
            trade_type="Import",
            incoterm="FOB",
            shipping_mode="Ocean",
            eta_date="2026-12-10",
        )
        # Upload and verify 2 docs
        u_inv = upload_trade_document_version(
            "IMP-2026-0301", "DOC-INV", "/files/inv.pdf", document_number="INV-301"
        )
        v_inv = verify_trade_document(u_inv["name"], action="verify", user="ops@example.com")
        self.assertTrue(v_inv["success"])
        self.assertEqual(v_inv["status"], "Verified")

        u_pl = upload_trade_document_version(
            "IMP-2026-0301", "DOC-PL", "/files/pl.pdf", document_number="PL-301"
        )
        verify_trade_document(u_pl["name"], action="verify", user="ops@example.com")

        # Mark one doc expired by uploading with past expiry date
        upload_trade_document_version(
            "IMP-2026-0301",
            "DOC-CO",
            "/files/co_old.pdf",
            issue_date="2026-01-01",
            expiry_date="2026-11-01",
        )

        payload = get_case_documents_status("IMP-2026-0301", as_of_date="2026-12-09")

        # Exact Section 3.1 top-level keys
        for key in (
            "case_id",
            "ready_count",
            "total_count",
            "percentage",
            "current_stage",
            "missing_urgent",
            "categories",
        ):
            self.assertIn(key, payload)

        self.assertEqual(payload["ready_count"], 2)
        self.assertGreater(payload["total_count"], 2)
        self.assertEqual(
            payload["percentage"],
            round((payload["ready_count"] / payload["total_count"]) * 100.0, 1),
        )

        # Categories must strictly match 4 canonical buckets
        cat_names = tuple(c["name"] for c in payload["categories"])
        self.assertEqual(cat_names, CANONICAL_CATEGORIES)
        for cat in payload["categories"]:
            self.assertIn(cat["status"], ("completed", "warning", "danger"))
            self.assertIsInstance(cat["ready"], int)
            self.assertIsInstance(cat["total"], int)

        # Critical alerts must be sorted before warnings
        alerts = payload["missing_urgent"]
        self.assertGreaterEqual(len(alerts), 1)
        alert_types = [a["type"] for a in alerts]
        self.assertEqual(alert_types[0], "critical")
        if "warning" in alert_types:
            self.assertLess(alert_types.index("critical"), alert_types.index("warning"))

    def test_verification_actions_and_daily_expiry_scanner(self):
        init_case_document_checklist(
            case_id="IMP-2026-0401",
            trade_type="Import",
            incoterm="CIF",
            shipping_mode="Ocean",
            eta_date="2026-12-05",
        )
        u_inv = upload_trade_document_version("IMP-2026-0401", "DOC-INV", "/files/inv401.pdf")
        v_ok = verify_trade_document(u_inv["name"], action="verify", notes="Approved")
        self.assertEqual(v_ok["status"], "Verified")

        v_rej = verify_trade_document(u_inv["name"], action="reject", notes="Wrong HS code")
        self.assertEqual(v_rej["status"], "Required")
        self.assertIsNone(v_rej["verified_by"])

        docs = {d["document_code"]: d for d in get_case_documents_list("IMP-2026-0401")}
        v_na = verify_trade_document(docs["DOC-SC"]["name"], action="mark_na")
        self.assertEqual(v_na["status"], "N/A")

        v_miss = verify_trade_document(docs["DOC-BL"]["name"], action="mark_missing")
        self.assertEqual(v_miss["status"], "Missing")

        # Set an expiry_date in the past on DOC-PL (stored directly for scheduler scan)
        pl_doc = docs["DOC-PL"]
        pl_doc["status"] = "Verified"
        pl_doc["file_url"] = "/files/pl401.pdf"
        pl_doc["expiry_date"] = "2026-12-01"
        in_memory_document_store.save(pl_doc)

        scan = scheduled_check_expiring_documents(as_of_date="2026-12-15")
        self.assertTrue(scan["success"])
        self.assertIn(pl_doc["name"], scan["expired_documents"])
        self.assertGreaterEqual(scan["overdue_missing_count"], 1)
        self.assertIn("IMP-2026-0401", scan["affected_cases"])

    def test_after_insert_hook_and_overview_live_overlay(self):
        class DummyTradeCase:
            name = "IMP-2026-0501"
            trade_type = "Import"
            incoterm = "CIF"
            shipping_mode = "Ocean"
            target_completion_date = "2026-12-20"
            shipment_tracking = None

        on_trade_case_after_insert(DummyTradeCase())
        docs = get_case_documents_list("IMP-2026-0501")
        self.assertGreaterEqual(len(docs), 8)

        # Category filter check
        commercial_docs = get_case_documents_list("IMP-2026-0501", category="Commercial")
        self.assertGreaterEqual(len(commercial_docs), 2)
        self.assertTrue(all(d["category"] == "Commercial" for d in commercial_docs))

    def test_hooks_and_api_facade_registration(self):
        self.assertIn("Trade Case", lw_hooks.doc_events)
        self.assertEqual(
            lw_hooks.doc_events["Trade Case"]["after_insert"],
            "logistics_wizard.document_engine.api.on_trade_case_after_insert",
        )
        self.assertIn("daily", lw_hooks.scheduler_events)
        self.assertIn(
            "logistics_wizard.document_engine.api.scheduled_check_expiring_documents",
            lw_hooks.scheduler_events["daily"],
        )

        # Central api.py exports
        for fn_name in (
            "get_case_documents_status",
            "get_case_documents_list",
            "init_case_document_checklist",
            "upload_trade_document_version",
            "verify_trade_document",
            "scheduled_check_expiring_documents",
        ):
            self.assertTrue(callable(getattr(lw_api, fn_name, None)), f"api.{fn_name} missing")


if __name__ == "__main__":
    unittest.main(verbosity=2)
