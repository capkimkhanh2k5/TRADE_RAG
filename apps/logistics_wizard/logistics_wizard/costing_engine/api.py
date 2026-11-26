# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""
costing_engine.api — Public API Facade & Data Contract Implementation
======================================================================
Module 5: Trade Cost & Landed Cost Management (Milestone 5)

Implements the public API facade conforming 100% to todoTradeCase.md Section 3.3:
- get_case_cost_summary(case_id: str) -> Dict[str, Any]
- get_case_export_profitability(case_id: str) -> Dict[str, Any]
- audit_case_costs(case_id: str) -> Dict[str, Any]
- allocate_and_sync_lcv(cost_sheet_name: str, auto_submit: bool = False) -> Dict[str, Any]
- format_case_cost_summary(cost_sheet: Any) -> Dict[str, Any]
"""

import sys
from typing import Dict, Any, List, Optional, Tuple, Union

try:
    import frappe
    from frappe import _
except ImportError:
    frappe = None
    _ = lambda x: x

from logistics_wizard.costing_engine.allocation_engine import (
    CostAllocationEngine,
    allocate_costs,
    extract_receipt_items,
)
from logistics_wizard.costing_engine.lcv_integrator import (
    LCVIntegrator,
    create_or_update_lcv,
)
from logistics_wizard.costing_engine.export_tracker import (
    ExportTracker,
    calculate_export_profitability,
    get_export_profitability_summary,
)
from logistics_wizard.costing_engine.audit_engine import (
    CostAuditEngine,
    audit_cost_sheet,
)

# Registry for testing/offline mock injection
_MOCK_COST_SHEET_REGISTRY: Dict[str, Any] = {}


def register_mock_cost_sheet(case_id: str, cost_sheet_data: Any) -> None:
    """Registers a mock or test cost sheet for offline tests."""
    cid = str(case_id).strip()
    _MOCK_COST_SHEET_REGISTRY[cid] = cost_sheet_data
    # Also index by cost_sheet name if present
    sheet_name = (
        cost_sheet_data.get("name")
        if isinstance(cost_sheet_data, dict)
        else getattr(cost_sheet_data, "name", None)
    )
    if sheet_name:
        _MOCK_COST_SHEET_REGISTRY[str(sheet_name).strip()] = cost_sheet_data


def clear_mock_cost_sheet_registry() -> None:
    """Clears the mock registry."""
    _MOCK_COST_SHEET_REGISTRY.clear()


def calculate_variance(estimated: float, actual: float) -> Tuple[float, float]:
    """
    Calculates variance amount (Actual - Estimated) and variance percentage (1 decimal place).
    Matches todoTradeCase.md Section 3.3 (e.g. 1350 / 17000 = 7.9%) and TradeCostSheet controller.
    """
    amt = round(float(actual or 0.0) - float(estimated or 0.0), 2)
    est_val = float(estimated or 0.0)
    act_val = float(actual or 0.0)
    if est_val > 0.0:
        pct = round((amt / est_val) * 100.0, 1)
    elif est_val == 0.0:
        pct = 100.0 if act_val > 0.0 else 0.0
    else:
        pct = round((amt / abs(est_val)) * 100.0, 1)
    return amt, pct


def rollup_cost_sheet_status(
    items: List[Dict[str, Any]],
    docstatus: int = 0,
    sheet_status: str = "",
) -> Dict[str, Any]:
    """
    Rolls up status metrics across active cost items.
    State machine: DRAFT -> IN PROGRESS -> ALMOST READY -> ALLOCATED -> FINALIZED.
    """
    active_items = [it for it in items if it.get("status") != "Cancelled"]
    total = len(active_items)

    invoices_received = sum(1 for it in active_items if bool(str(it.get("invoice_number") or "").strip()))
    costs_verified = sum(1 for it in active_items if it.get("status") in ("Verified", "Allocated"))
    costs_allocated = sum(1 for it in active_items if it.get("status") == "Allocated")

    if total == 0:
        status = "DRAFT" if docstatus == 0 else "FINALIZED"
    elif docstatus == 1:
        status = "FINALIZED"
    elif costs_allocated == total and total > 0:
        if sheet_status in ("Finalized", "Closed", "Submitted"):
            status = "FINALIZED"
        else:
            status = "ALLOCATED"
    elif costs_verified == total and total > 0:
        status = "ALMOST READY"
    elif invoices_received > 0 or costs_verified > 0 or costs_allocated > 0:
        status = "IN PROGRESS"
    else:
        status = "DRAFT"

    return {
        "invoices_received": invoices_received,
        "invoices_total": total,
        "costs_verified": costs_verified,
        "costs_allocated": costs_allocated,
        "cost_finalization_status": status,
    }


def format_case_cost_summary(cost_sheet: Any) -> Dict[str, Any]:
    """
    Formats a Trade Cost Sheet (Document or dict) into the exact Section 3.3 payload contract.
    """
    if isinstance(cost_sheet, dict):
        raw_items = cost_sheet.get("cost_items", []) or []
        purchase_val = float(
            cost_sheet.get("purchase_value", cost_sheet.get("total_purchase_value", 0.0)) or 0.0
        )
        currency = cost_sheet.get("currency", "USD") or "USD"
        docstatus = int(cost_sheet.get("docstatus", 0) or 0)
        sheet_status = str(cost_sheet.get("status", "") or "")
        sheet_rate = float(cost_sheet.get("conversion_rate", 1.0) or 1.0)
    else:
        raw_items = getattr(cost_sheet, "cost_items", []) or []
        purchase_val = float(
            getattr(cost_sheet, "purchase_value", getattr(cost_sheet, "total_purchase_value", 0.0)) or 0.0
        )
        currency = getattr(cost_sheet, "currency", "USD") or "USD"
        docstatus = int(getattr(cost_sheet, "docstatus", 0) or 0)
        sheet_status = str(getattr(cost_sheet, "status", "") or "")
        sheet_rate = float(getattr(cost_sheet, "conversion_rate", 1.0) or 1.0)

    if sheet_rate <= 0.0:
        sheet_rate = 1.0

    active_items = []
    for it in raw_items:
        st = it.get("status") if isinstance(it, dict) else getattr(it, "status", None)
        if st != "Cancelled":
            active_items.append(it)

    total_est = 0.0
    total_act = 0.0
    breakdown_map: Dict[str, float] = {}

    for it in active_items:
        if isinstance(it, dict):
            rate = float(it.get("exchange_rate", 0.0) or 0.0) or sheet_rate
            base_est = it.get("base_estimated_cost", it.get("estimated_amount_base", None))
            if base_est is None:
                raw_est = float(it.get("estimated_cost", it.get("estimated_amount", 0.0)) or 0.0)
                base_est = round(raw_est * rate, 2)
            else:
                base_est = float(base_est or 0.0)

            base_act = it.get("base_actual_cost", it.get("actual_amount_base", None))
            if base_act is None:
                raw_act = float(it.get("actual_cost", it.get("actual_amount", 0.0)) or 0.0)
                base_act = round(raw_act * rate, 2)
            else:
                base_act = float(base_act or 0.0)

            ctype = it.get("cost_type") or "Other"
        else:
            rate = float(getattr(it, "exchange_rate", 0.0) or 0.0) or sheet_rate
            base_est = getattr(it, "base_estimated_cost", getattr(it, "estimated_amount_base", None))
            if base_est is None:
                raw_est = float(getattr(it, "estimated_cost", getattr(it, "estimated_amount", 0.0)) or 0.0)
                base_est = round(raw_est * rate, 2)
            else:
                base_est = float(base_est or 0.0)

            base_act = getattr(it, "base_actual_cost", getattr(it, "actual_amount_base", None))
            if base_act is None:
                raw_act = float(getattr(it, "actual_cost", getattr(it, "actual_amount", 0.0)) or 0.0)
                base_act = round(raw_act * rate, 2)
            else:
                base_act = float(base_act or 0.0)

            ctype = getattr(it, "cost_type", None) or "Other"

        total_est += base_est
        total_act += base_act
        breakdown_map[ctype] = breakdown_map.get(ctype, 0.0) + base_act

    total_est = round(total_est, 2)
    total_act = round(total_act, 2)
    var_amt, var_pct = calculate_variance(total_est, total_act)

    dict_items = [
        it if isinstance(it, dict) else {
            "status": getattr(it, "status", None),
            "invoice_number": getattr(it, "invoice_number", None),
        }
        for it in active_items
    ]
    rollups = rollup_cost_sheet_status(dict_items, docstatus=docstatus, sheet_status=sheet_status)

    breakdown = [{"label": k, "amount": round(v, 2)} for k, v in sorted(breakdown_map.items())]

    return {
        "purchase_value": round(purchase_val, 2),
        "estimated_cost": total_est,
        "actual_cost": total_act,
        "variance_amount": var_amt,
        "variance_pct": var_pct,
        "actual_landed_cost": round(purchase_val + total_act, 2),
        "currency": currency,
        "breakdown": breakdown,
        "invoices_received": rollups["invoices_received"],
        "invoices_total": rollups["invoices_total"],
        "costs_verified": rollups["costs_verified"],
        "costs_allocated": rollups["costs_allocated"],
        "cost_finalization_status": rollups["cost_finalization_status"],
    }


def _frappe_whitelist():
    """Conditional decorator for frappe.whitelist."""
    if frappe and hasattr(frappe, "whitelist"):
        return frappe.whitelist(allow_guest=True)
    return lambda f: f


@_frappe_whitelist()
def get_case_cost_summary(case_id: str) -> Dict[str, Any]:
    """
    Returns the exact Section 3.3 payload contract for Trade Case Overview.
    """
    cid = str(case_id or "").strip()
    cost_sheet: Optional[Any] = None

    # 1. Check offline mock registry
    if cid in _MOCK_COST_SHEET_REGISTRY:
        cost_sheet = _MOCK_COST_SHEET_REGISTRY[cid]

    # 2. Check Frappe DB
    if cost_sheet is None and frappe and hasattr(frappe, "db") and hasattr(frappe.db, "get_value"):
        try:
            sheet_name = frappe.db.get_value(
                "Trade Cost Sheet",
                {"trade_case": cid, "docstatus": ["!=", 2]},
                "name",
            )
            if sheet_name:
                cost_sheet = frappe.get_doc("Trade Cost Sheet", sheet_name)
        except Exception:
            pass

    # 3. Fallback if no cost sheet exists for the case
    if cost_sheet is None:
        purchase_val = 0.0
        currency = "USD"
        if frappe and hasattr(frappe, "db") and hasattr(frappe.db, "get_value"):
            try:
                case_info = frappe.db.get_value(
                    "Trade Case",
                    cid,
                    ["order_amount", "currency"],
                    as_dict=True,
                )
                if case_info:
                    purchase_val = float(case_info.get("order_amount") or 0.0)
                    currency = case_info.get("currency") or "USD"
            except Exception:
                pass

        return {
            "purchase_value": round(purchase_val, 2),
            "estimated_cost": 0.0,
            "actual_cost": 0.0,
            "variance_amount": 0.0,
            "variance_pct": 0.0,
            "actual_landed_cost": round(purchase_val, 2),
            "currency": currency,
            "breakdown": [],
            "invoices_received": 0,
            "invoices_total": 0,
            "costs_verified": 0,
            "costs_allocated": 0,
            "cost_finalization_status": "DRAFT",
        }

    return format_case_cost_summary(cost_sheet)


@_frappe_whitelist()
def get_case_export_profitability(case_id: str) -> Dict[str, Any]:
    """Returns export profitability breakdown and margins for an Export Trade Case."""
    cid = str(case_id or "").strip()
    if cid in _MOCK_COST_SHEET_REGISTRY:
        return calculate_export_profitability(_MOCK_COST_SHEET_REGISTRY[cid])
    return get_export_profitability_summary(cid)


@_frappe_whitelist()
def audit_case_costs(case_id: str) -> Dict[str, Any]:
    """Runs full audit verification on the active Cost Sheet of a Trade Case."""
    cid = str(case_id or "").strip()
    cost_sheet = None

    if cid in _MOCK_COST_SHEET_REGISTRY:
        cost_sheet = _MOCK_COST_SHEET_REGISTRY[cid]
    elif frappe and hasattr(frappe, "db") and hasattr(frappe.db, "get_value"):
        try:
            sheet_name = frappe.db.get_value(
                "Trade Cost Sheet",
                {"trade_case": cid, "docstatus": ["!=", 2]},
                "name",
            )
            if sheet_name:
                cost_sheet = frappe.get_doc("Trade Cost Sheet", sheet_name)
        except Exception:
            pass

    if not cost_sheet:
        return {
            "passed": True,
            "errors": [],
            "warnings": [f"No active Trade Cost Sheet found for Trade Case {cid}"],
            "anomalies": [],
        }

    trade_case = None
    if frappe and hasattr(frappe, "get_doc"):
        try:
            trade_case = frappe.get_doc("Trade Case", cid)
        except Exception:
            trade_case = None

    if not trade_case:
        tc_id = (
            cost_sheet.get("trade_case")
            if isinstance(cost_sheet, dict)
            else getattr(cost_sheet, "trade_case", None)
        ) or cid
        trade_case = {"name": tc_id}

    return audit_cost_sheet(cost_sheet, trade_case=trade_case)


@_frappe_whitelist()
def allocate_and_sync_lcv(
    cost_sheet_name: str,
    auto_submit: bool = False,
    items: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Allocates import landed costs per item using Custom Cost Allocation Engine
    and synchronizes into ERPNext Landed Cost Voucher (LCV).
    Supports both live Frappe documents and registered mock cost sheets.
    """
    sheet_key = str(cost_sheet_name or "").strip()
    cost_sheet = None

    if sheet_key in _MOCK_COST_SHEET_REGISTRY:
        cost_sheet = _MOCK_COST_SHEET_REGISTRY[sheet_key]
    elif frappe and hasattr(frappe, "get_doc"):
        try:
            cost_sheet = frappe.get_doc("Trade Cost Sheet", sheet_key)
        except Exception:
            cost_sheet = None

    if cost_sheet is None:
        return {"success": False, "error": f"Trade Cost Sheet '{sheet_key}' not found"}

    # Prefer delegating to TradeCostSheet.sync_to_lcv if available on controller
    if hasattr(cost_sheet, "sync_to_lcv") and callable(cost_sheet.sync_to_lcv):
        return cost_sheet.sync_to_lcv(auto_submit=auto_submit, items=items)

    rule = (
        cost_sheet.get("allocation_rule")
        if isinstance(cost_sheet, dict)
        else getattr(cost_sheet, "allocation_rule", None)
    ) or "By Value"

    allocated_items = allocate_costs(cost_sheet, rule=rule, items=items)
    raw_res = create_or_update_lcv(cost_sheet, allocated_items, auto_submit=auto_submit)
    if isinstance(raw_res, str):
        res: Dict[str, Any] = {"success": bool(raw_res), "lcv_name": raw_res}
    elif isinstance(raw_res, dict):
        res = dict(raw_res)
        res.setdefault("success", bool(res.get("lcv_name") or res.get("name")))
    else:
        res = {"success": False, "lcv_name": None}
    res["allocated_items"] = allocated_items
    return res


def _is_frappe_cost_db_ready() -> bool:
    if not (frappe and getattr(frappe, "db", None)):
        return False
    exists_fn = getattr(frappe.db, "exists", None)
    if not callable(exists_fn):
        return False
    try:
        return bool(exists_fn("DocType", "Trade Cost Sheet"))
    except Exception:
        return False


def _extract_case_allocation_items(case_id: str, cost_sheet: Any = None) -> List[Dict[str, Any]]:
    """Extract real line items for allocation preview from linked Purchase Receipt / PO / SO."""
    if not _is_frappe_cost_db_ready():
        return []
    items: List[Dict[str, Any]] = []
    try:
        # 1. Try linked Purchase Receipt via Trade Warehouse Receipt or PO
        pr_name = None
        if frappe.db.exists("DocType", "Trade Warehouse Receipt"):
            pr_name = frappe.db.get_value("Trade Warehouse Receipt", {"trade_case": case_id}, "purchase_receipt")
        tc = frappe.db.get_value(
            "Trade Case", case_id, ["purchase_order", "sales_order", "trade_type"], as_dict=True
        ) or {}
        if pr_name and frappe.db.exists("Purchase Receipt", pr_name):
            pr_doc = frappe.get_doc("Purchase Receipt", pr_name)
            for it in (getattr(pr_doc, "items", None) or []):
                items.append({
                    "item_code": getattr(it, "item_code", "") or "",
                    "name": getattr(it, "item_name", "") or getattr(it, "item_code", ""),
                    "qty": float(getattr(it, "qty", 1) or 1),
                    "unit_price": float(getattr(it, "rate", 0) or 0),
                    "weight": float(getattr(it, "weight_per_unit", 0) or 1.0),
                    "volume": 0.01,
                })
        elif tc.get("purchase_order") and frappe.db.exists("Purchase Order", tc["purchase_order"]):
            po_doc = frappe.get_doc("Purchase Order", tc["purchase_order"])
            for it in (getattr(po_doc, "items", None) or []):
                items.append({
                    "item_code": getattr(it, "item_code", "") or "",
                    "name": getattr(it, "item_name", "") or getattr(it, "item_code", ""),
                    "qty": float(getattr(it, "qty", 1) or 1),
                    "unit_price": float(getattr(it, "rate", 0) or 0),
                    "weight": float(getattr(it, "weight_per_unit", 0) or 1.0),
                    "volume": 0.01,
                })
        elif tc.get("sales_order") and frappe.db.exists("Sales Order", tc["sales_order"]):
            so_doc = frappe.get_doc("Sales Order", tc["sales_order"])
            for it in (getattr(so_doc, "items", None) or []):
                items.append({
                    "item_code": getattr(it, "item_code", "") or "",
                    "name": getattr(it, "item_name", "") or getattr(it, "item_code", ""),
                    "qty": float(getattr(it, "qty", 1) or 1),
                    "unit_price": float(getattr(it, "rate", 0) or 0),
                    "weight": float(getattr(it, "weight_per_unit", 0) or 1.0),
                    "volume": 0.01,
                })
    except Exception:
        pass
    return items


def _format_audit_cards(audit_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Convert raw CostAuditEngine output into structured UI audit cards."""
    errors = audit_result.get("errors") or []
    warnings = audit_result.get("warnings") or []
    anomalies = audit_result.get("anomalies") or []

    dup_issues = [e for e in (errors + warnings + anomalies) if "duplicat" in str(e).lower() or "trùng" in str(e).lower()]
    missing_issues = [e for e in (errors + warnings + anomalies) if "missing" in str(e).lower() or "thiếu" in str(e).lower() or "no active" in str(e).lower()]
    assoc_issues = [e for e in (errors + warnings + anomalies) if "case" in str(e).lower() or "mismatch" in str(e).lower() or "wrong" in str(e).lower()]

    def _card(title: str, issues: List[Any], ok_desc: str) -> Dict[str, Any]:
        if not issues:
            return {
                "title": title,
                "status": "Hợp lệ",
                "status_class": "delay-tag-ontime",
                "border": "#10b981",
                "desc": ok_desc,
            }
        is_err = any(i in errors for i in issues)
        return {
            "title": title,
            "status": "Cần xử lý" if is_err else "Cần rà soát",
            "status_class": "delay-tag-positive",
            "border": "#dc2626" if is_err else "#d97706",
            "desc": "; ".join(str(i) for i in issues[:3]),
        }

    return [
        _card(
            "Trùng Lặp Hóa Đơn (Duplicate Check)",
            dup_issues,
            "Không phát hiện hóa đơn trùng lặp số chứng từ hoặc nhà cung cấp.",
        ),
        _card(
            "Chi Phí Trọng Yếu (Missing Cost Check)",
            missing_issues,
            "Đã đầy đủ các khoản chi phí trọng yếu cho hồ sơ XNK.",
        ),
        _card(
            "Gán Đúng Vụ Việc (Association Check)",
            assoc_issues,
            "Tất cả chứng từ chi phí đều tham chiếu đúng Trade Case.",
        ),
    ]


@_frappe_whitelist()
def add_cost_item_to_case(
    case_id: str,
    cost_type: str,
    estimated_cost: float = 0.0,
    actual_cost: float = 0.0,
    service_provider: Optional[str] = None,
    invoice_number: Optional[str] = None,
    cost_description: Optional[str] = None,
    status: str = "Draft",
    currency: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Append a Trade Cost Item line to a Trade Case's active Trade Cost Sheet
    (auto-creating the Trade Cost Sheet if none exists yet).
    Powers the 'Add Cost Invoice' Quick Action on Trade Case Overview & Cost Dashboard.
    """
    cid = str(case_id or "").strip()
    ctype = str(cost_type or "").strip()
    if not cid or not ctype:
        return {"success": False, "error": "case_id và cost_type là bắt buộc."}

    est_val = float(estimated_cost or 0.0)
    act_val = float(actual_cost or 0.0)
    row_payload = {
        "cost_type": ctype,
        "cost_description": cost_description or ctype,
        "service_provider": service_provider or None,
        "invoice_number": invoice_number or "",
        "currency": currency or "USD",
        "exchange_rate": 1.0,
        "estimated_cost": est_val,
        "actual_cost": act_val,
        "estimated_amount": est_val,
        "actual_amount": act_val,
        "status": status or "Draft",
    }

    if _is_frappe_cost_db_ready():
        sheet_name = frappe.db.get_value(
            "Trade Cost Sheet", {"trade_case": cid, "docstatus": ["!=", 2]}, "name"
        )
        if sheet_name:
            doc = frappe.get_doc("Trade Cost Sheet", sheet_name)
        else:
            tc = (
                frappe.db.get_value(
                    "Trade Case",
                    cid,
                    ["trade_type", "order_amount", "currency", "company"],
                    as_dict=True,
                )
                or {}
            )
            doc = frappe.get_doc(
                {
                    "doctype": "Trade Cost Sheet",
                    "trade_case": cid,
                    "trade_type": tc.get("trade_type") or "Import",
                    "company": tc.get("company"),
                    "currency": currency or tc.get("currency") or "USD",
                    "total_purchase_value": float(tc.get("order_amount") or 0.0),
                    "allocation_rule": "By Value",
                    "status": "Draft",
                    "cost_items": [],
                }
            )
        # Only pass service_provider if it exists as Supplier to avoid LinkValidationError
        if row_payload["service_provider"] and not frappe.db.exists("Supplier", row_payload["service_provider"]):
            row_payload["service_provider"] = None
        doc.append("cost_items", row_payload)
        if sheet_name:
            doc.save(ignore_permissions=True)
        else:
            doc.insert(ignore_permissions=True)
        summary = format_case_cost_summary(doc)
        return {
            "success": True,
            "cost_sheet_name": doc.name,
            "case_id": cid,
            "items_count": len(doc.cost_items or []),
            "summary": summary,
        }

    # Offline / test registry mode
    sheet = _MOCK_COST_SHEET_REGISTRY.get(cid)
    if sheet is None:
        sheet = {
            "name": f"TCS-MOCK-{cid}",
            "trade_case": cid,
            "trade_type": "Export" if cid.upper().startswith("EXP") else "Import",
            "currency": currency or "USD",
            "purchase_value": 0.0,
            "status": "Draft",
            "docstatus": 0,
            "cost_items": [],
        }
    if isinstance(sheet, dict):
        sheet.setdefault("cost_items", []).append(row_payload)
        register_mock_cost_sheet(cid, sheet)
    summary = format_case_cost_summary(sheet)
    return {
        "success": True,
        "cost_sheet_name": sheet.get("name") if isinstance(sheet, dict) else getattr(sheet, "name", None),
        "case_id": cid,
        "items_count": len(sheet.get("cost_items", [])) if isinstance(sheet, dict) else len(getattr(sheet, "cost_items", []) or []),
        "summary": summary,
    }


@_frappe_whitelist()
def get_cost_dashboard_data(
    case_id: Optional[str] = None,
    trade_type_filter: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Live unified backend API for Trade Cost & Landed Cost Dashboard (Module 5).
    Replaces hardcoded JS mock arrays with live Trade Cost Sheet, ERPNext PO/PR/SO items,
    CostAuditEngine checks, Export Profitability, and LCV linkage.
    """
    available_cases: List[Dict[str, Any]] = []
    use_db = _is_frappe_cost_db_ready()

    if use_db and frappe.db.exists("DocType", "Trade Case"):
        filters: Dict[str, Any] = {}
        tf = str(trade_type_filter or "").strip().lower()
        if tf == "import":
            filters["trade_type"] = "Import"
        elif tf == "export":
            filters["trade_type"] = "Export"
        rows = frappe.get_all(
            "Trade Case",
            filters=filters,
            fields=["name", "case_title", "trade_type", "supplier", "customer", "order_amount", "currency", "status"],
            order_by="modified desc",
            limit=50,
        ) or []
        for r in rows:
            party = r.get("supplier") if r.get("trade_type") == "Import" else (r.get("customer") or r.get("supplier") or "N/A")
            available_cases.append({
                "case_id": r["name"],
                "trade_type": r.get("trade_type") or "Import",
                "party": party or "N/A",
                "label": f"{r['name']} — {r.get('case_title') or party}",
            })
    else:
        for cid_key, sheet in _MOCK_COST_SHEET_REGISTRY.items():
            tc_key = sheet.get("trade_case") if isinstance(sheet, dict) else getattr(sheet, "trade_case", cid_key)
            if tc_key and not any(c["case_id"] == tc_key for c in available_cases):
                tt = (sheet.get("trade_type") if isinstance(sheet, dict) else getattr(sheet, "trade_type", "Import")) or "Import"
                available_cases.append({
                    "case_id": tc_key,
                    "trade_type": tt,
                    "party": "Registered Case",
                    "label": f"{tc_key} ({tt})",
                })

    selected_id = str(case_id or "").strip()
    if not selected_id and available_cases:
        selected_id = available_cases[0]["case_id"]

    cost_sheet = None
    cost_sheet_name = None
    party = "N/A"
    trade_type = "Import"
    lcv_id = None
    sheet_status = "Draft"

    if selected_id in _MOCK_COST_SHEET_REGISTRY:
        cost_sheet = _MOCK_COST_SHEET_REGISTRY[selected_id]
        cost_sheet_name = cost_sheet.get("name") if isinstance(cost_sheet, dict) else getattr(cost_sheet, "name", None)
        trade_type = (cost_sheet.get("trade_type") if isinstance(cost_sheet, dict) else getattr(cost_sheet, "trade_type", "Import")) or "Import"
        lcv_id = cost_sheet.get("landed_cost_voucher") if isinstance(cost_sheet, dict) else getattr(cost_sheet, "landed_cost_voucher", None)
        sheet_status = (cost_sheet.get("status") if isinstance(cost_sheet, dict) else getattr(cost_sheet, "status", "Draft")) or "Draft"
    elif use_db and selected_id:
        if frappe.db.exists("Trade Case", selected_id):
            tc = frappe.db.get_value(
                "Trade Case", selected_id, ["trade_type", "supplier", "customer", "case_title"], as_dict=True
            ) or {}
            trade_type = tc.get("trade_type") or "Import"
            party = tc.get("supplier") if trade_type == "Import" else (tc.get("customer") or tc.get("supplier") or tc.get("case_title") or "N/A")
        sheet_name = frappe.db.get_value(
            "Trade Cost Sheet", {"trade_case": selected_id, "docstatus": ["!=", 2]}, "name"
        )
        if sheet_name:
            cost_sheet = frappe.get_doc("Trade Cost Sheet", sheet_name)
            cost_sheet_name = cost_sheet.name
            trade_type = getattr(cost_sheet, "trade_type", None) or trade_type
            lcv_id = getattr(cost_sheet, "landed_cost_voucher", None)
            sheet_status = getattr(cost_sheet, "status", None) or "Draft"

    summary = format_case_cost_summary(cost_sheet) if cost_sheet is not None else get_case_cost_summary(selected_id)

    raw_items = (
        (cost_sheet.get("cost_items") if isinstance(cost_sheet, dict) else getattr(cost_sheet, "cost_items", None))
        if cost_sheet is not None
        else []
    ) or []
    cost_items_ui: List[Dict[str, Any]] = []
    for it in raw_items:
        is_d = isinstance(it, dict)
        ctype = (it.get("cost_type") if is_d else getattr(it, "cost_type", "Other")) or "Other"
        desc = (it.get("cost_description") if is_d else getattr(it, "cost_description", "")) or ctype
        prov = (it.get("service_provider") if is_d else getattr(it, "service_provider", "")) or "Chưa gán NCC"
        inv = (it.get("invoice_number") if is_d else getattr(it, "invoice_number", "")) or "Chưa có HĐ"
        est = float((it.get("base_estimated_cost") or it.get("estimated_cost") or it.get("estimated_amount") or 0) if is_d else (getattr(it, "base_estimated_cost", 0) or getattr(it, "estimated_cost", 0) or getattr(it, "estimated_amount", 0) or 0))
        act = float((it.get("base_actual_cost") or it.get("actual_cost") or it.get("actual_amount") or 0) if is_d else (getattr(it, "base_actual_cost", 0) or getattr(it, "actual_cost", 0) or getattr(it, "actual_amount", 0) or 0))
        st = (it.get("status") if is_d else getattr(it, "status", "Draft")) or "Draft"
        cost_items_ui.append({
            "type": f"{ctype} — {desc}" if desc and desc != ctype else ctype,
            "cost_type": ctype,
            "supplier": prov,
            "inv_no": inv,
            "est": round(est, 2),
            "act": round(act, 2),
            "status": st,
        })

    audit_raw = audit_case_costs(selected_id) if selected_id else {"passed": True, "errors": [], "warnings": [], "anomalies": []}
    audit_checks = _format_audit_cards(audit_raw)
    alloc_items = _extract_case_allocation_items(selected_id, cost_sheet)

    export_prof = None
    if str(trade_type).lower() == "export" and selected_id:
        try:
            export_prof = get_case_export_profitability(selected_id)
        except Exception:
            export_prof = None

    fin_st = summary.get("cost_finalization_status", "DRAFT")
    status_class = "badge-delivered" if fin_st in ("ALLOCATED", "FINALIZED") else "badge-in-transit"

    return {
        "success": True,
        "case_id": selected_id,
        "has_cost_sheet": cost_sheet is not None,
        "cost_sheet_name": cost_sheet_name,
        "trade_type": trade_type,
        "case_type": str(trade_type).lower(),
        "party": party,
        "status": fin_st,
        "sheet_status": sheet_status,
        "status_class": status_class,
        "lcv_id": lcv_id,
        "currency": summary.get("currency", "USD"),
        "po_value": summary["purchase_value"],
        "estimated_cost": summary["estimated_cost"],
        "actual_cost": summary["actual_cost"],
        "variance_amount": summary["variance_amount"],
        "variance_pct": summary["variance_pct"],
        "actual_landed_cost": summary["actual_landed_cost"],
        "summary": summary,
        "cost_items": cost_items_ui,
        "items_to_allocate": alloc_items,
        "audit_checks": audit_checks,
        "export_profitability": export_prof,
        "available_cases": available_cases,
    }
