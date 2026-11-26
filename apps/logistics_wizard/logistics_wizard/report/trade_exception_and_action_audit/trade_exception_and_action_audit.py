# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""Script Report: Trade Exception and Action Audit (Module 7)."""

from typing import Any, Dict, List, Optional, Tuple

try:
    import frappe
except ImportError:
    frappe = None


def execute(filters: Optional[Dict[str, Any]] = None) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    filters = filters or {}
    columns = [
        {"fieldname": "name", "label": "Mã sự cố", "fieldtype": "Link", "options": "Shipment Exception", "width": 140},
        {"fieldname": "trade_case", "label": "Trade Case", "fieldtype": "Link", "options": "Trade Case", "width": 140},
        {"fieldname": "source_module", "label": "Phân hệ", "fieldtype": "Data", "width": 100},
        {"fieldname": "rule_code", "label": "Mã quy tắc", "fieldtype": "Data", "width": 160},
        {"fieldname": "exception_type", "label": "Loại sự cố", "fieldtype": "Data", "width": 150},
        {"fieldname": "severity", "label": "Mức độ", "fieldtype": "Data", "width": 90},
        {"fieldname": "status", "label": "Trạng thái", "fieldtype": "Data", "width": 110},
        {"fieldname": "department", "label": "Phòng ban", "fieldtype": "Data", "width": 110},
        {"fieldname": "assigned_to", "label": "Người xử lý", "fieldtype": "Data", "width": 140},
        {"fieldname": "escalation_level", "label": "Escalation", "fieldtype": "Int", "width": 90},
        {"fieldname": "due_date", "label": "Hạn xử lý", "fieldtype": "Date", "width": 110},
        {"fieldname": "resolved_at", "label": "Thời điểm đóng", "fieldtype": "Datetime", "width": 150},
    ]

    if not (frappe and getattr(frappe, "db", None) and frappe.db.exists("DocType", "Shipment Exception")):
        return columns, []

    q_filters: Dict[str, Any] = {}
    if filters.get("trade_case"):
        q_filters["trade_case"] = filters["trade_case"]
    if filters.get("severity"):
        q_filters["severity"] = filters["severity"]
    if filters.get("status"):
        q_filters["status"] = filters["status"]

    rows = frappe.get_all(
        "Shipment Exception",
        filters=q_filters,
        fields=[
            "name", "trade_case", "source_module", "rule_code", "exception_type",
            "severity", "status", "department", "assigned_to", "escalation_level",
            "due_date", "resolved_at",
        ],
        order_by="raised_at desc",
    ) or []

    return columns, [dict(r) if isinstance(r, dict) else r.as_dict() for r in rows]
