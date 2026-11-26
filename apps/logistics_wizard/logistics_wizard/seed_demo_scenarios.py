# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""
seed_demo_scenarios.py — Idempotent End-to-End Demo Seed Data (Module 7 / Phase 6)
===================================================================================
Seeds the 4 canonical real-world Import & Export scenarios from docs/todoTradeCase.md
into MariaDB across ALL 7 Core Business Modules:
  1. Scenario 1 (Healthy — Import Air CIF): Tokyo -> Noi Bai, 100% Docs, Green Customs Cleared,
     Warehouse Completed, Cost Variance -1.3%, 0 Exceptions -> overall_health = Healthy.
  2. Scenario 2 (Attention — Import Ocean FOB): Shanghai -> Da Nang, +2d Delay, Missing C/O,
     Customs Preparing (HS Approved), Cost Variance +7.9%, Open Exceptions -> overall_health = Attention.
  3. Scenario 3 (Critical — Export Ocean CIF): Da Nang -> Los Angeles, Solar Panels, Red Channel
     Physical Inspection (5d Overdue), Export Cost Variance +15.0% -> overall_health = Critical.
  4. Scenario 4 (Critical — Warehouse Discrepancy): Busan -> Hai Phong, Expected 1000 / Received 985 /
     Damaged 10 -> Auto-triggered Warehouse Discrepancy Critical Exception -> overall_health = Critical.

Usage via bench:
    bench --site logistics.local execute logistics_wizard.seed_demo_scenarios.seed_all_demo_scenarios
"""

from datetime import date, timedelta
from typing import Any, Dict, List

try:
    import frappe
except ImportError:
    frappe = None

from logistics_wizard.document_engine.api import (
    get_case_documents_list,
    upload_trade_document_version,
    verify_trade_document,
)
from logistics_wizard.customs_engine.api import (
    advance_customs_workflow,
    approve_hs_code,
    create_customs_declaration,
    get_case_customs_declarations,
    propose_hs_code,
)
from logistics_wizard.costing_engine.api import add_cost_item_to_case
from logistics_wizard.warehouse_engine.api import (
    record_warehouse_inspection,
    schedule_warehouse_receiving,
)
from logistics_wizard.exception_engine.api import (
    create_action_item,
    evaluate_case_exceptions,
    get_case_action_items,
)

DEMO_SCENARIO_SPECS: List[Dict[str, Any]] = [
    {
        "key": "SCENARIO_1_HEALTHY_IMPORT_AIR",
        "case_title": "[DEMO-S1] Import Air CIF — Tokyo Optical Measuring Instruments",
        "trade_type": "Import",
        "shipping_mode": "Air",
        "incoterm": "CIF",
        "current_stage": "Cost Finalization",
        "status": "Cost Finalization",
        "origin_port": "Tokyo Narita (NRT)",
        "destination_port": "Hanoi Noi Bai (HAN)",
        "order_amount": 45000.0,
        "expected_health": "Healthy",
    },
    {
        "key": "SCENARIO_2_ATTENTION_DELAY_MISSING_CO",
        "case_title": "[DEMO-S2] Import Ocean FOB — Shanghai 5G Network Routers",
        "trade_type": "Import",
        "shipping_mode": "Ocean",
        "incoterm": "FOB",
        "current_stage": "In Transit",
        "status": "In Transit",
        "origin_port": "Shanghai Port (CNSHA)",
        "destination_port": "Da Nang Tien Sa (VNDAD)",
        "order_amount": 100000.0,
        "expected_health": "Attention",
    },
    {
        "key": "SCENARIO_3_CRITICAL_EXPORT_RED_CHANNEL",
        "case_title": "[DEMO-S3] Export Ocean CIF — Da Nang Solar Panels to Los Angeles",
        "trade_type": "Export",
        "shipping_mode": "Ocean",
        "incoterm": "CIF",
        "current_stage": "Export Port",
        "status": "Customs Clearance",
        "origin_port": "Da Nang Tien Sa (VNDAD)",
        "destination_port": "Port of Los Angeles (USLAX)",
        "order_amount": 150000.0,
        "expected_health": "Critical",
    },
    {
        "key": "SCENARIO_4_CRITICAL_WAREHOUSE_DISCREPANCY",
        "case_title": "[DEMO-S4] Import Ocean CIF — Busan Precision Bearings (Discrepancy)",
        "trade_type": "Import",
        "shipping_mode": "Ocean",
        "incoterm": "CIF",
        "current_stage": "Warehouse",
        "status": "Warehouse Receiving",
        "origin_port": "Busan Port (KRPUS)",
        "destination_port": "Hai Phong Port (VNHPH)",
        "order_amount": 80000.0,
        "expected_health": "Critical",
    },
]


def _get_or_create_trade_case(spec: Dict[str, Any], target_date: str) -> str:
    existing = frappe.db.get_value("Trade Case", {"case_title": spec["case_title"]}, "name")
    if existing:
        return str(existing)
    doc = frappe.get_doc(
        {
            "doctype": "Trade Case",
            "case_title": spec["case_title"],
            "trade_type": spec["trade_type"],
            "shipping_mode": spec["shipping_mode"],
            "mode": spec["shipping_mode"],
            "incoterm": spec["incoterm"],
            "current_stage": spec["current_stage"],
            "status": spec["status"],
            "origin_port": spec["origin_port"],
            "destination_port": spec["destination_port"],
            "order_amount": spec["order_amount"],
            "currency": "USD",
            "priority": "Urgent" if spec["expected_health"] == "Critical" else ("High" if spec["expected_health"] == "Attention" else "Normal"),
            "start_date": str(date.today() - timedelta(days=10)),
            "target_completion_date": target_date,
        }
    )
    doc.insert(ignore_permissions=True)
    return str(doc.name)


def _ensure_shipment(case_id: str, trade_type: str, carrier: str, vessel: str, mode: str, orig: str, dest: str, status: str, delay_days: int, tracking_no: str) -> str:
    existing = frappe.db.get_value("Shipment Tracking", {"trade_case": case_id}, "name")
    if existing:
        return str(existing)
    today = date.today()
    doc = frappe.get_doc(
        {
            "doctype": "Shipment Tracking",
            "name": f"SHP-{case_id}",
            "trade_case": case_id,
            "flow_type": trade_type,
            "shipping_method": mode,
            "carrier": carrier,
            "vessel_name": vessel,
            "tracking_number": tracking_no,
            "origin_port": orig,
            "destination_port": dest,
            "status": status,
            "delay_days": delay_days,
            "is_delayed": 1 if delay_days > 0 else 0,
            "etd": str(today - timedelta(days=7)),
            "atd": str(today - timedelta(days=7)),
            "initial_eta": str(today + timedelta(days=3)),
            "eta": str(today + timedelta(days=3 + delay_days)),
        }
    )
    doc.insert(ignore_permissions=True)
    frappe.db.set_value("Trade Case", case_id, "shipment_tracking", doc.name, update_modified=False)
    return str(doc.name)


def seed_all_demo_scenarios() -> Dict[str, Any]:
    """Idempotently seed all 4 canonical Import & Export demo scenarios in MariaDB."""
    if not (frappe and getattr(frappe, "db", None)):
        return {"success": False, "error": "Frappe DB is not connected."}

    today = date.today()
    seeded_cases: Dict[str, str] = {}

    # ---------------- SCENARIO 1: Healthy Air Import ----------------
    s1_spec = DEMO_SCENARIO_SPECS[0]
    s1_id = _get_or_create_trade_case(s1_spec, str(today + timedelta(days=5)))
    seeded_cases["scenario_1"] = s1_id
    _ensure_shipment(s1_id, "Import", "ANA Cargo", "NH897 B777F", "Air", s1_spec["origin_port"], s1_spec["destination_port"], "Completed", 0, f"ANA-{s1_id}")
    # Verify all mandatory docs
    for d in get_case_documents_list(s1_id):
        if d.get("status") != "N/A" and d.get("status") != "Verified":
            u = upload_trade_document_version(s1_id, d["document_code"], f"/files/{s1_id}_{d['document_code']}.pdf")
            verify_trade_document(u["name"], action="verify", notes="Verified Demo S1")
    if not get_case_customs_declarations(s1_id):
        c1 = create_customs_declaration(s1_id, customs_office_code="01B1", items=[{"item_name": "Optical Sensor", "qty": 50, "unit_price": 900, "import_duty_rate": 0, "vat_rate": 10}])
        propose_hs_code(c1["name"], 1, "90318000", confidence_score=98.5, legal_basis="GIR 1 & TT 31/2022")
        approve_hs_code(c1["name"], 1, action="approve", notes="Verified Optical HS")
        advance_customs_workflow(c1["name"], "Ready", force_skip_doc_check=True)
        advance_customs_workflow(c1["name"], "Declared", declaration_no=f"1061100{s1_id[-4:]}", customs_lane="Green", origin_verified=1, customs_value_verified=1, force_skip_doc_check=True)
        advance_customs_workflow(c1["name"], "Cleared")
    if not frappe.db.exists("Trade Cost Sheet", {"trade_case": s1_id}):
        add_cost_item_to_case(s1_id, "Freight", estimated_cost=3250, actual_cost=3200, invoice_number=f"ANA-INV-{s1_id}", cost_description="Air Freight NRT-HAN", status="Allocated")
        add_cost_item_to_case(s1_id, "Insurance", estimated_cost=400, actual_cost=380, invoice_number=f"INS-{s1_id}", cost_description="Air Cargo Insurance", status="Allocated")
        frappe.db.set_value("Trade Cost Sheet", {"trade_case": s1_id}, {"status": "Finalized", "cost_finalization_status": "FINALIZED"}, update_modified=False)
        frappe.db.set_value("Trade Case", s1_id, "costs_finalized", 1, update_modified=False)
    else:
        sheet_s1 = frappe.db.get_value("Trade Cost Sheet", {"trade_case": s1_id}, "name")
        if sheet_s1:
            frappe.db.sql("UPDATE `tabTrade Cost Item` SET status='Allocated' WHERE parent=%s", (sheet_s1,))
            frappe.db.set_value("Trade Cost Sheet", sheet_s1, {"status": "Finalized", "cost_finalization_status": "FINALIZED"}, update_modified=False)
        for ex_name in frappe.get_all("Shipment Exception", filters={"trade_case": s1_id, "rule_code": "RULE_07_COST_NOT_FINALIZED", "status": ["in", ["Open", "Investigating"]]}, pluck="name"):
            frappe.db.set_value("Shipment Exception", ex_name, "status", "Resolved", update_modified=False)
    wh1 = schedule_warehouse_receiving(s1_id, "Kho Công nghệ cao - WH-HANOI", str(today), expected_qty=50, space_reserved=1, receiving_team="Đội Thiết bị Nhạy cảm")
    record_warehouse_inspection(wh1["name"], received_qty=50, damaged_qty=0, actual_arrival=str(today))
    evaluate_case_exceptions(s1_id, auto_create=True)

    # ---------------- SCENARIO 2: Attention — +2d Delay & Missing C/O ----------------
    s2_spec = DEMO_SCENARIO_SPECS[1]
    s2_id = _get_or_create_trade_case(s2_spec, str(today + timedelta(days=2)))
    seeded_cases["scenario_2"] = s2_id
    _ensure_shipment(s2_id, "Import", "Maersk Line", "MAERSK MC-KINNEY MOLLER", "Ocean", s2_spec["origin_port"], s2_spec["destination_port"], "In Transit", 2, f"MAEU-{s2_id}")
    for d in get_case_documents_list(s2_id):
        if d["document_code"] == "DOC-CO":
            verify_trade_document(d["name"], action="mark_missing", notes="Chờ Supplier gửi C/O Form E gốc")
        elif d.get("status") not in ("N/A", "Verified"):
            u = upload_trade_document_version(s2_id, d["document_code"], f"/files/{s2_id}_{d['document_code']}.pdf")
            verify_trade_document(u["name"], action="verify", notes="Verified Demo S2")
    if not get_case_customs_declarations(s2_id):
        c2 = create_customs_declaration(s2_id, customs_office_code="32BD", co_form="Form E (ACFTA)", items=[{"item_name": "5G Enterprise Router", "qty": 200, "unit_price": 500, "import_duty_rate": 0, "vat_rate": 10}])
        propose_hs_code(c2["name"], 1, "85176299", confidence_score=95.0, legal_basis="GIR 1 & ACFTA Form E")
        approve_hs_code(c2["name"], 1, action="approve", notes="Approved 8517.62.99")
    if not frappe.db.exists("Trade Cost Sheet", {"trade_case": s2_id}):
        add_cost_item_to_case(s2_id, "Freight", estimated_cost=10000, actual_cost=10790, invoice_number=f"MAE-INV-{s2_id}", cost_description="Ocean Freight + Weather BAF", status="Verified")
    schedule_warehouse_receiving(s2_id, "Kho Ngoại quan Cảng Đà Nẵng - WH-DANANG", str(today + timedelta(days=5)), expected_qty=200, space_reserved=1, receiving_team="Đội Tiếp nhận Kho B")
    evaluate_case_exceptions(s2_id, auto_create=True)
    if not get_case_action_items(s2_id):
        create_action_item(s2_id, "Đôn đốc Supplier gửi chuyển phát nhanh C/O Form E gốc", department="Purchasing", owner_name="Tran Thi B", priority="High", due_date=str(today + timedelta(days=1)))

    # ---------------- SCENARIO 3: Critical — Export Red Channel ----------------
    s3_spec = DEMO_SCENARIO_SPECS[2]
    s3_id = _get_or_create_trade_case(s3_spec, str(today + timedelta(days=15)))
    seeded_cases["scenario_3"] = s3_id
    _ensure_shipment(s3_id, "Export", "ONE", "ONE APUS 014E", "Ocean", s3_spec["origin_port"], s3_spec["destination_port"], "Customs Clearance", 0, f"ONEU-{s3_id}")
    if not get_case_customs_declarations(s3_id):
        c3 = create_customs_declaration(s3_id, trade_type="Export", customs_office_code="32BD", items=[{"item_name": "Solar Panel 550W", "qty": 1250, "unit_price": 120, "import_duty_rate": 0, "vat_rate": 0}])
        propose_hs_code(c3["name"], 1, "85414300", confidence_score=97.0, legal_basis="Biểu thuế XK 2026")
        approve_hs_code(c3["name"], 1, action="approve", notes="Approved Solar Panel HS")
        advance_customs_workflow(c3["name"], "Ready", force_skip_doc_check=True)
        advance_customs_workflow(c3["name"], "Declared", declaration_no=f"3068800{s3_id[-4:]}", customs_lane="Red", origin_verified=1, customs_value_verified=1, force_skip_doc_check=True, as_of_date=str(today - timedelta(days=5)))
        advance_customs_workflow(c3["name"], "Processing", as_of_date=str(today))
    if not frappe.db.exists("Trade Cost Sheet", {"trade_case": s3_id}):
        add_cost_item_to_case(s3_id, "Freight", estimated_cost=12000, actual_cost=13800, invoice_number=f"ONE-INV-{s3_id}", cost_description="Export Ocean Freight + Red Channel Overtime", status="Verified")
    sheet_s3 = frappe.db.get_value("Trade Cost Sheet", {"trade_case": s3_id}, "name")
    if sheet_s3:
        s3_doc = frappe.get_doc("Trade Cost Sheet", sheet_s3)
        s3_doc.export_revenue = 150000
        s3_doc.export_cogs = 102000
        s3_doc.save(ignore_permissions=True)
    evaluate_case_exceptions(s3_id, auto_create=True)
    if not get_case_action_items(s3_id):
        create_action_item(s3_id, "Phối hợp Chi cục Hải quan Tiên Sa mở container kiểm hóa Luồng Đỏ", department="Customs", owner_name="Le Van C", priority="Urgent", due_date=str(today))

    # ---------------- SCENARIO 4: Critical — Warehouse Discrepancy ----------------
    s4_spec = DEMO_SCENARIO_SPECS[3]
    s4_id = _get_or_create_trade_case(s4_spec, str(today + timedelta(days=3)))
    seeded_cases["scenario_4"] = s4_id
    _ensure_shipment(s4_id, "Import", "HMM", "HMM ALGECIRAS", "Ocean", s4_spec["origin_port"], s4_spec["destination_port"], "Completed", 0, f"HDMU-{s4_id}")
    wh4 = schedule_warehouse_receiving(s4_id, "Kho Hải Phòng - WH-HAIPHONG", str(today), expected_qty=1000, space_reserved=1, receiving_team="Đội KCS Kho A")
    record_warehouse_inspection(wh4["name"], received_qty=985, damaged_qty=10, actual_arrival=str(today))
    evaluate_case_exceptions(s4_id, auto_create=True)
    if not get_case_action_items(s4_id):
        create_action_item(s4_id, "Lập biên bản giám định bảo hiểm thiếu 15 kiện / hư hỏng 10 kiện", department="Warehouse", owner_name="Hoang Van E", priority="Urgent", due_date=str(today + timedelta(days=1)))

    frappe.db.commit()
    return {"success": True, "seeded_cases": seeded_cases, "count": len(seeded_cases)}


__all__ = ["DEMO_SCENARIO_SPECS", "seed_all_demo_scenarios"]
