#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seed_trade_cases_and_costing.py
Populates real Trade Case and Trade Cost Sheet records linking to existing
Purchase Orders and Shipment Tracking in the logistics.local site.
"""

import frappe
from frappe.utils import today, add_days, now

def run():
    print(">>> Seeding Trade Cases and Trade Cost Sheets...")
    if not frappe.db:
        frappe.init(site="logistics.local")
        frappe.connect()

    company = frappe.db.get_value("Company", {}, "name") or "Cap Khanh Logistics"
    admin_user = "Administrator"

    # Define the 10 real Trade Cases mapped to the 10 POs & Shipments
    trade_cases_spec = [
        {
            "name": "TC-2026-00001",
            "case_title": "Nhập khẩu máy móc thiết bị Apple Inc. (Cảng Cát Lái - Đã hoàn tất)",
            "trade_type": "Import",
            "status": "Completed",
            "current_stage": "Closed",
            "overall_health": "Healthy",
            "priority": "High",
            "purchase_order": "PUR-ORD-2026-00002",
            "supplier": "Apple Inc.",
            "company": company,
            "currency": "USD",
            "order_amount": 550000.0,
            "shipping_mode": "Ocean",
            "mode": "Ocean",
            "incoterm": "CIF",
            "origin_country": "United States",
            "origin_port": "Shanghai Port (CNSHG)",
            "destination_country": "Vietnam",
            "destination_port": "Cat Lai Port, HCMC (VNHCM)",
            "case_owner": admin_user,
            "department": "Logistics & Procurement",
            "start_date": add_days(today(), -20),
            "target_completion_date": add_days(today(), -2),
            "actual_completion_date": add_days(today(), -1),
            "opened_date": add_days(today(), -20),
            "closed_date": add_days(today(), -1),
            "shipment_status_summary": "Lô hàng 1x40HC đã thông quan và dỡ kho hoàn tất",
            "document_readiness_pct": 100.0,
            "customs_declaration_no": "105988220190",
            "customs_lane": "Green",
            "customs_cleared": 1,
            "estimated_landed_cost": 585000.0,
            "actual_landed_cost": 582400.0,
            "cost_variance_pct": -0.44,
            "costs_finalized": 1,
            "open_exceptions_count": 0,
            "critical_exceptions_count": 0,
            "shipment_tracking": "ST-2026-00001",
            "stage_gate_status": "Passed"
        },
        {
            "name": "TC-2026-00002",
            "case_title": "Nhập khẩu linh kiện điện tử Apple Inc. qua đường hàng không (Nội Bài)",
            "trade_type": "Import",
            "status": "In Transit",
            "current_stage": "In Transit",
            "overall_health": "Healthy",
            "priority": "Urgent",
            "purchase_order": "PUR-ORD-2026-00003",
            "supplier": "Apple Inc.",
            "company": company,
            "currency": "USD",
            "order_amount": 330000.0,
            "shipping_mode": "Air",
            "mode": "Air",
            "incoterm": "CIF",
            "origin_country": "United States",
            "origin_port": "San Francisco (SFO)",
            "destination_country": "Vietnam",
            "destination_port": "Noi Bai International Airport (HAN)",
            "case_owner": admin_user,
            "department": "Air Freight Operations",
            "start_date": add_days(today(), -5),
            "target_completion_date": add_days(today(), 3),
            "opened_date": add_days(today(), -5),
            "expected_close_date": add_days(today(), 3),
            "shipment_status_summary": "Chuyến bay VN-CARGO-991 đang vận chuyển, ETA đúng lịch",
            "document_readiness_pct": 95.0,
            "customs_declaration_no": "105994402110",
            "customs_lane": "Green",
            "customs_cleared": 0,
            "estimated_landed_cost": 348000.0,
            "actual_landed_cost": 348000.0,
            "cost_variance_pct": 0.0,
            "costs_finalized": 0,
            "open_exceptions_count": 0,
            "critical_exceptions_count": 0,
            "shipment_tracking": "ST-2026-00002",
            "stage_gate_status": "Pending"
        },
        {
            "name": "TC-2026-00003",
            "case_title": "Nhập khẩu trang sức đá quý Pandora Jewelry (Bangkok - Tân Sơn Nhất)",
            "trade_type": "Import",
            "status": "In Transit",
            "current_stage": "In Transit",
            "overall_health": "Healthy",
            "priority": "High",
            "purchase_order": "PUR-ORD-2026-00004",
            "supplier": "Pandora Jewelry Ltd",
            "company": company,
            "currency": "USD",
            "order_amount": 76000.0,
            "shipping_mode": "Air",
            "mode": "Air",
            "incoterm": "FOB",
            "origin_country": "Thailand",
            "origin_port": "Suvarnabhumi Airport (BKK)",
            "destination_country": "Vietnam",
            "destination_port": "Tan Son Nhat (SGN)",
            "case_owner": admin_user,
            "department": "Luxury Goods Logistics",
            "start_date": add_days(today(), -3),
            "target_completion_date": add_days(today(), 4),
            "opened_date": add_days(today(), -3),
            "expected_close_date": add_days(today(), 4),
            "shipment_status_summary": "Hàng giá trị cao đang vận chuyển đường hàng không Thai Airways",
            "document_readiness_pct": 90.0,
            "customs_declaration_no": "105988210342",
            "customs_lane": "Yellow",
            "customs_cleared": 0,
            "estimated_landed_cost": 84500.0,
            "actual_landed_cost": 84500.0,
            "cost_variance_pct": 0.0,
            "costs_finalized": 0,
            "open_exceptions_count": 0,
            "critical_exceptions_count": 0,
            "shipment_tracking": "ST-PANDORA-AIR-01",
            "stage_gate_status": "Pending"
        },
        {
            "name": "TC-2026-00004",
            "case_title": "Nhập khẩu động cơ & linh kiện cơ khí Yamaha Motor (Yokohama - Cát Lái)",
            "trade_type": "Import",
            "status": "In Transit",
            "current_stage": "In Transit",
            "overall_health": "Healthy",
            "priority": "Normal",
            "purchase_order": "PUR-ORD-2026-00010",
            "supplier": "Yamaha Motor Co., Ltd.",
            "company": company,
            "currency": "USD",
            "order_amount": 867000.0,
            "shipping_mode": "Ocean",
            "mode": "Ocean",
            "incoterm": "CIF",
            "origin_country": "Japan",
            "origin_port": "Yokohama Port (JPYOK)",
            "destination_country": "Vietnam",
            "destination_port": "Cat Lai Port, HCMC (VNHCM)",
            "case_owner": admin_user,
            "department": "Automotive Operations",
            "start_date": add_days(today(), -10),
            "target_completion_date": add_days(today(), 6),
            "opened_date": add_days(today(), -10),
            "expected_close_date": add_days(today(), 6),
            "shipment_status_summary": "Tàu NYK đang hành trình ngoài khơi Biển Đông",
            "document_readiness_pct": 88.0,
            "customs_declaration_no": "105977110788",
            "customs_lane": "Green",
            "customs_cleared": 0,
            "estimated_landed_cost": 918000.0,
            "actual_landed_cost": 918000.0,
            "cost_variance_pct": 0.0,
            "costs_finalized": 0,
            "open_exceptions_count": 0,
            "critical_exceptions_count": 0,
            "shipment_tracking": "ST-YAMAHA-SEA-07",
            "stage_gate_status": "Pending"
        },
        {
            "name": "TC-2026-00005",
            "case_title": "Nhập khẩu ô tô nguyên chiếc Toyota Motor RORO (Laem Chabang - Đình Vũ)",
            "trade_type": "Import",
            "status": "In Transit",
            "current_stage": "In Transit",
            "overall_health": "Attention",
            "priority": "High",
            "purchase_order": "PUR-ORD-2026-00008",
            "supplier": "Toyota Motor Thailand",
            "company": company,
            "currency": "USD",
            "order_amount": 1433500.0,
            "shipping_mode": "Ocean",
            "mode": "Ocean",
            "incoterm": "FOB",
            "origin_country": "Thailand",
            "origin_port": "Laem Chabang (THLCH)",
            "destination_country": "Vietnam",
            "destination_port": "Dinh Vu Port, Hai Phong (VNHPH)",
            "case_owner": admin_user,
            "department": "Automotive Logistics",
            "start_date": add_days(today(), -8),
            "target_completion_date": add_days(today(), 5),
            "opened_date": add_days(today(), -8),
            "expected_close_date": add_days(today(), 5),
            "shipment_status_summary": "Tàu RORO gặp sóng to tại Vịnh Thái Lan, dự kiến trễ ETA +2 ngày",
            "document_readiness_pct": 80.0,
            "missing_critical_docs": "Bản gốc C/O Form D đang chuyển phát nhanh",
            "customs_declaration_no": "105999440599",
            "customs_lane": "Yellow",
            "customs_cleared": 0,
            "estimated_landed_cost": 1560000.0,
            "actual_landed_cost": 1582000.0,
            "cost_variance_pct": 1.41,
            "costs_finalized": 0,
            "open_exceptions_count": 1,
            "critical_exceptions_count": 0,
            "shipment_tracking": "ST-TOYOTA-RORO-05",
            "stage_gate_status": "Pending"
        },
        {
            "name": "TC-2026-00006",
            "case_title": "Nhập khẩu phụ tùng xe máy Honda Thailand RORO (Bangkok - Cái Mép)",
            "trade_type": "Import",
            "status": "In Transit",
            "current_stage": "In Transit",
            "overall_health": "Healthy",
            "priority": "Normal",
            "purchase_order": "PUR-ORD-2026-00009",
            "supplier": "Honda Vietnam/Thailand Co.",
            "company": company,
            "currency": "USD",
            "order_amount": 1300000.0,
            "shipping_mode": "Ocean",
            "mode": "Ocean",
            "incoterm": "CIF",
            "origin_country": "Thailand",
            "origin_port": "Bangkok Port (THBKK)",
            "destination_country": "Vietnam",
            "destination_port": "Cai Mep Port (VNCMT)",
            "case_owner": admin_user,
            "department": "Automotive Operations",
            "start_date": add_days(today(), -7),
            "target_completion_date": add_days(today(), 4),
            "opened_date": add_days(today(), -7),
            "expected_close_date": add_days(today(), 4),
            "shipment_status_summary": "Tàu K-Line đang cập phao số 0 Vũng Tàu",
            "document_readiness_pct": 92.0,
            "customs_declaration_no": "105966330612",
            "customs_lane": "Green",
            "customs_cleared": 0,
            "estimated_landed_cost": 1380000.0,
            "actual_landed_cost": 1380000.0,
            "cost_variance_pct": 0.0,
            "costs_finalized": 0,
            "open_exceptions_count": 0,
            "critical_exceptions_count": 0,
            "shipment_tracking": "ST-HONDA-RORO-06",
            "stage_gate_status": "Pending"
        },
        {
            "name": "TC-2026-00007",
            "case_title": "Nhập khẩu linh kiện máy chủ Dell Technologies (Penang - Cát Lái)",
            "trade_type": "Import",
            "status": "In Transit",
            "current_stage": "In Transit",
            "overall_health": "Healthy",
            "priority": "Normal",
            "purchase_order": "PUR-ORD-2026-00006",
            "supplier": "Dell Technologies",
            "company": company,
            "currency": "USD",
            "order_amount": 670500.0,
            "shipping_mode": "Ocean",
            "mode": "Ocean",
            "incoterm": "CIF",
            "origin_country": "Malaysia",
            "origin_port": "Penang Port (MYPEN)",
            "destination_country": "Vietnam",
            "destination_port": "Cat Lai Port, HCMC (VNHCM)",
            "case_owner": admin_user,
            "department": "IT Procurement Logistics",
            "start_date": add_days(today(), -6),
            "target_completion_date": add_days(today(), 5),
            "opened_date": add_days(today(), -6),
            "expected_close_date": add_days(today(), 5),
            "shipment_status_summary": "Container 40ft trên tàu ONE Apus hành trình thuận lợi",
            "document_readiness_pct": 94.0,
            "customs_declaration_no": "105955220311",
            "customs_lane": "Green",
            "customs_cleared": 0,
            "estimated_landed_cost": 712000.0,
            "actual_landed_cost": 712000.0,
            "cost_variance_pct": 0.0,
            "costs_finalized": 0,
            "open_exceptions_count": 0,
            "critical_exceptions_count": 0,
            "shipment_tracking": "ST-DELL-SEA-03",
            "stage_gate_status": "Pending"
        },
        {
            "name": "TC-2026-00008",
            "case_title": "Nhập khẩu bo mạch chủ Lenovo Group (Thâm Quyến - Hải Phòng)",
            "trade_type": "Import",
            "status": "In Transit",
            "current_stage": "In Transit",
            "overall_health": "Healthy",
            "priority": "Normal",
            "purchase_order": "PUR-ORD-2026-00007",
            "supplier": "Lenovo Group",
            "company": company,
            "currency": "USD",
            "order_amount": 716000.0,
            "shipping_mode": "Ocean",
            "mode": "Ocean",
            "incoterm": "FOB",
            "origin_country": "China",
            "origin_port": "Shenzhen Port (CNSZX)",
            "destination_country": "Vietnam",
            "destination_port": "Hai Phong Port (VNHPH)",
            "case_owner": admin_user,
            "department": "IT Procurement Logistics",
            "start_date": add_days(today(), -5),
            "target_completion_date": add_days(today(), 4),
            "opened_date": add_days(today(), -5),
            "expected_close_date": add_days(today(), 4),
            "shipment_status_summary": "Tàu Cosco Pride đang tiếp cận luồng Lạch Huyện",
            "document_readiness_pct": 91.0,
            "customs_declaration_no": "105988129033",
            "customs_lane": "Green",
            "customs_cleared": 0,
            "estimated_landed_cost": 756000.0,
            "actual_landed_cost": 756000.0,
            "cost_variance_pct": 0.0,
            "costs_finalized": 0,
            "open_exceptions_count": 0,
            "critical_exceptions_count": 0,
            "shipment_tracking": "ST-LENOVO-SEA-04",
            "stage_gate_status": "Pending"
        },
        {
            "name": "TC-2026-00009",
            "case_title": "Nhập khẩu linh kiện điện thoại Apple Inc. đường bay (Thâm Quyến - Nội Bài)",
            "trade_type": "Import",
            "status": "In Transit",
            "current_stage": "In Transit",
            "overall_health": "Healthy",
            "priority": "High",
            "purchase_order": "PUR-ORD-2026-00005",
            "supplier": "Apple Inc.",
            "company": company,
            "currency": "USD",
            "order_amount": 677500.0,
            "shipping_mode": "Air",
            "mode": "Air",
            "incoterm": "CIF",
            "origin_country": "China",
            "origin_port": "Shenzhen Baoan (SZX)",
            "destination_country": "Vietnam",
            "destination_port": "Noi Bai International Airport (HAN)",
            "case_owner": admin_user,
            "department": "Air Freight Operations",
            "start_date": add_days(today(), -2),
            "target_completion_date": add_days(today(), 2),
            "opened_date": add_days(today(), -2),
            "expected_close_date": add_days(today(), 2),
            "shipment_status_summary": "Chuyến bay SF Airlines SF-7788 dự kiến hạ cánh hôm nay",
            "document_readiness_pct": 98.0,
            "customs_declaration_no": "105977881234",
            "customs_lane": "Green",
            "customs_cleared": 0,
            "estimated_landed_cost": 698000.0,
            "actual_landed_cost": 698000.0,
            "cost_variance_pct": 0.0,
            "costs_finalized": 0,
            "open_exceptions_count": 0,
            "critical_exceptions_count": 0,
            "shipment_tracking": "ST-APPLE-AIR-02",
            "stage_gate_status": "Pending"
        },
        {
            "name": "TC-2026-00010",
            "case_title": "Nhập khẩu module cảm biến quang học Shanghai - Đà Nẵng (Bão trễ + Thiếu C/O)",
            "trade_type": "Import",
            "status": "In Transit",
            "current_stage": "In Transit",
            "overall_health": "Attention",
            "priority": "Urgent",
            "supplier": "Apple Inc.",
            "company": company,
            "currency": "USD",
            "order_amount": 420000.0,
            "shipping_mode": "Ocean",
            "mode": "Ocean",
            "incoterm": "CIF",
            "origin_country": "China",
            "origin_port": "Shanghai Port (CNSHG)",
            "destination_country": "Vietnam",
            "destination_port": "Tien Sa Port, Da Nang (VNDAD)",
            "case_owner": admin_user,
            "department": "Special Projects Logistics",
            "start_date": add_days(today(), -12),
            "target_completion_date": add_days(today(), 4),
            "opened_date": add_days(today(), -12),
            "expected_close_date": add_days(today(), 4),
            "shipment_status_summary": "Tàu Maersk dính bão trễ +2 ngày, đang thiếu chứng từ C/O Form E gốc",
            "document_readiness_pct": 75.0,
            "missing_critical_docs": "C/O Form E bản gốc chưa về, đang làm thủ tục nợ C/O 30 ngày",
            "customs_declaration_no": "105912345678",
            "customs_lane": "Yellow",
            "customs_cleared": 0,
            "estimated_landed_cost": 445000.0,
            "actual_landed_cost": 480155.0,
            "cost_variance_pct": 7.9,
            "costs_finalized": 0,
            "open_exceptions_count": 2,
            "critical_exceptions_count": 0,
            "shipment_tracking": "ST-IMP-2026-001",
            "stage_gate_status": "Pending"
        }
    ]

    for tc_data in trade_cases_spec:
        tc_name = tc_data["name"]
        # Auto-resolve Purchase Order from linked Shipment Tracking when omitted (e.g. TC-2026-00010 -> ST-IMP-2026-001 -> IMP-2026-001)
        st_link = tc_data.get("shipment_tracking")
        if (not tc_data.get("purchase_order") or not frappe.db.exists("Purchase Order", tc_data["purchase_order"])) and st_link and frappe.db.exists("Shipment Tracking", st_link):
            resolved_po = frappe.db.get_value("Shipment Tracking", st_link, "purchase_order")
            if resolved_po and frappe.db.exists("Purchase Order", resolved_po):
                tc_data["purchase_order"] = resolved_po

        if frappe.db.exists("Trade Case", tc_name):
            doc = frappe.get_doc("Trade Case", tc_name)
            doc.update(tc_data)
            doc.save(ignore_permissions=True)
            print(f"  [Updated] Trade Case {tc_name}")
        else:
            doc = frappe.get_doc({"doctype": "Trade Case", **tc_data})
            doc.insert(ignore_permissions=True)
            print(f"  [Created] Trade Case {tc_name}")

        # Ensure Shipment Tracking points back to Trade Case & link child shipment reference
        if st_link and frappe.db.exists("Shipment Tracking", st_link):
            frappe.db.set_value("Shipment Tracking", st_link, "trade_case", tc_name, update_modified=False)
            st_data = frappe.db.get_value("Shipment Tracking", st_link, ["tracking_number", "carrier", "status", "container_id", "delay_days"], as_dict=True) or {}
            doc.set("shipments", [])
            doc.append("shipments", {
                "doctype": "Trade Case Shipment Reference",
                "shipment_tracking": st_link,
                "tracking_number": st_data.get("tracking_number"),
                "carrier": st_data.get("carrier"),
                "status": st_data.get("status") or "In Transit",
                "container_id": st_data.get("container_id"),
                "delay_days": st_data.get("delay_days") or 0,
                "is_primary": 1
            })
            doc.save(ignore_permissions=True)

        # Create/Update corresponding Trade Cost Sheet WITH real child Trade Cost Item lines
        tcs_name = f"TCS-{tc_name.split('-', 1)[1]}"
        po_val = float(tc_data["order_amount"] or 0.0)
        est_log = round(max(1500.0, float(tc_data["estimated_landed_cost"]) - po_val), 2)
        act_log = round(max(1500.0, float(tc_data["actual_landed_cost"]) - po_val), 2)
        is_finalized = bool(tc_data["costs_finalized"])
        item_status = "Allocated" if is_finalized else "Verified"

        if frappe.db.exists("Trade Cost Sheet", tcs_name):
            tcs_doc = frappe.get_doc("Trade Cost Sheet", tcs_name)
        else:
            tcs_doc = frappe.get_doc({"doctype": "Trade Cost Sheet", "name": tcs_name})

        tcs_doc.update({
            "trade_case": tc_name,
            "case_title": tc_data["case_title"],
            "trade_type": tc_data["trade_type"],
            "status": "Finalized" if is_finalized else "Verified",
            "company": company,
            "posting_date": today(),
            "currency": "USD",
            "conversion_rate": 1.0,
            "allocation_rule": "By Value",
            "total_purchase_value": po_val,
        })

        # Ensure real Trade Cost Item lines exist so TradeCostSheet.validate() computes live totals
        existing_items = getattr(tcs_doc, "cost_items", None) or []
        if not existing_items:
            tcs_doc.set("cost_items", [
                {
                    "cost_type": "Freight",
                    "cost_description": f"International Freight ({tc_data['mode']} {tc_data['origin_port']} -> {tc_data['destination_port']})",
                    "invoice_number": f"FRT-{tc_name}",
                    "currency": "USD",
                    "exchange_rate": 1.0,
                    "estimated_cost": round(est_log * 0.55, 2),
                    "actual_cost": round(act_log * 0.55, 2),
                    "status": item_status,
                },
                {
                    "cost_type": "Duty",
                    "cost_description": "Customs Import Duty & Tariff",
                    "invoice_number": f"DTY-{tc_name}",
                    "currency": "USD",
                    "exchange_rate": 1.0,
                    "estimated_cost": round(est_log * 0.25, 2),
                    "actual_cost": round(act_log * 0.25, 2),
                    "status": item_status,
                },
                {
                    "cost_type": "Port",
                    "cost_description": "THC & Terminal Handling Charges",
                    "invoice_number": f"PRT-{tc_name}",
                    "currency": "USD",
                    "exchange_rate": 1.0,
                    "estimated_cost": round(est_log * 0.12, 2),
                    "actual_cost": round(act_log * 0.12, 2),
                    "status": item_status,
                },
                {
                    "cost_type": "Insurance",
                    "cost_description": "Cargo Marine/Air Insurance Premium",
                    "invoice_number": f"INS-{tc_name}",
                    "currency": "USD",
                    "exchange_rate": 1.0,
                    "estimated_cost": round(est_log - round(est_log * 0.55, 2) - round(est_log * 0.25, 2) - round(est_log * 0.12, 2), 2),
                    "actual_cost": round(act_log - round(act_log * 0.55, 2) - round(act_log * 0.25, 2) - round(act_log * 0.12, 2), 2),
                    "status": item_status,
                },
            ])
        if tcs_doc.is_new():
            tcs_doc.insert(ignore_permissions=True)
            print(f"  [Created] Trade Cost Sheet {tcs_name} ({len(tcs_doc.cost_items)} items)")
        else:
            tcs_doc.save(ignore_permissions=True)
            print(f"  [Updated] Trade Cost Sheet {tcs_name} ({len(tcs_doc.cost_items)} items)")

        # Seed Module 3 (Trade Document), Module 4 (Customs Declaration), Module 6 & Warehouse/LCV
        _seed_modules_for_tc_case(tc_data, tcs_doc, company)

    frappe.db.commit()
    print(">>> ✅ All 10 Trade Cases, Documents, Customs, Cost Items, Warehouse & LCV successfully seeded!")


def _seed_modules_for_tc_case(tc_data: dict, tcs_doc, company: str) -> None:
    """Populate real Modules 3, 4, 6 & ERPNext PR/LCV records for each TC-2026-* case idempotently."""
    tc_name = tc_data["name"]
    try:
        from logistics_wizard.document_engine.api import (
            generate_case_document_checklist,
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
        from logistics_wizard.warehouse_engine.api import (
            record_warehouse_inspection,
            schedule_warehouse_receiving,
        )
        from logistics_wizard.exception_engine.api import (
            create_action_item,
            evaluate_case_exceptions,
            get_case_action_items,
        )
        from logistics_wizard.costing_engine.api import allocate_and_sync_lcv
    except Exception as exc:
        print(f"  [WARN] Engine import skipped for {tc_name}: {exc}")
        return

    # 1. Module 3: Document Checklist & Verification
    generate_case_document_checklist(tc_name)
    docs = get_case_documents_list(tc_name)
    is_done = tc_data["status"] == "Completed"
    missing_co = tc_name in ("TC-2026-00005", "TC-2026-00010")
    early_ready_codes = {"DOC-CI", "DOC-PL", "DOC-BL", "DOC-AWB", "DOC-INS"}
    for d in docs:
        code = d.get("document_code")
        st = d.get("status")
        if is_done:
            if st not in ("N/A", "Verified"):
                u = upload_trade_document_version(tc_name, code, f"/files/{tc_name}_{code}.pdf")
                verify_trade_document(u["name"], action="verify", notes=f"Verified for completed case {tc_name}")
        elif missing_co and code == "DOC-CO":
            if st != "Missing":
                verify_trade_document(d["name"], action="mark_missing", notes="C/O Form bản gốc đang chuyển phát nhanh")
        elif code in early_ready_codes and st not in ("N/A", "Verified"):
            u = upload_trade_document_version(tc_name, code, f"/files/{tc_name}_{code}.pdf")
            verify_trade_document(u["name"], action="verify", notes=f"Pre-arrival verified for {tc_name}")

    # 2. Module 4: Customs Declaration grounded on real PO items
    hs_by_supplier = {
        "Apple Inc.": ("85171300", "Apple Electronics / Smartphone Assembly"),
        "Pandora Jewelry Ltd": ("71131190", "Sterling Silver 925 Pandora Jewelry"),
        "Yamaha Motor Co., Ltd.": ("87115090", "Yamaha CBU Motorcycle >800cc"),
        "Toyota Motor Thailand": ("87042129", "Toyota Hilux / Camry CBU Vehicle"),
        "Honda Vietnam/Thailand Co.": ("87115090", "Honda CBU Motorcycle & Parts"),
        "Dell Technologies": ("84713020", "Dell Commercial Laptops & Monitors"),
        "Lenovo Group": ("84713020", "Lenovo ThinkPad & Workstation Systems"),
    }
    if not get_case_customs_declarations(tc_name):
        hs_code, item_desc = hs_by_supplier.get(tc_data.get("supplier", ""), ("84713020", "Commercial Goods"))
        po_name = tc_data.get("purchase_order")
        cdec_items = []
        if po_name and frappe.db.exists("Purchase Order", po_name):
            po_doc = frappe.get_doc("Purchase Order", po_name)
            for it in (po_doc.items or [])[:2]:
                cdec_items.append({
                    "item_code": it.item_code,
                    "item_name": it.item_name or it.item_code,
                    "qty": float(it.qty or 1),
                    "unit_price": float(it.rate or 100),
                    "import_duty_rate": 5.0,
                    "vat_rate": 10.0,
                })
        if not cdec_items:
            cdec_items = [{
                "item_name": item_desc,
                "qty": 100,
                "unit_price": max(100.0, float(tc_data["order_amount"]) / 100.0),
                "import_duty_rate": 5.0,
                "vat_rate": 10.0,
            }]
        cdec = create_customs_declaration(
            tc_name,
            customs_office_code="02CI",
            co_form="Form D (ATIGA)" if tc_data.get("origin_country") == "Thailand" else "Form E (ACFTA)",
            items=cdec_items,
        )
        if cdec.get("success"):
            for i in range(1, len(cdec_items) + 1):
                propose_hs_code(cdec["name"], i, hs_code, confidence_score=94.5, legal_basis=f"GIR 1 & TT31/2022 ({tc_data.get('supplier')})")
                approve_hs_code(cdec["name"], i, action="approve", notes="Chuyên viên đã đối chiếu invoice & C/O")
            advance_customs_workflow(cdec["name"], "Ready", force_skip_doc_check=True)
            if is_done:
                advance_customs_workflow(
                    cdec["name"],
                    "Declared",
                    declaration_no=tc_data.get("customs_declaration_no"),
                    customs_lane=tc_data.get("customs_lane") or "Green",
                    origin_verified=1,
                    customs_value_verified=1,
                    force_skip_doc_check=True,
                )
                advance_customs_workflow(cdec["name"], "Cleared")

    # 3. Completed Case (TC-2026-00001): Real Warehouse Receipt, ERPNext Purchase Receipt & Landed Cost Voucher
    if is_done:
        wh = schedule_warehouse_receiving(tc_name, "Cat Lai Port - CK", today(), expected_qty=500, space_reserved=1, receiving_team="Đội Nhập Khẩu Cát Lái")
        if wh.get("name"):
            record_warehouse_inspection(wh["name"], received_qty=500, damaged_qty=0, actual_arrival=today())
        po_name = tc_data.get("purchase_order")
        if po_name and frappe.db.exists("Purchase Order", po_name):
            existing_pr = frappe.db.get_value("Purchase Receipt Item", {"purchase_order": po_name, "docstatus": ["!=", 2]}, "parent")
            if not existing_pr:
                try:
                    from erpnext.buying.doctype.purchase_order.purchase_order import make_purchase_receipt
                    pr_doc = make_purchase_receipt(po_name)
                    pr_doc.posting_date = today()
                    pr_doc.insert(ignore_permissions=True)
                    pr_doc.submit()
                    existing_pr = pr_doc.name
                    print(f"    ✓ Created & Submitted ERPNext PR: {existing_pr} for {tc_name}")
                except Exception as exc:
                    print(f"    [WARN] Could not auto-create PR for {tc_name}: {exc}")
            if existing_pr and not getattr(tcs_doc, "landed_cost_voucher", None):
                try:
                    tcs_doc.reload()
                    tcs_doc.set("document_links", [{
                        "document_type": "Purchase Receipt",
                        "document_name": existing_pr,
                        "document_status": "Submitted",
                    }])
                    tcs_doc.save(ignore_permissions=True)
                    lcv_res = allocate_and_sync_lcv(tcs_doc.name, auto_submit=True)
                    if lcv_res.get("success") or lcv_res.get("lcv_name"):
                        frappe.db.set_value("Trade Cost Sheet", tcs_doc.name, {"status": "Finalized", "cost_finalization_status": "FINALIZED"}, update_modified=False)
                        frappe.db.set_value("Trade Case", tc_name, "costs_finalized", 1, update_modified=False)
                        print(f"    ✓ Synced ERPNext Landed Cost Voucher: {lcv_res.get('lcv_name')} for {tc_name}")
                except Exception as exc:
                    print(f"    [WARN] LCV sync skipped for {tc_name}: {exc}")

    # 4. Module 6: Link legacy Exceptions & Run Exception Rules
    if tc_name == "TC-2026-00005" and frappe.db.exists("Shipment Exception", "EXC-TOYOTA-2026-005-01"):
        frappe.db.set_value("Shipment Exception", "EXC-TOYOTA-2026-005-01", "trade_case", tc_name, update_modified=False)
    if tc_name == "TC-2026-00010" and frappe.db.exists("Shipment Exception", "EXC-IMP-2026-001-01"):
        frappe.db.set_value("Shipment Exception", "EXC-IMP-2026-001-01", "trade_case", tc_name, update_modified=False)

    evaluate_case_exceptions(tc_name, auto_create=True)
    if tc_data.get("overall_health") == "Attention" and not get_case_action_items(tc_name):
        create_action_item(
            tc_name,
            f"Theo dõi ETA mới & bổ sung C/O bản gốc cho hồ sơ {tc_name}",
            department="Logistics",
            owner_name="Administrator",
            priority="High",
            due_date=add_days(today(), 2),
        )

if __name__ == "__main__":
    run()
