#!/usr/bin/env python3
"""
Phase 4 Test Suite: Warehouse Receiving & Inspection + Module 6 (Exceptions, Actions & Health)
===============================================================================================
Covers:
1. Trade Warehouse Receipt, Trade Action Item, and extended Shipment Exception schemas
2. Warehouse Receiving lifecycle: NOT READY -> SCHEDULED -> COMPLETED (clean) vs DISCREPANCY (Scenario 4)
3. Exact Section 3.4 contract payload from docs/todoTradeCase.md
4. All 8 automated Exception Rules from docsTitleProject/ToDo.md Section 4.6 + idempotency
5. Exception workflow: assign -> escalate (level 0->1->2 + severity upgrade) -> resolve + audit_log
6. Trade Action Item CRUD & live Trade Case Overview overlays
7. Deterministic Trade Case.overall_health computation (Healthy / Attention / Critical)
8. hooks.py registration (Purchase Receipt on_submit, hourly exception evaluator) & api.py exports
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
from logistics_wizard.doctype.shipment_exception.shipment_exception import ShipmentException
from logistics_wizard.doctype.trade_warehouse_receipt.trade_warehouse_receipt import (
    TradeWarehouseReceipt,
)
from logistics_wizard.exception_engine import (
    EXCEPTION_RULES_CATALOG,
    assign_exception,
    complete_action_item,
    compute_trade_case_health,
    create_action_item,
    escalate_exception,
    evaluate_8_exception_rules,
    evaluate_case_exceptions,
    get_case_action_items,
    get_case_exceptions_summary,
    in_memory_action_store,
    in_memory_exception_store,
    resolve_exception,
)
from logistics_wizard.warehouse_engine import (
    get_case_warehouse_status,
    in_memory_warehouse_store,
    record_warehouse_inspection,
    schedule_warehouse_receiving,
)


class TestPhase4SchemasAndControllers(unittest.TestCase):
    """Validate schemas & controller rules for Warehouse, Action Item, and Exception DocTypes."""

    def test_doctype_schemas_and_permissions(self):
        wh_path = os.path.join(
            APP_ROOT, "logistics_wizard", "doctype", "trade_warehouse_receipt", "trade_warehouse_receipt.json"
        )
        act_path = os.path.join(
            APP_ROOT, "logistics_wizard", "doctype", "trade_action_item", "trade_action_item.json"
        )
        exc_path = os.path.join(
            APP_ROOT, "logistics_wizard", "doctype", "shipment_exception", "shipment_exception.json"
        )
        with open(wh_path, "r", encoding="utf-8") as f:
            wh = json.load(f)
        with open(act_path, "r", encoding="utf-8") as f:
            act = json.load(f)
        with open(exc_path, "r", encoding="utf-8") as f:
            exc = json.load(f)

        self.assertEqual(wh["name"], "Trade Warehouse Receipt")
        self.assertEqual(act["name"], "Trade Action Item")
        self.assertEqual(exc["name"], "Shipment Exception")

        exc_fields = {f["fieldname"]: f for f in exc["fields"]}
        for fname in (
            "trade_case",
            "rule_code",
            "source_module",
            "assigned_to",
            "department",
            "due_date",
            "escalation_level",
            "escalated_to",
            "audit_log",
        ):
            self.assertIn(fname, exc_fields)
        # shipment_tracking must no longer be strictly reqd so non-shipment exceptions work
        self.assertFalse(exc_fields["shipment_tracking"].get("reqd", 0))
        for opt in ("Missing Document", "Customs Overdue", "Cost Variance", "Warehouse Discrepancy"):
            self.assertIn(opt, exc_fields["exception_type"]["options"])

    def test_shipment_exception_requires_case_or_shipment(self):
        bad = ShipmentException({"exception_type": "ETA Delay", "description": "Orphan"})
        with self.assertRaises(Exception):
            bad.validate()

    def test_warehouse_receipt_rejects_damaged_gt_received(self):
        wh = TradeWarehouseReceipt(
            {
                "trade_case": "IMP-2026-0001",
                "expected_qty": 100,
                "received_qty": 50,
                "damaged_qty": 60,
                "receiving_status": "INSPECTING",
            }
        )
        with self.assertRaises(Exception):
            wh.validate()


class TestPhase4WarehouseAndExceptionEngines(unittest.TestCase):
    """Validate Warehouse Section 3.4, Scenario 4, all 8 Exception Rules, and Auto Health."""

    def setUp(self):
        in_memory_warehouse_store.reset()
        in_memory_exception_store.reset()
        in_memory_action_store.reset()

    def tearDown(self):
        in_memory_warehouse_store.reset()
        in_memory_exception_store.reset()
        in_memory_action_store.reset()

    def test_warehouse_clean_receiving_and_section_3_4_contract(self):
        sch = schedule_warehouse_receiving(
            case_id="IMP-2026-0101",
            warehouse="Kho Ngoại quan - WH-DANANG",
            expected_arrival="2026-12-09",
            expected_qty=1000,
            space_reserved=1,
            receiving_team="Assigned (Đội Tiếp nhận Kho B)",
        )
        self.assertTrue(sch["success"])
        self.assertEqual(sch["receiving_status"], "SCHEDULED")

        pre = get_case_warehouse_status("IMP-2026-0101")
        for key in (
            "expected_arrival",
            "warehouse",
            "receiving_status",
            "expected_qty",
            "received_qty",
            "space_reserved",
            "receiving_team",
            "discrepancy_alert",
            "discrepancy_details",
        ):
            self.assertIn(key, pre)
        self.assertIsNone(pre["received_qty"])
        self.assertTrue(pre["space_reserved"])

        # Clean full delivery
        insp = record_warehouse_inspection(
            sch["name"],
            received_qty=1000,
            damaged_qty=0,
            container_seal_intact=1,
            actual_arrival="2026-12-09",
            purchase_receipt="MAT-PRE-2026-0001",
        )
        self.assertTrue(insp["success"])
        self.assertEqual(insp["receiving_status"], "COMPLETED")
        self.assertFalse(insp["discrepancy_alert"])
        self.assertEqual(insp["missing_qty"], 0.0)

        post = get_case_warehouse_status("IMP-2026-0101")
        self.assertEqual(post["receiving_status"], "COMPLETED")
        self.assertEqual(post["received_qty"], 1000.0)
        self.assertEqual(post["purchase_receipt"], "MAT-PRE-2026-0001")

    def test_scenario_4_warehouse_discrepancy_auto_raises_exception(self):
        # Exact Scenario 4 from docs/todoTradeCase.md: Expected 1000 / Received 985 / Damaged 10
        sch = schedule_warehouse_receiving(
            case_id="IMP-2026-0004",
            warehouse="WH-DANANG",
            expected_arrival="2026-12-09",
            expected_qty=1000,
            space_reserved=1,
        )
        insp = record_warehouse_inspection(
            sch["name"], received_qty=985, damaged_qty=10, actual_arrival="2026-12-09"
        )
        self.assertTrue(insp["success"])
        self.assertTrue(insp["discrepancy_alert"])
        self.assertEqual(insp["missing_qty"], 15.0)
        self.assertEqual(insp["damaged_qty"], 10.0)
        self.assertEqual(insp["receiving_status"], "DISCREPANCY")
        self.assertIn("DISCREPANCY DETECTED", insp["discrepancy_details"])

        # Must have auto-created an open Warehouse Discrepancy exception
        excs = get_case_exceptions_summary("IMP-2026-0004")
        self.assertEqual(excs["total_open"], 1)
        self.assertEqual(excs["items"][0]["exception_type"], "Warehouse Discrepancy")
        self.assertEqual(excs["items"][0]["severity"], "CRITICAL")

    def test_all_8_exception_rules_and_idempotency(self):
        self.assertEqual(len(EXCEPTION_RULES_CATALOG), 8)

        signals = {
            "current_stage": "Cost Finalization",
            "shipment": {
                "shipment_id": "SHP-2026-0045",
                "status": "Arrived Destination Port",
                "delay_days": 4,
                "is_stale": True,
                "stale_hours": 72,
                "days_at_port": 7,
            },
            "documents": {
                "missing_urgent": [
                    {
                        "code": "DOC-CO",
                        "name": "Certificate of Origin (C/O Form E)",
                        "type": "critical",
                        "deadline": "2026-11-20",
                        "note": "Quá hạn nộp C/O",
                    }
                ]
            },
            "customs": {
                "workflow_status": "Processing",
                "channel": "Red",
                "clearance_status": "NOT CLEARED",
                "processing_days": 5,
                "declaration_no": "106999888",
            },
            "cost": {
                "variance_pct": 16.2,
                "estimated_cost": 10000.0,
                "actual_cost": 11620.0,
                "invoices_total": 6,
                "cost_finalization_status": "IN PROGRESS",
            },
            "warehouse": {
                "discrepancy_alert": True,
                "damaged_qty": 3,
                "receiving_status": "DISCREPANCY",
                "discrepancy_details": "DISCREPANCY DETECTED (Expected: 500 / Received: 495 / Missing: 5 / Damaged: 3)",
            },
        }

        candidates = evaluate_8_exception_rules("IMP-2026-0800", signals, as_of_date="2026-11-26")
        rule_codes = {c["rule_code"] for c in candidates}
        self.assertEqual(len(candidates), 8)
        self.assertEqual(
            rule_codes,
            {
                "RULE_01_ETA_DELAY",
                "RULE_02_MISSING_DOCUMENT",
                "RULE_03_CUSTOMS_OVERDUE",
                "RULE_04_COST_VARIANCE",
                "RULE_05_STALE_TRACKING",
                "RULE_06_DEMURRAGE_RISK",
                "RULE_07_COST_NOT_FINALIZED",
                "RULE_08_WAREHOUSE_DISCREPANCY",
            },
        )

        # First evaluation creates 8 exceptions; second is idempotent (0 created, 8 updated)
        first = evaluate_case_exceptions("IMP-2026-0800", signals=signals, as_of_date="2026-11-26")
        self.assertEqual(first["created_count"], 8)
        self.assertEqual(first["health"]["status"], "Critical")

        second = evaluate_case_exceptions("IMP-2026-0800", signals=signals, as_of_date="2026-11-26")
        self.assertEqual(second["created_count"], 0)
        self.assertEqual(second["updated_count"], 8)

    def test_exception_assignment_escalation_resolution_and_action_items(self):
        ev = evaluate_case_exceptions(
            "IMP-2026-0900",
            signals={
                "shipment": {"delay_days": 2},
                "cost": {"variance_pct": 7.5, "estimated_cost": 10000, "actual_cost": 10750},
            },
            as_of_date="2026-11-26",
        )
        self.assertEqual(ev["created_count"], 2)
        self.assertEqual(ev["health"]["status"], "Attention")

        exc_id = ev["created_exceptions"][0]
        asgn = assign_exception(
            exc_id,
            assigned_to="ops@example.com",
            department="Logistics",
            due_date="2026-11-27",
            notes="Contact carrier rep",
        )
        self.assertTrue(asgn["success"])
        self.assertEqual(asgn["status"], "Investigating")

        esc1 = escalate_exception(exc_id, escalated_to="manager@example.com", reason="No carrier reply")
        self.assertTrue(esc1["success"])
        self.assertEqual(esc1["escalation_level"], 1)
        self.assertEqual(esc1["status"], "Escalated")

        res = resolve_exception(exc_id, resolution_notes="Vessel berthed, waiver issued", user="ops@example.com")
        self.assertTrue(res["success"])
        self.assertEqual(res["status"], "Resolved")

        stored = in_memory_exception_store.get(exc_id)
        self.assertIn("Assigned to ops@example.com", stored["audit_log"])
        self.assertIn("Escalated to Level 1", stored["audit_log"])
        self.assertIn("Marked Resolved", stored["audit_log"])

        # Trade Action Item flow
        act = create_action_item(
            case_id="IMP-2026-0900",
            action_title="Gửi công văn xin miễn lưu bãi Demurrage Waiver",
            department="Logistics",
            owner_name="Nguyen Van A",
            due_date="2026-11-28",
            priority="High",
            shipment_exception=exc_id,
        )
        self.assertTrue(act["success"])
        open_actions = get_case_action_items("IMP-2026-0900")
        self.assertEqual(len(open_actions), 1)

        comp = complete_action_item(act["name"], notes="Carrier approved 3 free days", user="ops@example.com")
        self.assertTrue(comp["success"])
        self.assertEqual(len(get_case_action_items("IMP-2026-0900")), 0)
        self.assertEqual(len(get_case_action_items("IMP-2026-0900", include_completed=True)), 1)

    def test_trade_case_health_transitions(self):
        # Healthy
        h_ok = compute_trade_case_health(
            signals={"shipment": {"delay_days": 0}, "cost": {"variance_pct": -1.3}, "customs": {"channel": "Green", "clearance_status": "CLEARED"}},
            open_exceptions=[],
        )
        self.assertEqual(h_ok["status"], "Healthy")

        # Attention (Scenario 2: +2 days delay, +7.9% cost)
        h_att = compute_trade_case_health(
            signals={"shipment": {"delay_days": 2}, "cost": {"variance_pct": 7.9}},
            open_exceptions=[],
        )
        self.assertEqual(h_att["status"], "Attention")

        # Critical (Scenario 3: Red channel)
        h_crit = compute_trade_case_health(
            signals={"customs": {"channel": "Red", "clearance_status": "NOT CLEARED"}},
            open_exceptions=[],
        )
        self.assertEqual(h_crit["status"], "Critical")

    def test_hooks_api_facade_and_live_overview_overlays(self):
        self.assertEqual(
            lw_hooks.doc_events["Purchase Receipt"]["on_submit"],
            "logistics_wizard.warehouse_engine.api.on_purchase_receipt_submit",
        )
        self.assertIn(
            "logistics_wizard.exception_engine.api.scheduled_evaluate_all_active_cases",
            lw_hooks.scheduler_events["hourly"],
        )
        for fn in (
            "get_case_warehouse_status",
            "schedule_warehouse_receiving",
            "record_warehouse_inspection",
            "evaluate_case_exceptions",
            "get_case_exceptions_summary",
            "assign_exception",
            "escalate_exception",
            "resolve_exception",
            "create_action_item",
            "complete_action_item",
            "get_case_action_items",
        ):
            self.assertTrue(callable(getattr(lw_api, fn, None)), f"api.{fn} missing")

        # Verify live overview overlays for warehouse, exceptions, and actions
        sch = schedule_warehouse_receiving("IMP-2026-0777", "WH-HAIPHONG", "2026-12-12", expected_qty=200)
        record_warehouse_inspection(sch["name"], received_qty=190, damaged_qty=2)
        create_action_item("IMP-2026-0777", "Lập biên bản giám định bảo hiểm", department="Warehouse", owner_name="Hoang Van E")

        ov = lw_api.get_trade_case_overview_data("IMP-2026-0777")
        self.assertTrue(ov["warehouse_readiness"]["discrepancy_alert"])
        self.assertEqual(ov["open_exceptions"]["total_open"], 1)
        self.assertEqual(len(ov["upcoming_actions"]), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
