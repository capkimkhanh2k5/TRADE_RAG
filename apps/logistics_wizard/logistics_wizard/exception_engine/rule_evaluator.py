# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""
rule_evaluator.py — 8 Automated Exception Rules & Trade Case Health Engine
===========================================================================
Implements the 8 business risk rules defined in docsTitleProject/ToDo.md Section 4.6:
1. RULE_01_ETA_DELAY            — ETA/ETD delay exceeds threshold
2. RULE_02_MISSING_DOCUMENT     — Critical / overdue / expired mandatory Trade Document
3. RULE_03_CUSTOMS_OVERDUE      — Customs processing overdue, Red Channel, or Rejected
4. RULE_04_COST_VARIANCE        — Landed / Export cost variance exceeds warning/critical %
5. RULE_05_STALE_TRACKING       — Shipment tracking feed stale beyond threshold hours
6. RULE_06_DEMURRAGE_RISK       — Container arrived at port > free days without clearance/pickup
7. RULE_07_COST_NOT_FINALIZED   — Cargo received/delivered but Landed Cost not finalized
8. RULE_08_WAREHOUSE_ISSUE      — Warehouse discrepancy (missing/damaged) or warehouse not ready
"""

from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional

try:
    from logistics_wizard.master_config import get_trade_thresholds
except ImportError:
    try:
        from ..master_config import get_trade_thresholds
    except ImportError:
        def get_trade_thresholds() -> Dict[str, Any]:
            return {
                "delay_warning_days": 1,
                "delay_critical_days": 3,
                "cost_variance_warn_pct": 5.0,
                "cost_variance_critical_pct": 15.0,
                "customs_max_processing_days": 3,
                "tracking_stale_hours": 48,
                "demurrage_free_days": 5,
            }


EXCEPTION_RULES_CATALOG: List[Dict[str, str]] = [
    {"code": "RULE_01_ETA_DELAY", "type": "ETA Delay", "department": "Logistics", "source_module": "Shipment"},
    {"code": "RULE_02_MISSING_DOCUMENT", "type": "Missing Document", "department": "Purchasing", "source_module": "Document"},
    {"code": "RULE_03_CUSTOMS_OVERDUE", "type": "Customs Overdue", "department": "Customs", "source_module": "Customs"},
    {"code": "RULE_04_COST_VARIANCE", "type": "Cost Variance", "department": "Accounting", "source_module": "Costing"},
    {"code": "RULE_05_STALE_TRACKING", "type": "Stale Tracking", "department": "Logistics", "source_module": "Shipment"},
    {"code": "RULE_06_DEMURRAGE_RISK", "type": "Demurrage/Detention Risk", "department": "Logistics", "source_module": "Shipment"},
    {"code": "RULE_07_COST_NOT_FINALIZED", "type": "Cost Not Finalized", "department": "Accounting", "source_module": "Costing"},
    {"code": "RULE_08_WAREHOUSE_ISSUE", "type": "Warehouse Discrepancy", "department": "Warehouse", "source_module": "Warehouse"},
]


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


def evaluate_8_exception_rules(
    case_id: str,
    signals: Dict[str, Any],
    as_of_date: Optional[Any] = None,
    thresholds: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Evaluate all 8 risk rules against aggregated cross-module signals for a Trade Case.
    Returns a list of triggered exception candidate payloads ready for idempotent creation.
    """
    today_dt = parse_date_safe(as_of_date) or date.today()
    cfg = dict(get_trade_thresholds())
    if thresholds:
        cfg.update(thresholds)

    delay_warn = int(cfg.get("delay_warning_days", 1))
    delay_crit = int(cfg.get("delay_critical_days", 3))
    cost_warn = float(cfg.get("cost_variance_warn_pct", 5.0))
    cost_crit = float(cfg.get("cost_variance_critical_pct", 15.0))
    customs_max_days = int(cfg.get("customs_max_processing_days", 3))
    stale_hours_limit = float(cfg.get("tracking_stale_hours", 48))
    demurrage_free_days = int(cfg.get("demurrage_free_days", 5))

    shipment = signals.get("shipment") or {}
    docs = signals.get("documents") or {}
    customs = signals.get("customs") or {}
    cost = signals.get("cost") or {}
    warehouse = signals.get("warehouse") or {}
    current_stage = str(signals.get("current_stage") or "In Transit")

    triggered: List[Dict[str, Any]] = []

    # RULE 1: ETA / ETD Delay
    delay_days = int(shipment.get("delay_days") or 0)
    if delay_days >= delay_warn:
        sev = "Critical" if delay_days >= delay_crit else "High"
        triggered.append(
            {
                "rule_code": "RULE_01_ETA_DELAY",
                "exception_type": "ETA Delay",
                "severity": sev,
                "title": f"Lô hàng trễ lịch trình +{delay_days} ngày",
                "description": f"Vận đơn {shipment.get('shipment_id') or case_id} bị trễ +{delay_days} ngày so với ETA gốc.",
                "department": "Logistics",
                "source_module": "Shipment",
                "delay_days": delay_days,
                "shipment_tracking": shipment.get("shipment_id"),
                "due_date": str(today_dt + timedelta(days=1 if sev == "Critical" else 2)),
            }
        )

    # RULE 2: Missing / Expired Critical Document
    missing_urgent = docs.get("missing_urgent") or []
    critical_docs = [m for m in missing_urgent if m.get("type") == "critical"]
    if critical_docs:
        doc_names = ", ".join(m.get("name", m.get("code", "")) for m in critical_docs[:3])
        sev = "Critical" if current_stage in ("Import Port", "Customs") else "High"
        triggered.append(
            {
                "rule_code": "RULE_02_MISSING_DOCUMENT",
                "exception_type": "Missing Document",
                "severity": sev,
                "title": f"Thiếu/hết hạn {len(critical_docs)} chứng từ khẩn cấp ({doc_names})",
                "description": "; ".join(
                    f"{m.get('name', m.get('code'))}: {m.get('note', 'Thiếu chứng từ')}"
                    for m in critical_docs[:5]
                ),
                "department": "Purchasing",
                "source_module": "Document",
                "due_date": str(critical_docs[0].get("deadline") or (today_dt + timedelta(days=1))),
            }
        )

    # RULE 3: Customs Overdue / Red Channel / Rejected
    c_status = str(customs.get("workflow_status") or customs.get("status") or "")
    c_lane = str(customs.get("channel") or "")
    c_days = int(customs.get("processing_days") or 0)
    c_overdue = bool(customs.get("is_overdue")) or (
        c_status in ("Declared", "Processing") and c_days > customs_max_days
    )
    if c_lane == "Red" and customs.get("clearance_status") != "CLEARED":
        triggered.append(
            {
                "rule_code": "RULE_03_CUSTOMS_OVERDUE",
                "exception_type": "Customs Hold",
                "severity": "Critical",
                "title": f"Tờ khai phân Luồng Đỏ — Kiểm hóa thực tế ({customs.get('declaration_no') or case_id})",
                "description": f"Tờ khai {customs.get('declaration_no') or ''} bị phân Luồng Đỏ, đã xử lý {c_days} ngày, cần ưu tiên kiểm hóa tránh rớt tàu/lưu bãi.",
                "department": "Customs",
                "source_module": "Customs",
                "due_date": str(today_dt + timedelta(days=1)),
            }
        )
    elif c_status == "Rejected" or customs.get("clearance_status") == "REJECTED":
        triggered.append(
            {
                "rule_code": "RULE_03_CUSTOMS_OVERDUE",
                "exception_type": "Customs Hold",
                "severity": "Critical",
                "title": f"Tờ khai Hải quan bị từ chối ({customs.get('declaration_no') or case_id})",
                "description": f"Trạng thái tờ khai: {customs.get('declaration_status') or 'Rejected'}.",
                "department": "Customs",
                "source_module": "Customs",
                "due_date": str(today_dt + timedelta(days=1)),
            }
        )
    elif c_overdue:
        triggered.append(
            {
                "rule_code": "RULE_03_CUSTOMS_OVERDUE",
                "exception_type": "Customs Overdue",
                "severity": "High",
                "title": f"Hải quan xử lý quá hạn SLA ({c_days} ngày > {customs_max_days} ngày)",
                "description": f"Tờ khai {customs.get('declaration_no') or case_id} đang ở trạng thái {c_status} quá {c_days} ngày.",
                "department": "Customs",
                "source_module": "Customs",
                "due_date": str(today_dt + timedelta(days=1)),
            }
        )

    # RULE 4: Cost Variance Exceeds Threshold
    var_pct = float(cost.get("variance_pct") or 0.0)
    if var_pct >= cost_warn:
        sev = "Critical" if var_pct >= cost_crit else "Warning"
        triggered.append(
            {
                "rule_code": "RULE_04_COST_VARIANCE",
                "exception_type": "Cost Variance",
                "severity": sev,
                "title": f"Chi phí thực tế vượt dự toán +{var_pct:.1f}%",
                "description": f"Thực tế: {cost.get('actual_cost', 0)} vs Dự toán: {cost.get('estimated_cost', 0)} (Vượt +{var_pct:.1f}%).",
                "department": "Accounting",
                "source_module": "Costing",
                "due_date": str(today_dt + timedelta(days=2)),
            }
        )

    # RULE 5: Stale Tracking Feed
    stale_hours = float(shipment.get("stale_hours") or 0.0)
    ship_status = str(shipment.get("status") or "")
    if (
        (bool(shipment.get("is_stale")) or stale_hours >= stale_hours_limit)
        and ship_status not in ("Delivered", "Completed", "Closed")
    ):
        triggered.append(
            {
                "rule_code": "RULE_05_STALE_TRACKING",
                "exception_type": "Stale Tracking",
                "severity": "Warning",
                "title": f"Mất tín hiệu cập nhật vận đơn ({int(stale_hours)}h chưa sync)",
                "description": f"Vận đơn {shipment.get('shipment_id') or case_id} không nhận được tín hiệu mới vượt ngưỡng {int(stale_hours_limit)} giờ.",
                "department": "Logistics",
                "source_module": "Shipment",
                "shipment_tracking": shipment.get("shipment_id"),
                "due_date": str(today_dt + timedelta(days=1)),
            }
        )

    # RULE 6: Demurrage / Detention Risk
    days_at_port = int(shipment.get("days_at_port") or 0)
    if days_at_port <= 0 and ship_status in ("Arrived Destination Port", "Import Port", "At Destination Port"):
        arr_dt = parse_date_safe(shipment.get("ata") or shipment.get("current_eta"))
        if arr_dt and today_dt > arr_dt:
            days_at_port = (today_dt - arr_dt).days
    if (
        days_at_port >= demurrage_free_days
        and customs.get("clearance_status") != "CLEARED"
        and warehouse.get("receiving_status") != "COMPLETED"
    ):
        triggered.append(
            {
                "rule_code": "RULE_06_DEMURRAGE_RISK",
                "exception_type": "Demurrage/Detention Risk",
                "severity": "Critical" if days_at_port >= demurrage_free_days + 2 else "High",
                "title": f"Nguy cơ phát sinh phí lưu bãi/lưu cont (DEM/DET — {days_at_port} ngày tại cảng)",
                "description": f"Hàng đã lưu cảng {days_at_port} ngày (vượt mốc miễn lưu {demurrage_free_days} ngày) nhưng chưa thông quan/lấy hàng.",
                "department": "Logistics",
                "source_module": "Shipment",
                "shipment_tracking": shipment.get("shipment_id"),
                "due_date": str(today_dt),
            }
        )

    # RULE 7: Cost Not Finalized After Receiving / Delivery
    cost_fin = str(cost.get("cost_finalization_status") or "").upper()
    cargo_received = (
        warehouse.get("receiving_status") in ("COMPLETED", "RECEIVED")
        or ship_status in ("Delivered", "Completed")
        or current_stage in ("Cost Finalization",)
    )
    if cargo_received and cost.get("invoices_total", 0) > 0 and cost_fin not in ("ALLOCATED", "FINALIZED", "COMPLETED"):
        triggered.append(
            {
                "rule_code": "RULE_07_COST_NOT_FINALIZED",
                "exception_type": "Cost Not Finalized",
                "severity": "Warning",
                "title": "Hàng đã nhập kho nhưng chưa hoàn tất phân bổ Landed Cost (LCV)",
                "description": f"Trạng thái chốt chi phí hiện tại: {cost_fin or 'IN PROGRESS'}. Cần đối soát hóa đơn và đồng bộ Landed Cost Voucher.",
                "department": "Accounting",
                "source_module": "Costing",
                "due_date": str(today_dt + timedelta(days=3)),
            }
        )

    # RULE 8: Warehouse Discrepancy OR Warehouse Not Ready on Arrival
    if warehouse.get("discrepancy_alert"):
        sev = "Critical" if (float(warehouse.get("damaged_qty") or 0) > 0 or not warehouse.get("container_seal_intact", True)) else "High"
        triggered.append(
            {
                "rule_code": "RULE_08_WAREHOUSE_DISCREPANCY",
                "exception_type": "Warehouse Discrepancy",
                "severity": sev,
                "title": f"Bất thường nhập kho: {warehouse.get('discrepancy_details') or 'Chênh lệch số lượng/hư hỏng'}",
                "description": warehouse.get("discrepancy_details") or "Số lượng thực nhận không khớp chứng từ.",
                "department": "Warehouse",
                "source_module": "Warehouse",
                "due_date": str(today_dt + timedelta(days=1)),
            }
        )
    else:
        arrived_or_imminent = ship_status in ("Arrived Destination Port", "Import Port", "Customs Clearance")
        if not arrived_or_imminent:
            eta_dt = parse_date_safe(shipment.get("current_eta") or warehouse.get("expected_arrival"))
            if eta_dt and 0 <= (eta_dt - today_dt).days <= 2:
                arrived_or_imminent = True
        if arrived_or_imminent and (
            warehouse.get("receiving_status", "NOT READY") == "NOT READY"
            and not warehouse.get("space_reserved")
        ):
            triggered.append(
                {
                    "rule_code": "RULE_08_WAREHOUSE_NOT_READY",
                    "exception_type": "Warehouse Not Ready",
                    "severity": "High",
                    "title": "Hàng đã cập cảng/sắp về kho nhưng kho chưa bố trí mặt bằng tiếp nhận",
                    "description": f"Trạng thái kho đang là {warehouse.get('receiving_status', 'NOT READY')} và chưa đặt chỗ mặt bằng (space_reserved=False).",
                    "department": "Warehouse",
                    "source_module": "Warehouse",
                    "due_date": str(today_dt + timedelta(days=1)),
                }
            )

    return triggered


def compute_trade_case_health(
    signals: Optional[Dict[str, Any]] = None,
    open_exceptions: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Deterministically compute Trade Case overall_health (Healthy / Attention / Critical)
    purely from live child module signals and open exceptions (never manual input).
    """
    sigs = signals or {}
    excs = open_exceptions or []
    shipment = sigs.get("shipment") or {}
    docs = sigs.get("documents") or {}
    customs = sigs.get("customs") or {}
    cost = sigs.get("cost") or {}
    warehouse = sigs.get("warehouse") or {}

    critical_reasons: List[str] = []
    attention_reasons: List[str] = []

    crit_excs = [e for e in excs if str(e.get("severity", "")).lower() == "critical"]
    high_warn_excs = [e for e in excs if str(e.get("severity", "")).lower() in ("high", "warning")]

    if crit_excs:
        critical_reasons.append(f"Có {len(crit_excs)} sự cố mức Critical đang mở")
    if str(customs.get("channel") or "") == "Red" and customs.get("clearance_status") != "CLEARED":
        critical_reasons.append("Tờ khai Hải quan phân Luồng Đỏ (Kiểm hóa 100%)")
    if customs.get("clearance_status") == "REJECTED":
        critical_reasons.append("Tờ khai Hải quan bị từ chối")
    if warehouse.get("discrepancy_alert"):
        critical_reasons.append("Phát hiện chênh lệch/hư hỏng hàng hóa khi nhập kho")
    delay_days = int(shipment.get("delay_days") or 0)
    if delay_days >= 3:
        critical_reasons.append(f"Lô hàng trễ nghiêm trọng +{delay_days} ngày")
    elif delay_days >= 1:
        attention_reasons.append(f"ETA trễ +{delay_days} ngày")

    var_pct = float(cost.get("variance_pct") or 0.0)
    if var_pct >= 15.0:
        critical_reasons.append(f"Chi phí vượt dự toán nghiêm trọng +{var_pct:.1f}%")
    elif var_pct >= 5.0:
        attention_reasons.append(f"Chi phí vượt dự toán +{var_pct:.1f}%")

    missing_urgent = docs.get("missing_urgent") or []
    if missing_urgent:
        attention_reasons.append(f"Còn {len(missing_urgent)} chứng từ khẩn/sắp hạn chưa hoàn tất")
    if customs.get("is_overdue"):
        attention_reasons.append("Hải quan xử lý quá hạn SLA")
    if high_warn_excs:
        attention_reasons.append(f"Còn {len(high_warn_excs)} sự cố mức High/Warning đang xử lý")

    if critical_reasons:
        status = "Critical"
        status_class = "danger"
        reasons = critical_reasons + attention_reasons
    elif attention_reasons:
        status = "Attention"
        status_class = "warning"
        reasons = attention_reasons
    else:
        status = "Healthy"
        status_class = "success"
        reasons = ["Tất cả phân hệ Vận chuyển, Chứng từ, Hải quan, Kho và Chi phí đang vận hành ổn định."]

    return {
        "status": status,
        "status_class": status_class,
        "reasons": reasons,
        "summary": "; ".join(reasons[:3]),
    }


__all__ = [
    "EXCEPTION_RULES_CATALOG",
    "parse_date_safe",
    "evaluate_8_exception_rules",
    "compute_trade_case_health",
]
