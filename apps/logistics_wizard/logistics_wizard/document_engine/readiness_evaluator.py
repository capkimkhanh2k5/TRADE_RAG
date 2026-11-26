# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""
readiness_evaluator.py — Document Expiry, Deadline & Readiness Engine
======================================================================
Evaluates Trade Document records for a Trade Case and produces the exact
Section 3.1 payload contract defined in docs/todoTradeCase.md.
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
            return {"doc_urgent_days_before_eta": 3}


CANONICAL_CATEGORIES: Tuple[str, ...] = (
    "Commercial",
    "Transport",
    "Customs",
    "Compliance",
)

STAGE_ORDER: Dict[str, int] = {
    "PO": 0,
    "SO": 0,
    "Booking": 1,
    "Export Port": 2,
    "In Transit": 3,
    "Import Port": 4,
    "Customs": 5,
    "Warehouse": 6,
    "Delivery": 6,
    "Cost Finalization": 7,
    "Closed": 8,
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


def _get_field(doc: Any, key: str, default: Any = None) -> Any:
    if isinstance(doc, dict):
        return doc.get(key, default)
    return getattr(doc, key, default)


def evaluate_document_state(
    doc: Any,
    as_of_date: Optional[Any] = None,
    urgent_window_days: Optional[int] = None,
    current_stage: str = "In Transit",
) -> Dict[str, Any]:
    """
    Evaluate a single Trade Document's effective status, readiness, and urgency alert.
    """
    today_dt = parse_date_safe(as_of_date) or date.today()
    if urgent_window_days is None:
        urgent_window_days = int(get_trade_thresholds().get("doc_urgent_days_before_eta", 3))

    code = str(_get_field(doc, "document_code", "") or "")
    name = str(_get_field(doc, "document_name", "") or code)
    category = str(_get_field(doc, "category", "Commercial") or "Commercial")
    raw_status = str(_get_field(doc, "status", "Required") or "Required")
    is_mandatory = int(_get_field(doc, "is_mandatory", 1) or 0) == 1
    expiry_dt = parse_date_safe(_get_field(doc, "expiry_date"))
    deadline_dt = parse_date_safe(_get_field(doc, "deadline"))
    req_stage = str(_get_field(doc, "required_before_stage", "") or "")

    effective_status = raw_status
    is_expired = False
    is_overdue = False
    urgency_type: Optional[str] = None
    note: Optional[str] = None

    if raw_status == "N/A":
        return {
            "code": code,
            "name": name,
            "category": category,
            "effective_status": "N/A",
            "is_mandatory": is_mandatory,
            "is_applicable": False,
            "is_ready": False,
            "is_expired": False,
            "is_overdue": False,
            "urgency_type": None,
            "deadline": str(deadline_dt) if deadline_dt else None,
            "note": None,
        }

    # 1. Check expiry date
    if expiry_dt and expiry_dt < today_dt:
        effective_status = "Expired"
        is_expired = True
        urgency_type = "critical" if is_mandatory else "warning"
        note = f"Chứng từ đã hết hiệu lực từ ngày {expiry_dt.strftime('%Y-%m-%d')}, cần cấp lại trước khi thông quan."

    is_ready = (effective_status == "Verified") and (not is_expired)

    # 2. Check missing / overdue / imminent deadline for unverified mandatory docs
    if not is_ready and not is_expired:
        if deadline_dt:
            days_left = (deadline_dt - today_dt).days
            if days_left < 0:
                is_overdue = True
                if effective_status == "Required":
                    effective_status = "Missing"
                if is_mandatory:
                    urgency_type = "critical"
                    note = f"Quá hạn nộp {abs(days_left)} ngày (Hạn chót: {deadline_dt.strftime('%Y-%m-%d')})."
            elif days_left <= 1 and is_mandatory:
                urgency_type = "critical"
                note = f"Khẩn cấp: còn {days_left} ngày tới hạn nộp ({deadline_dt.strftime('%Y-%m-%d')})."
            elif days_left <= urgent_window_days and is_mandatory:
                urgency_type = "warning"
                note = f"Sắp tới hạn nộp trong {days_left} ngày ({deadline_dt.strftime('%Y-%m-%d')})."

        # Also flag critical if Trade Case already reached or passed required_before_stage
        if is_mandatory and urgency_type is None and req_stage:
            cur_idx = STAGE_ORDER.get(current_stage, -1)
            req_idx = STAGE_ORDER.get(req_stage, 99)
            if cur_idx >= req_idx >= 0:
                urgency_type = "critical"
                note = f"Bắt buộc hoàn tất trước chặng {req_stage} (hồ sơ đang ở chặng {current_stage})."
            elif effective_status == "Missing":
                urgency_type = "critical"
                note = f"Chứng từ bắt buộc đang bị thiếu ({name})."

    return {
        "code": code,
        "name": name,
        "category": category,
        "effective_status": effective_status,
        "is_mandatory": is_mandatory,
        "is_applicable": True,
        "is_ready": is_ready,
        "is_expired": is_expired,
        "is_overdue": is_overdue,
        "urgency_type": urgency_type,
        "deadline": str(deadline_dt) if deadline_dt else None,
        "note": note,
    }


def compute_document_readiness_payload(
    case_id: str,
    docs: List[Any],
    current_stage: str = "In Transit",
    as_of_date: Optional[Any] = None,
    urgent_window_days: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Aggregate a Trade Case's documents into the exact Section 3.1 contract payload.
    """
    evaluated = [
        evaluate_document_state(
            d,
            as_of_date=as_of_date,
            urgent_window_days=urgent_window_days,
            current_stage=current_stage,
        )
        for d in (docs or [])
    ]

    applicable = [e for e in evaluated if e["is_applicable"]]
    total_count = len(applicable)
    ready_count = sum(1 for e in applicable if e["is_ready"])
    percentage = round((ready_count / total_count) * 100.0, 1) if total_count > 0 else 0.0

    missing_urgent: List[Dict[str, Any]] = []
    for e in applicable:
        if e["urgency_type"] in ("critical", "warning"):
            missing_urgent.append(
                {
                    "code": e["code"],
                    "name": e["name"],
                    "type": e["urgency_type"],
                    "deadline": e["deadline"],
                    "note": e["note"] or f"Chứng từ {e['name']} chưa hoàn tất ({e['effective_status']}).",
                }
            )

    # Sort critical alerts first, then earliest deadline
    missing_urgent.sort(
        key=lambda item: (
            0 if item["type"] == "critical" else 1,
            item["deadline"] or "9999-12-31",
            item["code"],
        )
    )

    categories: List[Dict[str, Any]] = []
    for cat_name in CANONICAL_CATEGORIES:
        cat_items = [e for e in applicable if e["category"] == cat_name]
        cat_total = len(cat_items)
        cat_ready = sum(1 for e in cat_items if e["is_ready"])
        has_critical = any(e["urgency_type"] == "critical" for e in cat_items)

        if cat_total == 0 or cat_ready == cat_total:
            cat_status = "completed"
        elif has_critical:
            cat_status = "danger"
        else:
            cat_status = "warning"

        categories.append(
            {
                "name": cat_name,
                "ready": cat_ready,
                "total": cat_total,
                "status": cat_status,
            }
        )

    return {
        "case_id": case_id,
        "ready_count": ready_count,
        "total_count": total_count,
        "percentage": percentage,
        "current_stage": current_stage,
        "missing_urgent": missing_urgent,
        "categories": categories,
    }


__all__ = [
    "CANONICAL_CATEGORIES",
    "STAGE_ORDER",
    "parse_date_safe",
    "evaluate_document_state",
    "compute_document_readiness_payload",
]
