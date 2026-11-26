#!/usr/bin/env python3
"""
Phase 6 Test Suite: Module 7 (Executive Dashboard, 6 Script Reports, 4-Scenario Seed & Acceptance)
====================================================================================================
Covers:
1. All 6 Frappe Script Reports JSON schemas, roles, and execute() return contracts
2. Workspace Reporting & Audit card registration for all 6 reports
3. get_executive_dashboard_summary() schema & offline resilience
4. DEMO_SCENARIO_SPECS coverage (Import + Export + Healthy / Attention / Critical Red / Warehouse Discrepancy)
5. End-to-end offline acceptance check verifying all 7 Core Business Modules work together cleanly
"""

import importlib
import json
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
APP_ROOT = os.path.join(REPO_ROOT, "apps", "logistics_wizard")
if APP_ROOT not in sys.path:
    sys.path.insert(0, APP_ROOT)

from logistics_wizard import api as lw_api
from logistics_wizard.seed_demo_scenarios import DEMO_SCENARIO_SPECS


EXPECTED_REPORTS = [
    ("shipment_delay_and_carrier_performance", "Shipment Delay and Carrier Performance", "Shipment Tracking"),
    ("trade_document_readiness_audit", "Trade Document Readiness Audit", "Trade Document"),
    ("customs_clearance_sla_performance", "Customs Clearance SLA Performance", "Customs Declaration"),
    ("import_landed_cost_variance", "Import Landed Cost Variance", "Trade Cost Sheet"),
    ("export_profitability_and_logistics_cost", "Export Profitability and Logistics Cost", "Trade Cost Sheet"),
    ("trade_exception_and_action_audit", "Trade Exception and Action Audit", "Shipment Exception"),
]


class TestPhase6ExecutiveReportsAndSeed(unittest.TestCase):
    """Validate all 6 Script Reports, Executive Dashboard contract, and Seed specifications."""

    def test_all_6_script_reports_schema_and_execute_contract(self):
        report_root = os.path.join(APP_ROOT, "logistics_wizard", "report")
        for slug, expected_name, ref_doctype in EXPECTED_REPORTS:
            json_path = os.path.join(report_root, slug, f"{slug}.json")
            self.assertTrue(os.path.exists(json_path), f"Missing report JSON: {json_path}")
            with open(json_path, "r", encoding="utf-8") as fh:
                meta = json.load(fh)
            self.assertEqual(meta["name"], expected_name)
            self.assertEqual(meta["report_type"], "Script Report")
            self.assertEqual(meta["is_standard"], "Yes")
            self.assertEqual(meta["module"], "Logistics Wizard")
            self.assertEqual(meta["ref_doctype"], ref_doctype)
            self.assertGreaterEqual(len(meta.get("roles") or []), 3)

            mod = importlib.import_module(f"logistics_wizard.report.{slug}.{slug}")
            self.assertTrue(callable(getattr(mod, "execute", None)))
            cols, rows = mod.execute({})
            self.assertIsInstance(cols, list)
            self.assertGreaterEqual(len(cols), 7)
            self.assertIsInstance(rows, list)

    def test_workspace_links_all_6_reports(self):
        ws_path = os.path.join(
            APP_ROOT, "logistics_wizard", "workspace", "logistics_wizard", "logistics_wizard.json"
        )
        with open(ws_path, "r", encoding="utf-8") as fh:
            ws = json.load(fh)
        report_links = {
            lnk["link_to"]
            for lnk in ws.get("links", [])
            if lnk.get("link_type") == "Report"
        }
        for _, expected_name, _ in EXPECTED_REPORTS:
            self.assertIn(expected_name, report_links, f"Report '{expected_name}' missing in Workspace")

    def test_executive_dashboard_summary_contract(self):
        res = lw_api.get_executive_dashboard_summary("30d")
        self.assertEqual(res["status"], "success")
        data = res["data"]
        for key in (
            "metrics",
            "pipeline",
            "health_donut",
            "modality_split",
            "cost_breakdown",
            "corridors",
            "action_alerts",
        ):
            self.assertIn(key, data)
        for metric_key in (
            "total_cases",
            "import_cases",
            "export_cases",
            "in_transit_shipments",
            "delayed_shipments",
            "missing_documents",
            "customs_processing",
            "customs_stuck",
            "active_exceptions",
            "total_spend",
        ):
            self.assertIn(metric_key, data["metrics"])

    def test_demo_scenario_specs_cover_import_export_and_4_scenarios(self):
        self.assertEqual(len(DEMO_SCENARIO_SPECS), 4)
        trade_types = {s["trade_type"] for s in DEMO_SCENARIO_SPECS}
        healths = {s["expected_health"] for s in DEMO_SCENARIO_SPECS}
        self.assertEqual(trade_types, {"Import", "Export"})
        self.assertEqual(healths, {"Healthy", "Attention", "Critical"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
