#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite: Phase 1 — Foundation, Naming Series (IMP/EXP), Master Config & Export Shipment
=========================================================================================
Verifies all Phase 1 deliverables standalone without requiring a live MariaDB instance:
1. Trade Case IMP/EXP naming series, legacy TC-* preservation, and Sales Order sync.
2. Trade Master Config: Incoterms 2020, document templates, mode validation, customs offices, thresholds.
3. Shipment Tracking Export flow_type auto-resolution, outbound route geometry, Hub filtering, and Delivery Note hook.
4. Scheduled background jobs: polling sync & idempotent stale tracking scan.
5. Frappe hooks registration for Delivery Note doc_events and scheduler_events.
"""

import json
import os
import sys
import time
import types
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
APP_PATH = os.path.join(PROJECT_ROOT, "apps", "logistics_wizard")
if APP_PATH not in sys.path:
    sys.path.insert(0, APP_PATH)


class _DummyDoc:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def get(self, key, default=None):
        return getattr(self, key, default)


class TestPhase1FoundationAndShipment(unittest.TestCase):
    def setUp(self):
        from logistics_wizard import api, master_config, tracking_service, hooks
        self.api = api
        self.master_config = master_config
        self.tracking_service = tracking_service
        self.hooks = hooks
        self.tracking_service.in_memory_db.reset()

    def tearDown(self):
        self.tracking_service.in_memory_db.reset()

    # --------------------------------------------------------------------------
    # 1. Trade Case Naming Series IMP/EXP & Sales Order Sync
    # --------------------------------------------------------------------------
    def test_trade_case_naming_series_import_export_and_legacy(self):
        from logistics_wizard.doctype.trade_case.trade_case import TradeCase

        # Arrange & Act: Import
        tc_imp = TradeCase({"trade_type": "Import"})
        tc_imp.validate()
        # Assert
        self.assertEqual(tc_imp.naming_series, "IMP-.YYYY.-.####")

        # Arrange & Act: Export via before_naming + validate
        tc_exp = TradeCase({"trade_type": "Export"})
        tc_exp.before_naming()
        tc_exp.validate()
        # Assert
        self.assertEqual(tc_exp.naming_series, "EXP-.YYYY.-.####")

        # Arrange & Act: Legacy TC-* record preservation
        tc_legacy = TradeCase({"name": "TC-2026-00001", "trade_type": "Import"})
        tc_legacy.validate()
        # Assert
        self.assertEqual(tc_legacy.name, "TC-2026-00001")
        self.assertEqual(tc_legacy.naming_series, "TC-.YYYY.-.")

    def test_trade_case_json_schema_naming_series_and_zero_duplication(self):
        json_path = os.path.join(
            APP_PATH, "logistics_wizard", "doctype", "trade_case", "trade_case.json"
        )
        with open(json_path, "r", encoding="utf-8") as f:
            schema = json.load(f)

        fields = {fld["fieldname"]: fld for fld in schema.get("fields", []) if "fieldname" in fld}
        self.assertEqual(fields["naming_series"]["default"], "IMP-.YYYY.-.####")
        self.assertEqual(
            fields["naming_series"]["options"],
            "IMP-.YYYY.-.####\nEXP-.YYYY.-.####\nTC-.YYYY.-.",
        )
        for forbidden in ("items", "checkpoints", "transit_waypoints", "gps_coordinates"):
            self.assertNotIn(forbidden, fields)

    def test_trade_case_sales_order_metadata_sync(self):
        from logistics_wizard.doctype.trade_case import trade_case as tc_mod
        from logistics_wizard.doctype.trade_case.trade_case import TradeCase

        mock_db = types.SimpleNamespace(
            get_value=lambda doctype, name, fieldnames, as_dict=False: {
                "customer": "California Solar Tech LLC",
                "currency": "USD",
                "grand_total": 150000.0,
                "company": "Cap Khanh Logistics",
            }
            if doctype == "Sales Order" and name == "SO-2026-0019"
            else None
        )
        mock_frappe = types.SimpleNamespace(db=mock_db)

        with patch.object(tc_mod, "frappe", mock_frappe):
            tc_exp = TradeCase({"trade_type": "Export", "sales_order": "SO-2026-0019"})
            tc_exp.validate()

        self.assertEqual(tc_exp.naming_series, "EXP-.YYYY.-.####")
        self.assertEqual(tc_exp.customer, "California Solar Tech LLC")
        self.assertEqual(tc_exp.currency, "USD")
        self.assertEqual(tc_exp.order_amount, 150000.0)
        self.assertEqual(tc_exp.company, "Cap Khanh Logistics")

    # --------------------------------------------------------------------------
    # 2. Trade Master Config
    # --------------------------------------------------------------------------
    def test_master_config_incoterms_2020(self):
        incoterms = self.master_config.INCOTERMS_2020
        expected_codes = {"EXW", "FCA", "FAS", "FOB", "CFR", "CIF", "CPT", "CIP", "DAP", "DPU", "DDP"}
        self.assertEqual(set(incoterms.keys()), expected_codes)
        self.assertTrue(incoterms["CIF"]["insurance_mandatory"])
        self.assertTrue(incoterms["CIP"]["insurance_mandatory"])
        self.assertFalse(incoterms["FOB"]["insurance_mandatory"])
        self.assertFalse(incoterms["EXW"]["insurance_mandatory"])
        self.assertEqual(incoterms["EXW"]["export_clearance_responsibility"], "Buyer")
        self.assertEqual(incoterms["DDP"]["import_clearance_responsibility"], "Seller")

    def test_master_config_document_templates_and_mode_validation(self):
        imp_air_cif = self.master_config.get_required_documents_template("Import", "CIF", "Air")
        imp_codes = {d["code"]: d for d in imp_air_cif}
        self.assertIn("DOC-AWB", imp_codes)
        self.assertIn("DOC-DO", imp_codes)
        self.assertIn("DOC-CUS-IMP", imp_codes)
        self.assertIn("DOC-INS", imp_codes)
        self.assertTrue(imp_codes["DOC-INS"]["is_mandatory"])
        self.assertNotIn("DOC-BL", imp_codes)

        exp_ocean_fob = self.master_config.get_required_documents_template("Export", "FOB", "Ocean")
        exp_codes = {d["code"]: d for d in exp_ocean_fob}
        self.assertIn("DOC-BL", exp_codes)
        self.assertIn("DOC-BKG", exp_codes)
        self.assertIn("DOC-CUS-EXP", exp_codes)
        self.assertIn("DOC-INS", exp_codes)
        self.assertFalse(exp_codes["DOC-INS"]["is_mandatory"])
        self.assertNotIn("DOC-DO", exp_codes)

        warn_res = self.master_config.validate_incoterm_for_mode("CIF", "Air")
        self.assertFalse(warn_res["valid"])
        self.assertIn("CIP", warn_res["warning"])

        ok_res = self.master_config.validate_incoterm_for_mode("CIF", "Ocean")
        self.assertTrue(ok_res["valid"])
        self.assertIsNone(ok_res["warning"])

    def test_master_config_customs_offices_and_thresholds(self):
        self.assertGreaterEqual(len(self.master_config.CUSTOMS_OFFICES_VN), 7)
        for office in self.master_config.CUSTOMS_OFFICES_VN:
            for key in ("code", "name", "port_code", "mode", "region"):
                self.assertIn(key, office)

        thresholds = self.master_config.get_trade_thresholds()
        for key in (
            "enable_auto_polling",
            "auto_create_exceptions",
            "polling_interval_minutes",
            "stale_threshold_hours",
            "cost_variance_warning_pct",
            "cost_variance_critical_pct",
            "demurrage_free_days",
            "doc_urgent_days_before_eta",
        ):
            self.assertIn(key, thresholds)

    # --------------------------------------------------------------------------
    # 3. Export Shipment Routing, Hub Filtering & Delivery Note Hook
    # --------------------------------------------------------------------------
    def test_shipment_tracking_export_validate_and_routing(self):
        from logistics_wizard.doctype.shipment_tracking.shipment_tracking import ShipmentTracking

        st = ShipmentTracking({"sales_order": "SO-2026-0019"})
        st.validate()
        self.assertEqual(st.flow_type, "Export")

        # Mock Frappe DB to test outbound Export route in get_shipment_tracking
        so_doc = _DummyDoc(
            name="SO-2026-0019",
            docstatus=1,
            status="To Deliver and Bill",
            customer="California Solar Tech LLC",
            set_warehouse="WH-DANANG",
            shipping_address_name="ADDR-USLAX",
            company="Cap Khanh Logistics",
        )
        st_doc = _DummyDoc(
            name="ST-EXP-2026-001",
            docstatus=1,
            flow_type="Export",
            sales_order="SO-2026-0019",
            customer="California Solar Tech LLC",
            shipping_method="Ocean",
            origin_port="Da Nang",
            destination_port="Los Angeles",
            status="In Transit",
            transit_route=[],
        )
        wh_doc = _DummyDoc(name="WH-DANANG", address="ADDR-DN", warehouse_name="Kho Đà Nẵng")
        addr_dn = _DummyDoc(city="Da Nang", country="Vietnam")
        addr_us = _DummyDoc(city="Los Angeles", country="United States")

        docs_map = {
            ("Shipment Tracking", "ST-EXP-2026-001"): st_doc,
            ("Sales Order", "SO-2026-0019"): so_doc,
            ("Warehouse", "WH-DANANG"): wh_doc,
            ("Address", "ADDR-DN"): addr_dn,
            ("Address", "ADDR-USLAX"): addr_us,
        }

        with patch.object(self.api.frappe.db, "exists", side_effect=lambda dt, nm=None: (dt, nm) in docs_map), \
             patch.object(self.api.frappe.db, "get_value", return_value="ST-EXP-2026-001"), \
             patch.object(self.api.frappe, "get_doc", side_effect=lambda dt, nm: docs_map[(dt, nm)]), \
             patch.object(self.api, "sync_transit_route_with_status", return_value=False):
            res = self.api.get_shipment_tracking(tracking_id="SO-2026-0019")

        self.assertEqual(res.get("status"), "success")
        self.assertEqual(res["data"]["doctype"], "Sales Order")
        self.assertEqual(res["data"]["flow_type"], "Export")
        self.assertIn("Vietnam", res["data"]["origin"]["query"])
        self.assertIn("United States", res["data"]["destination"]["query"])
        self.assertGreater(len(res["data"]["full_route"]), 2)

    def test_hub_data_flow_type_filter_and_export_search(self):
        self.tracking_service.in_memory_db.save_shipment("SHP-IMP-1", {
            "name": "SHP-IMP-1",
            "flow_type": "Import",
            "purchase_order": "PO-2026-001",
            "carrier": "Maersk Line",
            "shipping_method": "Ocean",
            "origin_port": "Shanghai",
            "destination_port": "Da Nang",
            "status": "In Transit",
            "is_delayed": 0,
            "is_stale": 0,
        })
        self.tracking_service.in_memory_db.save_shipment("SHP-EXP-1", {
            "name": "SHP-EXP-1",
            "flow_type": "Export",
            "sales_order": "SO-2026-0019",
            "delivery_note": "DN-2026-0035",
            "customer": "California Solar Tech LLC",
            "trade_case": "EXP-2026-0001",
            "carrier": "ONE",
            "shipping_method": "Ocean",
            "origin_port": "Da Nang",
            "destination_port": "Los Angeles",
            "status": "In Transit",
            "is_delayed": 0,
            "is_stale": 0,
        })

        exp_res = self.api.get_shipment_tracking_hub_data(flow_type="Export")
        exp_names = [s["name"] for s in exp_res["shipments"]]
        self.assertEqual(exp_names, ["SHP-EXP-1"])

        search_res = self.api.get_shipment_tracking_hub_data(search_term="California Solar")
        self.assertEqual([s["name"] for s in search_res["shipments"]], ["SHP-EXP-1"])

    def test_validate_delivery_note_shipment_status_hook(self):
        dn_doc = _DummyDoc(
            name="DN-2026-0035",
            items=[_DummyDoc(against_sales_order="SO-2026-0019")],
        )
        set_calls = []

        # Case 1: Booked / In Transit shipment -> Allowed & back-linked
        with patch.object(
            self.api.frappe.db,
            "get_value",
            return_value={"name": "ST-EXP-01", "status": "Booked", "origin_port": "Da Nang"},
        ), patch.object(
            self.api.frappe.db,
            "set_value",
            side_effect=lambda dt, nm, fld, val: set_calls.append((dt, nm, fld, val)),
        ):
            self.api.validate_delivery_note_shipment_status(dn_doc)

        self.assertEqual(set_calls, [("Shipment Tracking", "ST-EXP-01", "delivery_note", "DN-2026-0035")])

        # Case 2: Cancelled shipment -> Blocked via frappe.throw
        with patch.object(
            self.api.frappe.db,
            "get_value",
            return_value={"name": "ST-EXP-01", "status": "Cancelled", "origin_port": "Da Nang"},
        ):
            with self.assertRaises(self.api.frappe.ValidationError):
                self.api.validate_delivery_note_shipment_status(dn_doc)

    # --------------------------------------------------------------------------
    # 4. Scheduled Background Sync & Idempotent Stale Scan
    # --------------------------------------------------------------------------
    def test_scheduled_scan_stale_shipments_idempotent_and_sync_active(self):
        now = datetime(2026, 11, 24, 12, 0, 0)
        fresh_ts = (now - timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S")
        stale_ts = (now - timedelta(hours=72)).strftime("%Y-%m-%d %H:%M:%S")
        old_completed_ts = (now - timedelta(hours=120)).strftime("%Y-%m-%d %H:%M:%S")

        self.tracking_service.in_memory_db.save_shipment("SHP-FRESH", {
            "name": "SHP-FRESH",
            "status": "In Transit",
            "tracking_number": "TRK-FRESH",
            "carrier": "Maersk Line",
            "last_synced_at": fresh_ts,
            "is_stale": 0,
            "transit_route": [],
        })
        self.tracking_service.in_memory_db.save_shipment("SHP-STALE", {
            "name": "SHP-STALE",
            "status": "In Transit",
            "tracking_number": "TRK-STALE",
            "carrier": "ONE",
            "last_synced_at": stale_ts,
            "is_stale": 0,
            "transit_route": [],
        })
        self.tracking_service.in_memory_db.save_shipment("SHP-DONE", {
            "name": "SHP-DONE",
            "status": "Completed",
            "tracking_number": "TRK-DONE",
            "carrier": "MSC",
            "last_synced_at": old_completed_ts,
            "is_stale": 0,
            "transit_route": [],
        })

        # First scan: SHP-STALE flagged and raises 1 exception; SHP-DONE ignored
        scan_1 = self.tracking_service.scheduled_scan_stale_shipments(threshold_hours=48, current_time=now)
        self.assertTrue(scan_1["success"])
        self.assertEqual(scan_1["scanned_count"], 2)
        self.assertEqual(scan_1["stale_count"], 1)
        self.assertEqual(scan_1["stale_shipments"], ["SHP-STALE"])
        self.assertEqual(scan_1["exceptions_created"], 1)
        self.assertEqual(self.tracking_service.in_memory_db.get_shipment("SHP-STALE")["is_stale"], 1)
        self.assertEqual(self.tracking_service.in_memory_db.get_shipment("SHP-FRESH")["is_stale"], 0)
        self.assertEqual(self.tracking_service.in_memory_db.get_shipment("SHP-DONE")["is_stale"], 0)
        self.assertEqual(len(self.tracking_service.in_memory_db.exceptions), 1)
        exc = list(self.tracking_service.in_memory_db.exceptions.values())[0]
        self.assertEqual(exc["exception_type"], "Stale Tracking")

        # Second scan: Idempotent -> 0 new exceptions
        scan_2 = self.tracking_service.scheduled_scan_stale_shipments(threshold_hours=48, current_time=now)
        self.assertEqual(scan_2["stale_count"], 1)
        self.assertEqual(scan_2["exceptions_created"], 0)
        self.assertEqual(len(self.tracking_service.in_memory_db.exceptions), 1)

        # Scheduled sync active shipments -> syncs only the 2 non-terminal shipments
        sync_res = self.tracking_service.scheduled_sync_active_shipments(
            provider=self.tracking_service.MockTrackingProvider(scenario="departed")
        )
        self.assertTrue(sync_res["success"])
        self.assertFalse(sync_res["skipped"])
        self.assertEqual(sync_res["synced_count"], 2)
        self.assertEqual(sync_res["failed_count"], 0)

    # --------------------------------------------------------------------------
    # 5. Hooks Registration
    # --------------------------------------------------------------------------
    def test_hooks_doc_events_and_scheduler_events(self):
        self.assertIn("Delivery Note", self.hooks.doc_events)
        self.assertEqual(
            self.hooks.doc_events["Delivery Note"]["before_submit"],
            "logistics_wizard.api.validate_delivery_note_shipment_status",
        )
        self.assertTrue(hasattr(self.hooks, "scheduler_events"))
        self.assertIn(
            "logistics_wizard.tracking_service.scheduled_scan_stale_shipments",
            self.hooks.scheduler_events["hourly"],
        )
        self.assertIn(
            "logistics_wizard.tracking_service.scheduled_sync_active_shipments",
            self.hooks.scheduler_events["cron"]["0 */2 * * *"],
        )

    def test_no_mutual_recursion_on_corridor_labels(self):
        t0 = time.monotonic()
        res = self.api.get_location_coords("Hải phận Quốc tế Thái Bình Dương")
        elapsed = time.monotonic() - t0
        self.assertIsNone(res)
        self.assertLess(elapsed, 2.0)


if __name__ == "__main__":
    unittest.main()
