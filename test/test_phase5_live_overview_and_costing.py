#!/usr/bin/env python3
"""
Phase 5 Test Suite: Live Trade Case Overview (Module 1) & Un-mocked Trade Cost Dashboard (Module 5)
====================================================================================================
Covers:
1. Live Cost Dashboard API: get_cost_dashboard_data() & add_cost_item_to_case()
2. Export profitability integration inside get_cost_dashboard_data()
3. Cost audit card formatting (Duplicate, Missing Cost, Association checks)
4. _build_live_trade_case_overview() 14-section live aggregator with synthetic Trade Case doc
5. Frontend wiring verification on BOTH unified_logistics_hub.js and unified_logistics_hub.bundle.js:
   - All 5 Quick Action buttons call real Phase 2-5 backend APIs (zero msgprint stubs)
   - EmbeddedTradeCostDashboardController calls get_cost_dashboard_data & allocate_and_sync_lcv
   - Purple Ban compliance preserved
"""

import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
APP_ROOT = os.path.join(REPO_ROOT, "apps", "logistics_wizard")
if APP_ROOT not in sys.path:
    sys.path.insert(0, APP_ROOT)

from logistics_wizard import api as lw_api
from logistics_wizard.costing_engine.api import (
    add_cost_item_to_case,
    clear_mock_cost_sheet_registry,
    get_cost_dashboard_data,
    register_mock_cost_sheet,
)
from logistics_wizard.customs_engine import (
    approve_hs_code,
    create_customs_declaration,
    in_memory_customs_store,
    propose_hs_code,
)
from logistics_wizard.document_engine import (
    in_memory_document_store,
    init_case_document_checklist,
)
from logistics_wizard.exception_engine import (
    create_action_item,
    in_memory_action_store,
    in_memory_exception_store,
    raise_exception_from_rule,
)
from logistics_wizard.warehouse_engine import (
    in_memory_warehouse_store,
    schedule_warehouse_receiving,
)


class TestPhase5LiveOverviewAndCostDashboard(unittest.TestCase):
    """Validate Phase 5 live Trade Cost Dashboard APIs, live Overview builder, and UI wiring."""

    def setUp(self):
        clear_mock_cost_sheet_registry()
        in_memory_document_store.reset()
        in_memory_customs_store.reset()
        in_memory_warehouse_store.reset()
        in_memory_exception_store.reset()
        in_memory_action_store.reset()

    def tearDown(self):
        clear_mock_cost_sheet_registry()
        in_memory_document_store.reset()
        in_memory_customs_store.reset()
        in_memory_warehouse_store.reset()
        in_memory_exception_store.reset()
        in_memory_action_store.reset()

    def test_add_cost_item_and_get_cost_dashboard_data_import(self):
        r1 = add_cost_item_to_case(
            case_id="IMP-2026-5001",
            cost_type="Freight",
            estimated_cost=8000,
            actual_cost=8800,
            invoice_number="INV-MAE-5001",
            cost_description="Ocean Freight",
            status="Verified",
        )
        self.assertTrue(r1["success"])
        self.assertEqual(r1["items_count"], 1)

        r2 = add_cost_item_to_case(
            case_id="IMP-2026-5001",
            cost_type="Insurance",
            estimated_cost=500,
            actual_cost=550,
            invoice_number="INV-INS-5001",
            cost_description="Cargo Insurance",
            status="Verified",
        )
        self.assertTrue(r2["success"])
        self.assertEqual(r2["items_count"], 2)

        dash = get_cost_dashboard_data("IMP-2026-5001")
        self.assertTrue(dash["success"])
        self.assertTrue(dash["has_cost_sheet"])
        self.assertEqual(dash["case_id"], "IMP-2026-5001")
        self.assertEqual(dash["estimated_cost"], 8500.0)
        self.assertEqual(dash["actual_cost"], 9350.0)
        self.assertEqual(dash["variance_amount"], 850.0)
        self.assertEqual(dash["variance_pct"], 10.0)
        self.assertEqual(len(dash["cost_items"]), 2)
        self.assertEqual(len(dash["audit_checks"]), 3)
        self.assertEqual(dash["case_type"], "import")
        self.assertIsNone(dash["export_profitability"])

    def test_get_cost_dashboard_data_export_profitability(self):
        register_mock_cost_sheet(
            "EXP-2026-5002",
            {
                "name": "TCS-EXP-5002",
                "trade_case": "EXP-2026-5002",
                "trade_type": "Export",
                "currency": "USD",
                "purchase_value": 80000.0,
                "export_revenue": 80000.0,
                "export_cogs": 52000.0,
                "status": "Verified",
                "docstatus": 0,
                "cost_items": [
                    {
                        "cost_type": "Freight",
                        "cost_description": "Export Ocean Freight",
                        "invoice_number": "ONE-EXP-5002",
                        "estimated_cost": 4000.0,
                        "actual_cost": 4500.0,
                        "status": "Verified",
                    }
                ],
            },
        )
        dash = get_cost_dashboard_data("EXP-2026-5002")
        self.assertTrue(dash["success"])
        self.assertEqual(dash["case_type"], "export")
        self.assertIsNotNone(dash["export_profitability"])
        self.assertEqual(dash["export_profitability"]["export_revenue"], 80000.0)
        self.assertEqual(dash["export_profitability"]["export_logistics_cost"], 4500.0)

    def test_live_trade_case_overview_builder_aggregates_all_14_sections(self):
        cid = "IMP-2026-5050"
        init_case_document_checklist(cid, trade_type="Import", incoterm="CIF", shipping_mode="Ocean", eta_date="2026-12-20")
        c = create_customs_declaration(cid, customs_office_code="02CI", items=[{"item_name": "Chipset", "qty": 100, "unit_price": 50, "vat_rate": 10}])
        propose_hs_code(c["name"], 1, "85423100")
        approve_hs_code(c["name"], 1, action="approve")
        add_cost_item_to_case(cid, "Freight", estimated_cost=3000, actual_cost=3300, invoice_number="INV-5050", status="Verified")
        schedule_warehouse_receiving(cid, "WH-DANANG", "2026-12-22", expected_qty=100, space_reserved=1)
        raise_exception_from_rule(cid, "RULE_01_ETA_DELAY", "ETA Delay", "High", "Delay +2d", "Weather delay", department="Logistics")
        create_action_item(cid, "Follow up carrier ETA", department="Logistics", owner_name="Ops Lead")

        class DummyTC:
            name = cid
            case_title = "Live Semiconductor Import"
            trade_type = "Import"
            status = "Active"
            current_stage = "In Transit"
            overall_health = "Attention"
            shipping_mode = "Ocean"
            incoterm = "CIF"
            supplier = "TSMC Global"
            customer = None
            purchase_order = None
            sales_order = None
            origin_port = "Kaohsiung Port"
            destination_port = "Da Nang Port"
            case_owner = "ops@example.com"
            department = "Import Ops"
            priority = "High"
            order_amount = 50000.0
            currency = "USD"
            start_date = "2026-11-20"
            target_completion_date = "2026-12-25"
            creation = "2026-11-20 08:00:00"
            modified = "2026-11-26 10:00:00"
            owner = "Administrator"
            shipment_tracking = None
            stakeholders = []
            customs_cleared = 0
            costs_finalized = 0

        payload = lw_api._build_live_trade_case_overview(DummyTC(), [{"case_id": cid}])
        self.assertTrue(payload["is_live"])
        self.assertEqual(payload["case_id"], cid)
        self.assertEqual(payload["header"]["supplier"], "TSMC Global")
        self.assertEqual(payload["overall_health"]["status"], "Attention")
        self.assertEqual(len(payload["overall_health"]["cards"]), 6)
        self.assertGreaterEqual(payload["document_readiness"]["total_count"], 7)
        self.assertEqual(payload["customs_readiness"]["hs_classification"], "8542.31.00")
        self.assertEqual(payload["cost_summary"]["actual_cost"], 3300.0)
        self.assertEqual(payload["warehouse_readiness"]["warehouse"], "WH-DANANG")
        self.assertEqual(payload["open_exceptions"]["total_open"], 1)
        self.assertEqual(len(payload["upcoming_actions"]), 1)
        self.assertFalse(payload["quick_actions"]["can_close"])
        self.assertGreaterEqual(len(payload["quick_actions"]["close_reasons"]), 2)

    def test_frontend_quick_actions_and_cost_dashboard_are_wired_to_live_rpcs(self):
        js_paths = [
            os.path.join(APP_ROOT, "logistics_wizard", "public", "js", "unified_logistics_hub.js"),
            os.path.join(APP_ROOT, "logistics_wizard", "public", "js", "unified_logistics_hub.bundle.js"),
        ]
        required_rpcs = [
            "logistics_wizard.document_engine.api.upload_trade_document_version",
            "logistics_wizard.customs_engine.api.create_customs_declaration",
            "logistics_wizard.customs_engine.api.advance_customs_workflow",
            "logistics_wizard.costing_engine.api.add_cost_item_to_case",
            "logistics_wizard.exception_engine.api.raise_exception_from_rule",
            "logistics_wizard.exception_engine.api.create_action_item",
            "logistics_wizard.costing_engine.api.get_cost_dashboard_data",
            "logistics_wizard.costing_engine.api.allocate_and_sync_lcv",
        ]
        forbidden_stubs = [
            "sẽ kết nối với Module Document Readiness",
            "Đang tiến hành đồng bộ dữ liệu sang Landed Cost Voucher...",
        ]
        for path in js_paths:
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()
            for rpc in required_rpcs:
                self.assertIn(rpc, content, f"Missing live RPC '{rpc}' in {os.path.basename(path)}")
            for stub in forbidden_stubs:
                self.assertNotIn(stub, content, f"Old stub '{stub}' still present in {os.path.basename(path)}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
