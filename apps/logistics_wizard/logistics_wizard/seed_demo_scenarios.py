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
        "supplier": "Tokyo Optical Precision Corp",
        "item_code": "OPTICAL-SENSOR-X1",
        "item_name": "Optical Measuring Sensor System X1",
        "qty": 50.0,
        "rate": 900.0,
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
        "supplier": "Shanghai NetComm Technologies",
        "item_code": "ROUTER-5G-ENT",
        "item_name": "5G Enterprise Core Router",
        "qty": 200.0,
        "rate": 500.0,
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
        "customer": "SunPower California LLC",
        "item_code": "SOLAR-PANEL-550W",
        "item_name": "Monocrystalline Solar Photovoltaic Module 550W",
        "qty": 1250.0,
        "rate": 120.0,
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
        "supplier": "Busan Precision Bearing Co.",
        "item_code": "BEARING-CNC-P4",
        "item_name": "Precision CNC Spindle Ball Bearing P4",
        "qty": 1000.0,
        "rate": 80.0,
    },
    {
        "key": "SCENARIO_5_HEALTHY_EXPORT_AIR_COMPLETE",
        "case_title": "[DEMO-S5] Export Air FOB — Ho Chi Minh Solar Inverters to Tokyo",
        "trade_type": "Export",
        "shipping_mode": "Air",
        "incoterm": "FOB",
        "current_stage": "Closed",
        "status": "Completed",
        "origin_port": "Tan Son Nhat Airport (SGN)",
        "destination_port": "Tokyo Narita (NRT)",
        "order_amount": 96000.0,
        "expected_health": "Healthy",
        "customer": "Tokyo Solar Distribution Inc",
        "item_code": "SOLAR-INVERTER-10K",
        "item_name": "Hybrid Solar Inverter 10kW Three-Phase",
        "qty": 80.0,
        "rate": 1200.0,
    },
]


def _ensure_partner_and_item(spec: Dict[str, Any], company: str) -> Dict[str, str]:
    """Ensure real ERPNext Supplier/Customer and Item master records exist for demo linking."""
    out: Dict[str, str] = {"company": company}
    currency = "USD"
    item_group = frappe.db.get_value("Item Group", {}, "name") or "All Item Groups"
    default_wh = frappe.db.get_value("Warehouse", {"company": company, "is_group": 0}, "name")
    if default_wh:
        out["warehouse"] = default_wh

    item_code = spec.get("item_code")
    if item_code and not frappe.db.exists("Item", item_code):
        it_doc = frappe.get_doc({
            "doctype": "Item",
            "item_code": item_code,
            "item_name": spec.get("item_name") or item_code,
            "item_group": item_group,
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "standard_rate": float(spec.get("rate") or 100.0),
        })
        it_doc.insert(ignore_permissions=True)

    if spec["trade_type"] == "Import":
        sup = spec.get("supplier")
        if sup and not frappe.db.exists("Supplier", sup):
            sup_group = frappe.db.get_value("Supplier Group", {}, "name") or "All Supplier Groups"
            frappe.get_doc({
                "doctype": "Supplier",
                "supplier_name": sup,
                "supplier_group": sup_group,
                "supplier_type": "Company",
                "default_currency": currency,
            }).insert(ignore_permissions=True)
        out["party_type"] = "Supplier"
        out["party"] = sup or ""
    else:
        cust = spec.get("customer")
        if cust and not frappe.db.exists("Customer", cust):
            cust_group = frappe.db.get_value("Customer Group", {}, "name") or "All Customer Groups"
            terr = frappe.db.get_value("Territory", {}, "name") or "All Territories"
            frappe.get_doc({
                "doctype": "Customer",
                "customer_name": cust,
                "customer_group": cust_group,
                "customer_type": "Company",
                "territory": terr,
                "default_currency": currency,
            }).insert(ignore_permissions=True)
        out["party_type"] = "Customer"
        out["party"] = cust or ""
    return out


def _ensure_po_or_so(case_id: str, spec: Dict[str, Any], meta: Dict[str, str]) -> str:
    """Create and submit a real Purchase Order (Import) or Sales Order (Export) linked to Trade Case."""
    company = meta["company"]
    wh = meta.get("warehouse")
    price_list = "Standard Buying" if spec["trade_type"] == "Import" else "Standard Selling"
    if not frappe.db.exists("Price List", price_list):
        frappe.get_doc({
            "doctype": "Price List",
            "price_list_name": price_list,
            "enabled": 1,
            "buying": 1 if spec["trade_type"] == "Import" else 0,
            "selling": 1 if spec["trade_type"] == "Export" else 0,
            "currency": "USD",
        }).insert(ignore_permissions=True)

    if spec["trade_type"] == "Import":
        existing = frappe.db.get_value("Trade Case", case_id, "purchase_order")
        if not existing or not frappe.db.exists("Purchase Order", existing):
            existing = frappe.db.get_value(
                "Purchase Order",
                {"supplier": meta["party"], "grand_total": float(spec["order_amount"]), "docstatus": 1},
                "name",
            )
        if not existing:
            po = frappe.get_doc({
                "doctype": "Purchase Order",
                "company": company,
                "supplier": meta["party"],
                "currency": "USD",
                "conversion_rate": float(frappe.db.get_value("Purchase Order", {"docstatus": 1}, "conversion_rate") or 1.0),
                "buying_price_list": price_list,
                "transaction_date": str(date.today() - timedelta(days=12)),
                "schedule_date": str(date.today() + timedelta(days=3)),
                "items": [{
                    "item_code": spec["item_code"],
                    "item_name": spec["item_name"],
                    "qty": float(spec["qty"]),
                    "rate": float(spec["rate"]),
                    "schedule_date": str(date.today() + timedelta(days=3)),
                    **({"warehouse": wh} if wh else {}),
                }],
            })
            po.insert(ignore_permissions=True)
            po.submit()
            existing = po.name
        frappe.db.set_value("Trade Case", case_id, {"supplier": meta["party"], "purchase_order": existing}, update_modified=False)
        return str(existing)

    existing_so = frappe.db.get_value("Trade Case", case_id, "sales_order")
    if not existing_so or not frappe.db.exists("Sales Order", existing_so):
        existing_so = frappe.db.get_value(
            "Sales Order",
            {"customer": meta["party"], "docstatus": 1},
            "name",
        )
    if not existing_so:
        so = frappe.get_doc({
            "doctype": "Sales Order",
            "company": company,
            "customer": meta["party"],
            "currency": "USD",
            "conversion_rate": float(frappe.db.get_value("Purchase Order", {"docstatus": 1}, "conversion_rate") or 1.0),
            "selling_price_list": price_list,
            "transaction_date": str(date.today() - timedelta(days=10)),
            "delivery_date": str(date.today() + timedelta(days=5)),
            "items": [{
                "item_code": spec["item_code"],
                "item_name": spec["item_name"],
                "qty": float(spec["qty"]),
                "rate": float(spec["rate"]),
                "delivery_date": str(date.today() + timedelta(days=5)),
                **({"warehouse": wh} if wh else {}),
            }],
        })
        so.insert(ignore_permissions=True)
        so.submit()
        existing_so = so.name
    frappe.db.set_value("Trade Case", case_id, {"customer": meta["party"], "sales_order": existing_so}, update_modified=False)
    return str(existing_so)


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
            "supplier": spec.get("supplier"),
            "customer": spec.get("customer"),
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


def _ensure_shipment(
    case_id: str,
    trade_type: str,
    carrier: str,
    vessel: str,
    mode: str,
    orig: str,
    dest: str,
    status: str,
    delay_days: int,
    tracking_no: str,
    po_name: str = None,
    so_name: str = None,
) -> str:
    from logistics_wizard import routing

    orig_c = routing.get_location_coords(orig) or (20.8656, 106.762)
    dest_c = routing.get_location_coords(dest) or (10.7626, 106.7898)
    mid_lat = round((orig_c[0] + dest_c[0]) / 2.0, 4)
    mid_lon = round((orig_c[1] + dest_c[1]) / 2.0, 4)
    today = date.today()

    milestones = [
        ("BOOKED", "Đặt chỗ vận chuyển quốc tế", orig, orig_c, -9),
        ("GATE_IN", "Hạ bãi / Ga hàng hóa xuất", orig, orig_c, -8),
        ("LOADED", "Xếp hàng lên phương tiện", orig, orig_c, -7),
        ("DEPARTED", "Khởi hành rời cảng/sân bay xuất", orig, orig_c, -7),
        ("TRANSSHIPMENT", "Đang hành trình quốc tế", f"{orig} -> {dest}", (mid_lat, mid_lon), -2),
        ("ARRIVED", "Cập cảng / Hạ cánh điểm đến", dest, dest_c, 0 if status == "Completed" else 2 + delay_days),
        ("DISCHARGED", "Dỡ hàng khỏi tàu/máy bay", dest, dest_c, 0 if status == "Completed" else 2 + delay_days),
        ("GATE_OUT", "Hoàn tất thủ tục & Ra cổng cảng", dest, dest_c, 0 if status == "Completed" else 3 + delay_days),
        ("DELIVERED", "Bàn giao kho đích hoàn tất", dest, dest_c, 0 if status == "Completed" else 3 + delay_days),
    ]
    current_idx = 8 if status == "Completed" else (5 if status == "Customs Clearance" else 4)

    existing = frappe.db.get_value("Shipment Tracking", {"trade_case": case_id}, "name")
    if existing:
        doc = frappe.get_doc("Shipment Tracking", existing)
        changed = False
        if po_name and not doc.purchase_order:
            doc.purchase_order = po_name
            changed = True
        if so_name and not doc.sales_order:
            doc.sales_order = so_name
            changed = True
        if not (getattr(doc, "transit_route", None) and len(doc.transit_route) >= 5):
            doc.set("transit_route", [])
            for idx_m, (m_code, act, loc, coords, day_off) in enumerate(milestones):
                d_str = str(today + timedelta(days=day_off))
                doc.append("transit_route", {
                    "milestone": m_code,
                    "activity": act,
                    "location": loc,
                    "date": d_str,
                    "timestamp": f"{d_str} 10:00:00",
                    "lat": coords[0],
                    "lon": coords[1],
                    "vessel_or_flight": vessel,
                    "is_current": 1 if idx_m == current_idx else 0,
                })
            changed = True
        if changed:
            doc.save(ignore_permissions=True)
        return str(existing)

    doc = frappe.get_doc(
        {
            "doctype": "Shipment Tracking",
            "name": f"SHP-{case_id}",
            "trade_case": case_id,
            "flow_type": trade_type,
            "purchase_order": po_name if trade_type == "Import" else None,
            "sales_order": so_name if trade_type == "Export" else None,
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
            "current_lat": dest_c[0] if status in ("Completed", "Customs Clearance") else mid_lat,
            "current_lon": dest_c[1] if status in ("Completed", "Customs Clearance") else mid_lon,
            "transit_route": [
                {
                    "milestone": m_code,
                    "activity": act,
                    "location": loc,
                    "date": str(today + timedelta(days=day_off)),
                    "timestamp": f"{today + timedelta(days=day_off)} 10:00:00",
                    "lat": coords[0],
                    "lon": coords[1],
                    "vessel_or_flight": vessel,
                    "is_current": 1 if idx_m == current_idx else 0,
                }
                for idx_m, (m_code, act, loc, coords, day_off) in enumerate(milestones)
            ],
        }
    )
    doc.insert(ignore_permissions=True)
    frappe.db.set_value("Trade Case", case_id, "shipment_tracking", doc.name, update_modified=False)
    return str(doc.name)


def _ensure_pr_and_lcv(case_id: str, po_name: str, qty_received: float = None) -> None:
    """Create a real ERPNext Purchase Receipt + draft/submitted Landed Cost Voucher linked to Cost Sheet."""
    from logistics_wizard.costing_engine.api import allocate_and_sync_lcv

    sheet_name = frappe.db.get_value("Trade Cost Sheet", {"trade_case": case_id, "docstatus": ["!=", 2]}, "name")
    if not po_name or not frappe.db.exists("Purchase Order", po_name):
        return
    pr_name = frappe.db.get_value("Purchase Receipt Item", {"purchase_order": po_name, "docstatus": ["!=", 2]}, "parent")
    if not pr_name:
        try:
            from erpnext.buying.doctype.purchase_order.purchase_order import make_purchase_receipt
            pr_doc = make_purchase_receipt(po_name)
            pr_doc.posting_date = str(date.today())
            if qty_received and pr_doc.items:
                pr_doc.items[0].qty = float(qty_received)
            pr_doc.insert(ignore_permissions=True)
            pr_doc.submit()
            pr_name = pr_doc.name
        except Exception:
            pr_name = None
    if sheet_name and pr_name:
        sheet = frappe.get_doc("Trade Cost Sheet", sheet_name)
        if not getattr(sheet, "document_links", None):
            sheet.set("document_links", [{
                "document_type": "Purchase Receipt",
                "document_name": pr_name,
                "document_status": "Submitted",
            }])
            sheet.save(ignore_permissions=True)
        if not getattr(sheet, "landed_cost_voucher", None):
            try:
                allocate_and_sync_lcv(sheet_name, auto_submit=True)
            except Exception:
                pass


def seed_all_demo_scenarios() -> Dict[str, Any]:
    """Idempotently seed all 5 canonical Import & Export demo scenarios in MariaDB."""
    if not (frappe and getattr(frappe, "db", None)):
        return {"success": False, "error": "Frappe DB is not connected."}

    company = frappe.db.get_value("Company", {}, "name") or "Cap Khanh Logistics"
    today = date.today()
    seeded_cases: Dict[str, str] = {}

    # ---------------- SCENARIO 1: Healthy Air Import ----------------
    s1_spec = DEMO_SCENARIO_SPECS[0]
    s1_meta = _ensure_partner_and_item(s1_spec, company)
    s1_id = _get_or_create_trade_case(s1_spec, str(today + timedelta(days=5)))
    s1_po = _ensure_po_or_so(s1_id, s1_spec, s1_meta)
    seeded_cases["scenario_1"] = s1_id
    _ensure_shipment(s1_id, "Import", "ANA Cargo", "NH897 B777F", "Air", s1_spec["origin_port"], s1_spec["destination_port"], "Completed", 0, f"ANA-{s1_id}", po_name=s1_po)
    for d in get_case_documents_list(s1_id):
        if d.get("status") != "N/A" and d.get("status") != "Verified":
            u = upload_trade_document_version(s1_id, d["document_code"], f"/files/{s1_id}_{d['document_code']}.pdf")
            verify_trade_document(u["name"], action="verify", notes="Verified Demo S1")
    if not get_case_customs_declarations(s1_id):
        c1 = create_customs_declaration(s1_id, customs_office_code="01B1", items=[{"item_code": s1_spec["item_code"], "item_name": s1_spec["item_name"], "qty": 50, "unit_price": 900, "import_duty_rate": 0, "vat_rate": 10}])
        propose_hs_code(c1["name"], 1, "90318000", confidence_score=98.5, legal_basis="GIR 1 & TT 31/2022")
        approve_hs_code(c1["name"], 1, action="approve", notes="Verified Optical HS")
        advance_customs_workflow(c1["name"], "Ready", force_skip_doc_check=True)
        advance_customs_workflow(c1["name"], "Declared", declaration_no=f"1061100{s1_id[-4:]}", customs_lane="Green", origin_verified=1, customs_value_verified=1, force_skip_doc_check=True)
        advance_customs_workflow(c1["name"], "Cleared")
    if not frappe.db.exists("Trade Cost Sheet", {"trade_case": s1_id}):
        add_cost_item_to_case(s1_id, "Freight", estimated_cost=3250, actual_cost=3200, invoice_number=f"ANA-INV-{s1_id}", cost_description="Air Freight NRT-HAN", status="Allocated")
        add_cost_item_to_case(s1_id, "Insurance", estimated_cost=400, actual_cost=380, invoice_number=f"INS-{s1_id}", cost_description="Air Cargo Insurance", status="Allocated")
    _ensure_pr_and_lcv(s1_id, s1_po, qty_received=50)
    sheet_s1 = frappe.db.get_value("Trade Cost Sheet", {"trade_case": s1_id}, "name")
    if sheet_s1:
        frappe.db.sql("UPDATE `tabTrade Cost Item` SET status='Allocated' WHERE parent=%s", (sheet_s1,))
        frappe.db.set_value("Trade Cost Sheet", sheet_s1, {"status": "Finalized", "cost_finalization_status": "FINALIZED"}, update_modified=False)
        frappe.db.set_value("Trade Case", s1_id, "costs_finalized", 1, update_modified=False)
    for ex_name in frappe.get_all("Shipment Exception", filters={"trade_case": s1_id, "rule_code": "RULE_07_COST_NOT_FINALIZED", "status": ["in", ["Open", "Investigating"]]}, pluck="name"):
        frappe.db.set_value("Shipment Exception", ex_name, "status", "Resolved", update_modified=False)
    wh1 = schedule_warehouse_receiving(s1_id, "Kho Công nghệ cao - WH-HANOI", str(today), expected_qty=50, space_reserved=1, receiving_team="Đội Thiết bị Nhạy cảm")
    record_warehouse_inspection(wh1["name"], received_qty=50, damaged_qty=0, actual_arrival=str(today))
    evaluate_case_exceptions(s1_id, auto_create=True)

    # ---------------- SCENARIO 2: Attention — +2d Delay & Missing C/O ----------------
    s2_spec = DEMO_SCENARIO_SPECS[1]
    s2_meta = _ensure_partner_and_item(s2_spec, company)
    s2_id = _get_or_create_trade_case(s2_spec, str(today + timedelta(days=2)))
    s2_po = _ensure_po_or_so(s2_id, s2_spec, s2_meta)
    seeded_cases["scenario_2"] = s2_id
    _ensure_shipment(s2_id, "Import", "Maersk Line", "MAERSK MC-KINNEY MOLLER", "Ocean", s2_spec["origin_port"], s2_spec["destination_port"], "In Transit", 2, f"MAEU-{s2_id}", po_name=s2_po)
    for d in get_case_documents_list(s2_id):
        if d["document_code"] == "DOC-CO":
            verify_trade_document(d["name"], action="mark_missing", notes="Chờ Supplier gửi C/O Form E gốc")
        elif d.get("status") not in ("N/A", "Verified"):
            u = upload_trade_document_version(s2_id, d["document_code"], f"/files/{s2_id}_{d['document_code']}.pdf")
            verify_trade_document(u["name"], action="verify", notes="Verified Demo S2")
    if not get_case_customs_declarations(s2_id):
        c2 = create_customs_declaration(s2_id, customs_office_code="32BD", co_form="Form E (ACFTA)", items=[{"item_code": s2_spec["item_code"], "item_name": s2_spec["item_name"], "qty": 200, "unit_price": 500, "import_duty_rate": 0, "vat_rate": 10}])
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
    s3_meta = _ensure_partner_and_item(s3_spec, company)
    s3_id = _get_or_create_trade_case(s3_spec, str(today + timedelta(days=15)))
    s3_so = _ensure_po_or_so(s3_id, s3_spec, s3_meta)
    seeded_cases["scenario_3"] = s3_id
    s3_shp = _ensure_shipment(s3_id, "Export", "ONE", "ONE APUS 014E", "Ocean", s3_spec["origin_port"], s3_spec["destination_port"], "Customs Clearance", 0, f"ONEU-{s3_id}", so_name=s3_so)
    # Create draft Delivery Note linked to SO & Shipment for Export Red Channel (awaiting clearance)
    if not frappe.db.exists("Delivery Note Item", {"against_sales_order": s3_so, "docstatus": ["!=", 2]}):
        try:
            from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note
            dn3 = make_delivery_note(s3_so)
            dn3.posting_date = str(today)
            if hasattr(dn3, "shipment_tracking"):
                dn3.shipment_tracking = s3_shp
            dn3.insert(ignore_permissions=True)
        except Exception:
            pass
    if not get_case_customs_declarations(s3_id):
        c3 = create_customs_declaration(s3_id, trade_type="Export", customs_office_code="32BD", items=[{"item_code": s3_spec["item_code"], "item_name": s3_spec["item_name"], "qty": 1250, "unit_price": 120, "import_duty_rate": 0, "vat_rate": 0}])
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
    s4_meta = _ensure_partner_and_item(s4_spec, company)
    s4_id = _get_or_create_trade_case(s4_spec, str(today + timedelta(days=3)))
    s4_po = _ensure_po_or_so(s4_id, s4_spec, s4_meta)
    seeded_cases["scenario_4"] = s4_id
    _ensure_shipment(s4_id, "Import", "HMM", "HMM ALGECIRAS", "Ocean", s4_spec["origin_port"], s4_spec["destination_port"], "Completed", 0, f"HDMU-{s4_id}", po_name=s4_po)
    for d in get_case_documents_list(s4_id):
        if d.get("status") not in ("N/A", "Verified"):
            u = upload_trade_document_version(s4_id, d["document_code"], f"/files/{s4_id}_{d['document_code']}.pdf")
            verify_trade_document(u["name"], action="verify", notes="Verified Demo S4")
    if not get_case_customs_declarations(s4_id):
        c4 = create_customs_declaration(s4_id, customs_office_code="03CC", items=[{"item_code": s4_spec["item_code"], "item_name": s4_spec["item_name"], "qty": 1000, "unit_price": 80, "import_duty_rate": 3.0, "vat_rate": 10.0}])
        propose_hs_code(c4["name"], 1, "84821000", confidence_score=96.0, legal_basis="GIR 1 & Nhóm 84.82 Biểu thuế")
        approve_hs_code(c4["name"], 1, action="approve", notes="Approved Bearing HS")
        advance_customs_workflow(c4["name"], "Ready", force_skip_doc_check=True)
        advance_customs_workflow(c4["name"], "Declared", declaration_no=f"1064400{s4_id[-4:]}", customs_lane="Green", origin_verified=1, customs_value_verified=1, force_skip_doc_check=True)
        advance_customs_workflow(c4["name"], "Cleared")
    if not frappe.db.exists("Trade Cost Sheet", {"trade_case": s4_id}):
        add_cost_item_to_case(s4_id, "Freight", estimated_cost=4200, actual_cost=4200, invoice_number=f"HMM-INV-{s4_id}", cost_description="Ocean Freight Busan - Hai Phong", status="Verified")
        add_cost_item_to_case(s4_id, "Port", estimated_cost=650, actual_cost=650, invoice_number=f"HPH-PRT-{s4_id}", cost_description="Hai Phong Terminal & Demurrage Survey", status="Verified")
    _ensure_pr_and_lcv(s4_id, s4_po, qty_received=985)
    wh4 = schedule_warehouse_receiving(s4_id, "Kho Hải Phòng - WH-HAIPHONG", str(today), expected_qty=1000, space_reserved=1, receiving_team="Đội KCS Kho A")
    record_warehouse_inspection(wh4["name"], received_qty=985, damaged_qty=10, actual_arrival=str(today))
    evaluate_case_exceptions(s4_id, auto_create=True)
    if not get_case_action_items(s4_id):
        create_action_item(s4_id, "Lập biên bản giám định bảo hiểm thiếu 15 kiện / hư hỏng 10 kiện", department="Warehouse", owner_name="Hoang Van E", priority="Urgent", due_date=str(today + timedelta(days=1)))

    # ---------------- SCENARIO 5: Healthy Export Air Complete (SO -> DN -> SI + Green Customs) ----------------
    s5_spec = DEMO_SCENARIO_SPECS[4]
    s5_meta = _ensure_partner_and_item(s5_spec, company)
    s5_id = _get_or_create_trade_case(s5_spec, str(today - timedelta(days=1)))
    s5_so = _ensure_po_or_so(s5_id, s5_spec, s5_meta)
    seeded_cases["scenario_5"] = s5_id
    s5_shp = _ensure_shipment(s5_id, "Export", "Vietnam Airlines Cargo", "VN-CARGO-310", "Air", s5_spec["origin_port"], s5_spec["destination_port"], "Completed", 0, f"VN-EXP-{s5_id}", so_name=s5_so)
    for d in get_case_documents_list(s5_id):
        if d.get("status") not in ("N/A", "Verified"):
            u = upload_trade_document_version(s5_id, d["document_code"], f"/files/{s5_id}_{d['document_code']}.pdf")
            verify_trade_document(u["name"], action="verify", notes="Verified Export Demo S5")
    if not get_case_customs_declarations(s5_id):
        c5 = create_customs_declaration(s5_id, trade_type="Export", customs_office_code="02CI", items=[{"item_code": s5_spec["item_code"], "item_name": s5_spec["item_name"], "qty": 80, "unit_price": 1200, "import_duty_rate": 0, "vat_rate": 0}])
        propose_hs_code(c5["name"], 1, "85044090", confidence_score=96.5, legal_basis="GIR 1 & Nhóm 85.04 Biểu thuế XK")
        approve_hs_code(c5["name"], 1, action="approve", notes="Approved Solar Inverter HS")
        advance_customs_workflow(c5["name"], "Ready", force_skip_doc_check=True)
        advance_customs_workflow(c5["name"], "Declared", declaration_no=f"3069900{s5_id[-4:]}", customs_lane="Green", origin_verified=1, customs_value_verified=1, force_skip_doc_check=True)
        advance_customs_workflow(c5["name"], "Cleared")
    if not frappe.db.exists("Trade Cost Sheet", {"trade_case": s5_id}):
        add_cost_item_to_case(s5_id, "Freight", estimated_cost=4300, actual_cost=4150, invoice_number=f"VN-INV-{s5_id}", cost_description="Air Freight Export SGN - NRT", status="Allocated")
        add_cost_item_to_case(s5_id, "Broker Fee", estimated_cost=650, actual_cost=650, invoice_number=f"BRK-{s5_id}", cost_description="Export Customs Brokerage & Terminal", status="Allocated")
    sheet_s5 = frappe.db.get_value("Trade Cost Sheet", {"trade_case": s5_id}, "name")
    if sheet_s5:
        s5_doc = frappe.get_doc("Trade Cost Sheet", sheet_s5)
        s5_doc.export_revenue = 96000
        s5_doc.export_cogs = 64000
        s5_doc.status = "Finalized"
        s5_doc.save(ignore_permissions=True)
        frappe.db.sql("UPDATE `tabTrade Cost Item` SET status='Allocated' WHERE parent=%s", (sheet_s5,))
        frappe.db.set_value("Trade Cost Sheet", sheet_s5, {"status": "Finalized", "cost_finalization_status": "FINALIZED"}, update_modified=False)
        frappe.db.set_value("Trade Case", s5_id, "costs_finalized", 1, update_modified=False)
    # Create Delivery Note & Sales Invoice for Scenario 5 Export workflow
    from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note, make_sales_invoice
    if not frappe.db.exists("Delivery Note Item", {"against_sales_order": s5_so, "docstatus": ["!=", 2]}):
        try:
            dn5 = make_delivery_note(s5_so)
            dn5.posting_date = str(today)
            if hasattr(dn5, "shipment_tracking"):
                dn5.shipment_tracking = s5_shp
            dn5.insert(ignore_permissions=True)
            frappe.db.set_value("Shipment Tracking", s5_shp, "delivery_note", dn5.name, update_modified=False)
        except Exception as dn_err:
            frappe.log_error(f"Scenario 5 DN error: {dn_err}")
    if not frappe.db.exists("Sales Invoice Item", {"sales_order": s5_so, "docstatus": ["!=", 2]}):
        try:
            si5 = make_sales_invoice(s5_so)
            si5.posting_date = str(today)
            usd_rec = frappe.db.get_value(
                "Account",
                {"company": s5_spec.get("company") or company, "account_type": "Receivable", "account_currency": "USD"},
                "name",
            )
            if usd_rec:
                si5.debit_to = usd_rec
            si5.insert(ignore_permissions=True)
            si5.submit()
        except Exception as si_err:
            frappe.log_error(f"Scenario 5 SI error: {si_err}")
    evaluate_case_exceptions(s5_id, auto_create=True)
    for ex_name in frappe.get_all("Shipment Exception", filters={"trade_case": s5_id, "status": ["in", ["Open", "Investigating"]]}, pluck="name"):
        frappe.db.set_value("Shipment Exception", ex_name, "status", "Resolved", update_modified=False)
    frappe.db.set_value("Trade Case", s5_id, {"overall_health": "Healthy", "open_exceptions_count": 0, "critical_exceptions_count": 0}, update_modified=False)

    frappe.db.commit()
    return {"success": True, "seeded_cases": seeded_cases, "count": len(seeded_cases)}


__all__ = ["DEMO_SCENARIO_SPECS", "seed_all_demo_scenarios"]
