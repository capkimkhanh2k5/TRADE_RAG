# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""Script Report: Import Landed Cost Variance (Module 7)."""

from typing import Any, Dict, List, Optional, Tuple

try:
    import frappe
except ImportError:
    frappe = None


def execute(filters: Optional[Dict[str, Any]] = None) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    filters = filters or {}
    columns = [
        {"fieldname": "name", "label": "Trade Cost Sheet", "fieldtype": "Link", "options": "Trade Cost Sheet", "width": 150},
        {"fieldname": "trade_case", "label": "Trade Case", "fieldtype": "Link", "options": "Trade Case", "width": 140},
        {"fieldname": "total_purchase_value", "label": "Trị giá hàng (PO)", "fieldtype": "Currency", "width": 130},
        {"fieldname": "total_estimated_cost", "label": "Dự toán (Est)", "fieldtype": "Currency", "width": 120},
        {"fieldname": "total_actual_cost", "label": "Thực tế (Actual)", "fieldtype": "Currency", "width": 120},
        {"fieldname": "variance_amount", "label": "Chênh lệch ($)", "fieldtype": "Currency", "width": 120},
        {"fieldname": "variance_pct", "label": "Chênh lệch (%)", "fieldtype": "Percent", "width": 110},
        {"fieldname": "actual_landed_cost", "label": "Tổng Landed Cost", "fieldtype": "Currency", "width": 140},
        {"fieldname": "landed_cost_voucher", "label": "LCV ERPNext", "fieldtype": "Link", "options": "Landed Cost Voucher", "width": 140},
        {"fieldname": "cost_finalization_status", "label": "Trạng thái chốt", "fieldtype": "Data", "width": 120},
    ]

    if not (frappe and getattr(frappe, "db", None) and frappe.db.exists("DocType", "Trade Cost Sheet")):
        return columns, []

    q_filters: Dict[str, Any] = {"trade_type": "Import", "docstatus": ["!=", 2]}
    if filters.get("trade_case"):
        q_filters["trade_case"] = filters["trade_case"]

    rows = frappe.get_all(
        "Trade Cost Sheet",
        filters=q_filters,
        fields=[
            "name", "trade_case", "total_purchase_value", "total_estimated_cost",
            "total_actual_cost", "variance_amount", "variance_pct",
            "actual_landed_cost", "landed_cost_voucher", "cost_finalization_status",
        ],
        order_by="modified desc",
    ) or []

    return columns, [dict(r) if isinstance(r, dict) else r.as_dict() for r in rows]
