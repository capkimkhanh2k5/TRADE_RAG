# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""Script Report: Shipment Delay and Carrier Performance (Module 7)."""

from typing import Any, Dict, List, Optional, Tuple

try:
    import frappe
except ImportError:
    frappe = None


def execute(filters: Optional[Dict[str, Any]] = None) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    filters = filters or {}
    columns = [
        {"fieldname": "carrier", "label": "Hãng vận tải (Carrier)", "fieldtype": "Data", "width": 180},
        {"fieldname": "shipping_method", "label": "Phương thức", "fieldtype": "Data", "width": 110},
        {"fieldname": "flow_type", "label": "Luồng XNK", "fieldtype": "Data", "width": 100},
        {"fieldname": "total_shipments", "label": "Tổng vận đơn", "fieldtype": "Int", "width": 110},
        {"fieldname": "delayed_count", "label": "Số lô trễ", "fieldtype": "Int", "width": 100},
        {"fieldname": "stale_count", "label": "Mất tín hiệu", "fieldtype": "Int", "width": 110},
        {"fieldname": "avg_delay_days", "label": "Trễ TB (ngày)", "fieldtype": "Float", "width": 120},
        {"fieldname": "on_time_pct", "label": "Đúng hạn (%)", "fieldtype": "Percent", "width": 120},
    ]

    if not (frappe and getattr(frappe, "db", None) and frappe.db.exists("DocType", "Shipment Tracking")):
        return columns, []

    q_filters: Dict[str, Any] = {}
    if filters.get("flow_type"):
        q_filters["flow_type"] = filters["flow_type"]
    if filters.get("carrier"):
        q_filters["carrier"] = filters["carrier"]

    rows = frappe.get_all(
        "Shipment Tracking",
        filters=q_filters,
        fields=["carrier", "shipping_method", "flow_type", "delay_days", "is_stale"],
    ) or []

    grouped: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
    for r in rows:
        key = (
            str(r.get("carrier") or "Unknown Carrier"),
            str(r.get("shipping_method") or "Ocean"),
            str(r.get("flow_type") or "Import"),
        )
        b = grouped.setdefault(key, {"total": 0, "delayed": 0, "stale": 0, "delay_sum": 0})
        b["total"] += 1
        d = int(r.get("delay_days") or 0)
        if d > 0:
            b["delayed"] += 1
            b["delay_sum"] += d
        if int(r.get("is_stale") or 0) == 1:
            b["stale"] += 1

    data = []
    for (carrier, mode, flow), b in sorted(grouped.items(), key=lambda kv: kv[1]["total"], reverse=True):
        total = b["total"]
        delayed = b["delayed"]
        data.append({
            "carrier": carrier,
            "shipping_method": mode,
            "flow_type": flow,
            "total_shipments": total,
            "delayed_count": delayed,
            "stale_count": b["stale"],
            "avg_delay_days": round(b["delay_sum"] / delayed, 1) if delayed > 0 else 0.0,
            "on_time_pct": round(((total - delayed) / total) * 100.0, 1) if total > 0 else 100.0,
        })
    return columns, data
