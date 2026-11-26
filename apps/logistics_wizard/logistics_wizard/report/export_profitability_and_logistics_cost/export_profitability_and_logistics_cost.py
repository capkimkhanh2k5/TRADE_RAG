# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""Script Report: Export Profitability and Logistics Cost (Module 7)."""

from typing import Any, Dict, List, Optional, Tuple

try:
    import frappe
except ImportError:
    frappe = None


def execute(filters: Optional[Dict[str, Any]] = None) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    filters = filters or {}
    columns = [
        {"fieldname": "name", "label": "Trade Cost Sheet", "fieldtype": "Link", "options": "Trade Cost Sheet", "width": 150},
        {"fieldname": "trade_case", "label": "Export Case", "fieldtype": "Link", "options": "Trade Case", "width": 140},
        {"fieldname": "export_revenue", "label": "Doanh thu XK", "fieldtype": "Currency", "width": 130},
        {"fieldname": "export_cogs", "label": "Giá vốn (COGS)", "fieldtype": "Currency", "width": 120},
        {"fieldname": "export_logistics_cost", "label": "Chi phí Logistics XK", "fieldtype": "Currency", "width": 140},
        {"fieldname": "export_gross_margin", "label": "Lợi nhuận gộp", "fieldtype": "Currency", "width": 130},
        {"fieldname": "export_net_profit", "label": "Lợi nhuận thuần", "fieldtype": "Currency", "width": 130},
        {"fieldname": "export_net_margin_pct", "label": "Biên LN thuần (%)", "fieldtype": "Percent", "width": 120},
        {"fieldname": "variance_pct", "label": "Độ lệch CP (%)", "fieldtype": "Percent", "width": 110},
    ]

    if not (frappe and getattr(frappe, "db", None) and frappe.db.exists("DocType", "Trade Cost Sheet")):
        return columns, []

    q_filters: Dict[str, Any] = {"trade_type": "Export", "docstatus": ["!=", 2]}
    if filters.get("trade_case"):
        q_filters["trade_case"] = filters["trade_case"]

    rows = frappe.get_all(
        "Trade Cost Sheet",
        filters=q_filters,
        fields=[
            "name", "trade_case", "export_revenue", "export_cogs",
            "export_logistics_cost", "total_actual_cost", "export_gross_margin",
            "export_net_profit", "export_net_margin_pct", "variance_pct",
        ],
        order_by="modified desc",
    ) or []

    data = []
    for r in rows:
        rev = float(r.get("export_revenue") or 0)
        cogs = float(r.get("export_cogs") or 0)
        log_c = float(r.get("export_logistics_cost") or r.get("total_actual_cost") or 0)
        gross = (rev - cogs) if rev > 0 else float(r.get("export_gross_margin") or 0)
        net = (gross - log_c) if rev > 0 else float(r.get("export_net_profit") or (gross - log_c))
        net_pct = round((net / rev) * 100.0, 1) if rev > 0 else float(r.get("export_net_margin_pct") or 0.0)
        data.append({
            "name": r["name"],
            "trade_case": r.get("trade_case"),
            "export_revenue": round(rev, 2),
            "export_cogs": round(cogs, 2),
            "export_logistics_cost": round(log_c, 2),
            "export_gross_margin": round(gross, 2),
            "export_net_profit": round(net, 2),
            "export_net_margin_pct": round(net_pct, 1),
            "variance_pct": float(r.get("variance_pct") or 0.0),
        })
    return columns, data
