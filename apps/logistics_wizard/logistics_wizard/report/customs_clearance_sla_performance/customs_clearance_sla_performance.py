# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""Script Report: Customs Clearance SLA Performance (Module 7)."""

from typing import Any, Dict, List, Optional, Tuple

try:
    import frappe
except ImportError:
    frappe = None


def execute(filters: Optional[Dict[str, Any]] = None) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    filters = filters or {}
    columns = [
        {"fieldname": "name", "label": "Mã bản ghi", "fieldtype": "Link", "options": "Customs Declaration", "width": 150},
        {"fieldname": "declaration_no", "label": "Số tờ khai VNACCS", "fieldtype": "Data", "width": 140},
        {"fieldname": "trade_case", "label": "Trade Case", "fieldtype": "Link", "options": "Trade Case", "width": 140},
        {"fieldname": "trade_type", "label": "Loại hình", "fieldtype": "Data", "width": 90},
        {"fieldname": "customs_office_code", "label": "Chi cục HQ", "fieldtype": "Data", "width": 100},
        {"fieldname": "workflow_status", "label": "Trạng thái", "fieldtype": "Data", "width": 110},
        {"fieldname": "customs_lane", "label": "Phân luồng", "fieldtype": "Data", "width": 100},
        {"fieldname": "primary_hs_code", "label": "Mã HS chính", "fieldtype": "Data", "width": 110},
        {"fieldname": "total_duty_tax", "label": "Tổng thuế", "fieldtype": "Currency", "width": 120},
        {"fieldname": "processing_days", "label": "Ngày xử lý", "fieldtype": "Int", "width": 100},
        {"fieldname": "sla_status", "label": "Đánh giá SLA", "fieldtype": "Data", "width": 110},
    ]

    if not (frappe and getattr(frappe, "db", None) and frappe.db.exists("DocType", "Customs Declaration")):
        return columns, []

    q_filters: Dict[str, Any] = {}
    if filters.get("trade_type"):
        q_filters["trade_type"] = filters["trade_type"]
    if filters.get("customs_lane"):
        q_filters["customs_lane"] = filters["customs_lane"]

    rows = frappe.get_all(
        "Customs Declaration",
        filters=q_filters,
        fields=[
            "name", "declaration_no", "trade_case", "trade_type", "customs_office_code",
            "workflow_status", "customs_lane", "primary_hs_code", "total_duty_tax", "processing_days",
        ],
        order_by="modified desc",
    ) or []

    data = []
    for r in rows:
        days = int(r.get("processing_days") or 0)
        wf = str(r.get("workflow_status") or "")
        overdue = (wf in ("Declared", "Processing") and days > 3) or wf == "Rejected"
        data.append({
            "name": r["name"],
            "declaration_no": r.get("declaration_no") or "Pending",
            "trade_case": r.get("trade_case"),
            "trade_type": r.get("trade_type"),
            "customs_office_code": r.get("customs_office_code") or "-",
            "workflow_status": wf,
            "customs_lane": r.get("customs_lane") or "Not Declared",
            "primary_hs_code": r.get("primary_hs_code") or "Pending",
            "total_duty_tax": float(r.get("total_duty_tax") or 0.0),
            "processing_days": days,
            "sla_status": "Overdue / Hold" if overdue else "On SLA",
        })
    return columns, data
