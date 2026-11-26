# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""
workflow_engine.py — Customs Workflow State Machine & Section 3.2 Evaluator
============================================================================
Enforces the 6-state clearance lifecycle:
    Preparing -> Ready -> Declared -> Processing -> Cleared / Rejected
and computes the exact Section 3.2 payload contract for Trade Case Overview.
"""

from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple

try:
    from logistics_wizard.master_config import get_trade_thresholds
except ImportError:
    try:
        from ..master_config import get_trade_thresholds
    except ImportError:
        def get_trade_thresholds() -> Dict[str, Any]:
            return {"customs_max_processing_days": 3}


ALLOWED_TRANSITIONS: Dict[str, Tuple[str, ...]] = {
    "Preparing": ("Ready", "Rejected"),
    "Ready": ("Declared", "Preparing", "Rejected"),
    "Declared": ("Processing", "Cleared", "Rejected"),
    "Processing": ("Cleared", "Rejected"),
    "Rejected": ("Preparing",),
    "Cleared": (),
}


def parse_date_safe(val: Any) -> Optional[date]:
    if not val:
        return None
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, date):
        return val
    s = str(val).strip()
    if not s or s.lower() in ("none", "null"):
        return None
    if "T" in s:
        s = s.split("T")[0]
    elif " " in s:
        s = s.split(" ")[0]
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def can_transition(current_status: str, target_status: str) -> bool:
    """Return True if workflow state transition is allowed by the customs state machine."""
    cur = str(current_status or "Preparing").strip()
    tgt = str(target_status or "").strip()
    if cur == tgt:
        return True
    return tgt in ALLOWED_TRANSITIONS.get(cur, ())


def is_declaration_overdue(
    decl: Any,
    as_of_date: Optional[Any] = None,
    max_processing_days: Optional[int] = None,
) -> Tuple[bool, int]:
    """
    Determine if a Declared/Processing declaration has exceeded the customs SLA threshold.
    Returns (is_overdue, elapsed_days).
    """
    status = str(_get(decl, "workflow_status", "Preparing") or "Preparing")
    decl_dt = parse_date_safe(_get(decl, "declaration_date"))
    if not decl_dt:
        return False, 0

    today_dt = parse_date_safe(as_of_date) or date.today()
    clear_dt = parse_date_safe(_get(decl, "clearance_date"))
    end_dt = clear_dt if clear_dt else today_dt
    elapsed = max(0, (end_dt - decl_dt).days)

    if status not in ("Declared", "Processing"):
        return False, elapsed

    if max_processing_days is None:
        max_processing_days = int(get_trade_thresholds().get("customs_max_processing_days", 3))

    return elapsed > max_processing_days, elapsed


def compute_customs_readiness_payload(
    case_id: str,
    declaration: Optional[Any],
    doc_readiness: Optional[Dict[str, Any]] = None,
    as_of_date: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Produce the exact Section 3.2 payload contract from docs/todoTradeCase.md:
    - status, readiness_pct, hs_classification, hs_approval_status,
      origin_verified, customs_value_verified, declaration_status,
      declaration_no, channel, license, inspection, clearance_status
    plus operational metadata for drill-down and SLA monitoring.
    """
    if not declaration:
        return {
            "case_id": case_id,
            "has_declaration": False,
            "declaration_name": None,
            "status": "NOT STARTED",
            "readiness_pct": 0,
            "hs_classification": "Pending HS Classification",
            "hs_approval_status": "Pending",
            "origin_verified": False,
            "customs_value_verified": False,
            "declaration_status": "Not Created (Chưa lập tờ khai)",
            "declaration_no": None,
            "channel": None,
            "license": "N/A",
            "inspection": "Pending",
            "clearance_status": "NOT CLEARED",
            "items_count": 0,
            "hs_approved_count": 0,
            "total_customs_value": 0.0,
            "total_duty_tax": 0.0,
            "processing_days": 0,
            "is_overdue": False,
        }

    wf_status = str(_get(declaration, "workflow_status", "Preparing") or "Preparing")
    lane = str(_get(declaration, "customs_lane", "Not Declared") or "Not Declared")
    decl_no = _get(declaration, "declaration_no") or None
    origin_verified = bool(int(_get(declaration, "origin_verified", 0) or 0))
    value_verified = bool(int(_get(declaration, "customs_value_verified", 0) or 0))
    license_status = str(_get(declaration, "license_status", "N/A") or "N/A")
    inspection_status = str(_get(declaration, "inspection_status", "Pending") or "Pending")
    items: List[Any] = _get(declaration, "items") or []

    total_items = len(items)
    approved_items = [
        it for it in items
        if str(_get(it, "hs_approval_status", "Pending")) == "Approved"
        and str(_get(it, "approved_hs_code", "") or "").strip()
    ]
    proposed_items = [
        it for it in items
        if str(_get(it, "hs_approval_status", "Pending")) == "Proposed"
    ]
    hs_approved_count = len(approved_items)
    all_hs_approved = total_items > 0 and hs_approved_count == total_items

    primary_hs = str(_get(declaration, "primary_hs_code", "") or "").strip()
    if not primary_hs and approved_items:
        primary_hs = str(_get(approved_items[0], "approved_hs_code", "") or "").strip()
    if not primary_hs and items:
        primary_hs = str(_get(items[0], "suggested_hs_code", "") or "").strip()

    if all_hs_approved:
        hs_approval_status = "Approved by Customs Specialist"
    elif hs_approved_count > 0:
        hs_approval_status = f"Partially Approved ({hs_approved_count}/{total_items})"
    elif proposed_items:
        hs_approval_status = f"Proposed - Awaiting Specialist Approval ({len(proposed_items)}/{total_items})"
    else:
        hs_approval_status = "Pending HS Classification"

    # Weighted readiness percentage (0 - 100)
    score = 0
    # 1. HS Approval (30 pts)
    if total_items > 0:
        score += int(round(30 * (hs_approved_count / total_items)))
    # 2. Trade Document Readiness (20 pts)
    if doc_readiness and doc_readiness.get("total_count", 0) > 0:
        doc_pct = float(doc_readiness.get("percentage", 0) or 0)
        score += int(round(20 * min(100.0, max(0.0, doc_pct)) / 100.0))
    elif wf_status in ("Ready", "Declared", "Processing", "Cleared"):
        score += 20
    # 3. Origin & Customs Value verification (15 pts)
    if origin_verified:
        score += 8
    if value_verified:
        score += 7
    # 4. License & Inspection compliance (10 pts)
    if license_status in ("N/A", "Approved"):
        score += 5
    if inspection_status in ("Not Required", "Passed"):
        score += 5
    # 5. Declaration & Clearance progress (25 pts)
    if wf_status == "Cleared":
        score = 100
    elif wf_status in ("Declared", "Processing"):
        score += 15
    elif wf_status == "Ready":
        score += 5

    readiness_pct = min(100, max(0, int(score)))

    # Human-readable declaration_status & status banner
    if wf_status == "Cleared":
        status_banner = "CLEARED"
        clearance_status = "CLEARED"
        decl_status_label = f"Cleared ({lane} Channel)"
    elif wf_status == "Rejected":
        status_banner = "REJECTED"
        clearance_status = "REJECTED"
        reason = _get(declaration, "rejection_reason") or "Cần bổ sung hồ sơ"
        decl_status_label = f"Rejected ({reason})"
    elif wf_status == "Processing" and lane == "Red":
        status_banner = "PHYSICAL INSPECTION (RED CHANNEL)"
        clearance_status = "NOT CLEARED"
        decl_status_label = f"Processing - Red Channel ({decl_no or 'Pending No'})"
    elif wf_status in ("Declared", "Processing"):
        status_banner = wf_status.upper()
        clearance_status = "NOT CLEARED"
        decl_status_label = f"{wf_status} - {lane} Channel ({decl_no or 'Pending No'})"
    elif wf_status == "Ready":
        status_banner = "READY"
        clearance_status = "NOT CLEARED"
        decl_status_label = "Ready to Transmit VNACCS"
    else:
        status_banner = "PREPARING"
        clearance_status = "NOT CLEARED"
        if not all_hs_approved:
            decl_status_label = "Preparing (Chờ phê duyệt mã HS)"
        elif doc_readiness and doc_readiness.get("missing_urgent"):
            first_doc = doc_readiness["missing_urgent"][0].get("name", "chứng từ")
            decl_status_label = f"Pending (Chờ {first_doc})"
        else:
            decl_status_label = "Preparing Declaration"

    overdue_flag, elapsed_days = is_declaration_overdue(declaration, as_of_date=as_of_date)

    return {
        "case_id": case_id,
        "has_declaration": True,
        "declaration_name": _get(declaration, "name"),
        "status": status_banner,
        "workflow_status": wf_status,
        "readiness_pct": readiness_pct,
        "hs_classification": primary_hs or "Pending",
        "hs_approval_status": hs_approval_status,
        "origin_verified": origin_verified,
        "customs_value_verified": value_verified,
        "declaration_status": decl_status_label,
        "declaration_no": decl_no,
        "channel": None if lane == "Not Declared" else lane,
        "license": license_status,
        "inspection": inspection_status,
        "clearance_status": clearance_status,
        "customs_office_code": _get(declaration, "customs_office_code"),
        "customs_office_name": _get(declaration, "customs_office_name"),
        "items_count": total_items,
        "hs_approved_count": hs_approved_count,
        "total_customs_value": float(_get(declaration, "total_customs_value", 0) or 0),
        "total_duty_tax": float(_get(declaration, "total_duty_tax", 0) or 0),
        "processing_days": elapsed_days,
        "is_overdue": overdue_flag,
    }


__all__ = [
    "ALLOWED_TRANSITIONS",
    "parse_date_safe",
    "can_transition",
    "is_declaration_overdue",
    "compute_customs_readiness_payload",
]
