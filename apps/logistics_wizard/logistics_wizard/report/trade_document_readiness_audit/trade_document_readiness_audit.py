# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""Script Report: Trade Document Readiness Audit (Module 7)."""

from typing import Any, Dict, List, Optional, Tuple

try:
    import frappe
except ImportError:
    frappe = None


def execute(filters: Optional[Dict[str, Any]] = None) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    filters = filters or {}
    columns = [
        {"fieldname": "trade_case", "label": "Hồ sơ XNK (Trade Case)", "fieldtype": "Link", "options": "Trade Case", "width": 160},
        {"fieldname": "trade_type", "label": "Loại hình", "fieldtype": "Data", "width": 90},
        {"fieldname": "applicable_docs", "label": "Chứng từ yêu cầu", "fieldtype": "Int", "width": 120},
        {"fieldname": "verified_docs", "label": "Đã xác minh", "fieldtype": "Int", "width": 110},
        {"fieldname": "missing_expired", "label": "Thiếu / Hết hạn", "fieldtype": "Int", "width": 120},
        {"fieldname": "readiness_pct", "label": "Tỷ lệ sẵn sàng (%)", "fieldtype": "Percent", "width": 130},
        {"fieldname": "critical_missing", "label": "Danh sách chứng từ khẩn thiếu", "fieldtype": "Data", "width": 260},
    ]

    if not (frappe and getattr(frappe, "db", None) and frappe.db.exists("DocType", "Trade Document")):
        return columns, []

    q_filters: Dict[str, Any] = {}
    if filters.get("trade_case"):
        q_filters["trade_case"] = filters["trade_case"]
    if filters.get("trade_type"):
        q_filters["trade_type"] = filters["trade_type"]

    docs = frappe.get_all(
        "Trade Document",
        filters=q_filters,
        fields=["trade_case", "trade_type", "document_code", "document_name", "status", "is_mandatory"],
    ) or []

    grouped: Dict[str, Dict[str, Any]] = {}
    for d in docs:
        cid = str(d.get("trade_case") or "")
        if not cid:
            continue
        b = grouped.setdefault(
            cid,
            {"trade_type": d.get("trade_type") or "Import", "applicable": 0, "verified": 0, "bad": 0, "missing_list": []},
        )
        st = str(d.get("status") or "Required")
        if st == "N/A":
            continue
        b["applicable"] += 1
        if st == "Verified":
            b["verified"] += 1
        elif st in ("Missing", "Expired"):
            b["bad"] += 1
            b["missing_list"].append(f"{d.get('document_code')} ({st})")

    data = []
    for cid, b in sorted(grouped.items()):
        app = b["applicable"]
        ver = b["verified"]
        data.append({
            "trade_case": cid,
            "trade_type": b["trade_type"],
            "applicable_docs": app,
            "verified_docs": ver,
            "missing_expired": b["bad"],
            "readiness_pct": round((ver / app) * 100.0, 1) if app > 0 else 0.0,
            "critical_missing": ", ".join(b["missing_list"]) if b["missing_list"] else "Đầy đủ",
        })
    return columns, data
