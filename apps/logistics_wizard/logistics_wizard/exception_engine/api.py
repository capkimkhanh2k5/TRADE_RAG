# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""
exception_engine.api — Exception Workflow, Escalation, Action Items & Health Rollup
====================================================================================
Module 6: Exception / Workflow / Action Management (Phase 4)
"""

from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional

try:
    import frappe
except ImportError:
    frappe = None

from logistics_wizard.doctype.shipment_exception.shipment_exception import ShipmentException
from logistics_wizard.doctype.trade_action_item.trade_action_item import TradeActionItem
from .rule_evaluator import (
    compute_trade_case_health,
    evaluate_8_exception_rules,
    parse_date_safe,
)

OPEN_STATUSES = ("Open", "Investigating", "Acknowledged", "Pending Vendor", "Escalated")


def _frappe_whitelist():
    if frappe and hasattr(frappe, "whitelist"):
        return frappe.whitelist(allow_guest=True)
    return lambda fn: fn


class InMemoryExceptionStore:
    def __init__(self):
        self.exceptions: Dict[str, Dict[str, Any]] = {}
        self._seq: int = 0

    def reset(self) -> None:
        self.exceptions.clear()
        self._seq = 0

    def next_name(self) -> str:
        self._seq += 1
        return f"EXC-{datetime.now().year}-{self._seq:05d}"

    def save(self, doc_dict: Dict[str, Any]) -> Dict[str, Any]:
        name = doc_dict.get("name") or self.next_name()
        doc_dict["name"] = name
        self.exceptions[name] = doc_dict
        return doc_dict

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        return self.exceptions.get(name)

    def list_by_case(self, case_id: str) -> List[Dict[str, Any]]:
        return [
            e for e in self.exceptions.values()
            if str(e.get("trade_case") or "") == str(case_id)
        ]

    def find_open_by_rule(self, case_id: str, rule_code: str) -> Optional[Dict[str, Any]]:
        for e in self.exceptions.values():
            if (
                str(e.get("trade_case") or "") == str(case_id)
                and str(e.get("rule_code") or "") == str(rule_code)
                and str(e.get("status") or "Open") in OPEN_STATUSES
            ):
                return e
        return None


class InMemoryActionStore:
    def __init__(self):
        self.actions: Dict[str, Dict[str, Any]] = {}
        self._seq: int = 0

    def reset(self) -> None:
        self.actions.clear()
        self._seq = 0

    def next_name(self) -> str:
        self._seq += 1
        return f"TACT-{datetime.now().year}-{self._seq:05d}"

    def save(self, doc_dict: Dict[str, Any]) -> Dict[str, Any]:
        name = doc_dict.get("name") or self.next_name()
        doc_dict["name"] = name
        self.actions[name] = doc_dict
        return doc_dict

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        return self.actions.get(name)

    def list_by_case(self, case_id: str) -> List[Dict[str, Any]]:
        return [
            a for a in self.actions.values()
            if str(a.get("trade_case") or "") == str(case_id)
        ]


in_memory_exception_store = InMemoryExceptionStore()
in_memory_action_store = InMemoryActionStore()


def is_frappe_db_ready(doctype: str = "Shipment Exception") -> bool:
    if not (frappe and getattr(frappe, "db", None)):
        return False
    exists_fn = getattr(frappe.db, "exists", None)
    if not callable(exists_fn):
        return False
    try:
        return bool(exists_fn("DocType", doctype))
    except Exception:
        return False


def _get_current_user() -> str:
    if frappe and getattr(frappe, "session", None) and getattr(frappe.session, "user", None):
        return str(frappe.session.user)
    return "Administrator"


def _append_audit(existing_log: Optional[str], event: str, actor: Optional[str] = None) -> str:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    who = actor or _get_current_user()
    line = f"[{ts}] ({who}) {event}"
    return f"{existing_log}\n{line}".strip() if existing_log else line


def _to_dict(doc: Any) -> Dict[str, Any]:
    if isinstance(doc, dict):
        return dict(doc)
    if callable(getattr(doc, "as_dict", None)):
        return doc.as_dict()
    return dict(doc.__dict__)


def _fetch_case_exceptions(case_id: str) -> List[Dict[str, Any]]:
    if is_frappe_db_ready("Shipment Exception"):
        fields = [
            "name", "trade_case", "shipment_tracking", "rule_code", "source_module",
            "exception_type", "severity", "status", "title", "description",
            "assigned_to", "department", "due_date", "escalation_level",
            "escalated_to", "escalated_at", "raised_at", "resolved_at", "resolved_by",
            "resolution_notes", "audit_log", "delay_days",
        ]
        rows = frappe.get_all(
            "Shipment Exception",
            filters={"trade_case": case_id},
            fields=fields,
            order_by="raised_at desc",
        ) or []
        return [dict(r) if isinstance(r, dict) else r.as_dict() for r in rows]

    return list(in_memory_exception_store.list_by_case(case_id))


@_frappe_whitelist()
def raise_exception_from_rule(
    case_id: str,
    rule_code: str,
    exception_type: str,
    severity: str,
    title: str,
    description: str,
    department: str = "Logistics",
    source_module: str = "Manual",
    due_date: Optional[str] = None,
    assigned_to: Optional[str] = None,
    shipment_tracking: Optional[str] = None,
    delay_days: int = 0,
    reference_doctype: Optional[str] = None,
    reference_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Idempotently create or update an open Shipment Exception for a given (case_id, rule_code).
    Prevents duplicate alerts across repeated scheduler or hook evaluations.
    """
    cid = str(case_id or "").strip()
    if not cid:
        return {"success": False, "error": "Trade Case ID là bắt buộc."}

    use_db = is_frappe_db_ready("Shipment Exception")
    if use_db:
        existing_name = None
        if rule_code:
            existing_name = frappe.db.get_value(
                "Shipment Exception",
                {
                    "trade_case": cid,
                    "rule_code": rule_code,
                    "status": ["in", list(OPEN_STATUSES)],
                },
                "name",
            )
        if existing_name:
            doc = frappe.get_doc("Shipment Exception", existing_name)
            doc.severity = severity
            doc.title = title
            doc.description = description
            if due_date and not doc.due_date:
                doc.due_date = due_date
            if delay_days:
                doc.delay_days = int(delay_days)
            doc.save(ignore_permissions=True)
            return {"success": True, "created": False, "name": doc.name, "case_id": cid}

        doc = frappe.get_doc(
            {
                "doctype": "Shipment Exception",
                "trade_case": cid,
                "shipment_tracking": shipment_tracking,
                "rule_code": rule_code,
                "source_module": source_module,
                "exception_type": exception_type,
                "severity": severity,
                "status": "Open",
                "title": title,
                "description": description,
                "department": department,
                "assigned_to": assigned_to,
                "due_date": due_date,
                "delay_days": int(delay_days or 0),
                "reference_doctype": reference_doctype,
                "reference_name": reference_name,
                "audit_log": _append_audit("", f"Exception raised by {rule_code or 'Manual'} ({severity})"),
            }
        )
        doc.insert(ignore_permissions=True)
        return {"success": True, "created": True, "name": doc.name, "case_id": cid}

    # In-memory standalone mode
    existing = in_memory_exception_store.find_open_by_rule(cid, rule_code) if rule_code else None
    if existing:
        existing["severity"] = severity
        existing["title"] = title
        existing["description"] = description
        if due_date and not existing.get("due_date"):
            existing["due_date"] = due_date
        if delay_days:
            existing["delay_days"] = int(delay_days)
        in_memory_exception_store.save(existing)
        sync_trade_case_exception_and_health(cid)
        return {"success": True, "created": False, "name": existing["name"], "case_id": cid}

    payload = {
        "trade_case": cid,
        "shipment_tracking": shipment_tracking,
        "rule_code": rule_code,
        "source_module": source_module,
        "exception_type": exception_type,
        "severity": severity,
        "status": "Open",
        "title": title,
        "description": description,
        "department": department,
        "assigned_to": assigned_to,
        "due_date": due_date,
        "escalation_level": 0,
        "delay_days": int(delay_days or 0),
        "reference_doctype": reference_doctype,
        "reference_name": reference_name,
        "audit_log": _append_audit("", f"Exception raised by {rule_code or 'Manual'} ({severity})"),
    }
    se = ShipmentException(payload)
    se.validate()
    saved = in_memory_exception_store.save(se.as_dict())
    sync_trade_case_exception_and_health(cid)
    return {"success": True, "created": True, "name": saved["name"], "case_id": cid}


def _collect_live_signals(case_id: str, as_of_date: Optional[str] = None) -> Dict[str, Any]:
    """Gather real-time operational signals from all child modules for a Trade Case."""
    signals: Dict[str, Any] = {
        "current_stage": "In Transit",
        "shipment": {},
        "documents": {},
        "customs": {},
        "cost": {},
        "warehouse": {},
    }

    if is_frappe_db_ready("Trade Case") and frappe.db.exists("Trade Case", case_id):
        tc = frappe.db.get_value(
            "Trade Case", case_id, ["current_stage", "shipment_tracking"], as_dict=True
        )
        if tc:
            signals["current_stage"] = tc.get("current_stage") or "In Transit"
            shp_id = tc.get("shipment_tracking")
            if shp_id and frappe.db.exists("Shipment Tracking", shp_id):
                st = frappe.db.get_value(
                    "Shipment Tracking",
                    shp_id,
                    ["name", "status", "delay_days", "eta", "ata", "is_stale", "last_synced_at"],
                    as_dict=True,
                )
                if st:
                    signals["shipment"] = {
                        "shipment_id": st.get("name"),
                        "status": st.get("status"),
                        "delay_days": int(st.get("delay_days") or 0),
                        "current_eta": str(st.get("eta")) if st.get("eta") else None,
                        "ata": str(st.get("ata")) if st.get("ata") else None,
                        "is_stale": bool(st.get("is_stale")),
                    }

    try:
        from logistics_wizard.document_engine.api import get_case_documents_status
        signals["documents"] = get_case_documents_status(case_id, as_of_date=as_of_date)
    except Exception:
        pass

    try:
        from logistics_wizard.customs_engine.api import get_case_customs_status
        signals["customs"] = get_case_customs_status(case_id, as_of_date=as_of_date)
    except Exception:
        pass

    try:
        from logistics_wizard.costing_engine.api import get_case_cost_summary
        signals["cost"] = get_case_cost_summary(case_id)
    except Exception:
        pass

    try:
        from logistics_wizard.warehouse_engine.api import get_case_warehouse_status
        signals["warehouse"] = get_case_warehouse_status(case_id)
    except Exception:
        pass

    return signals


@_frappe_whitelist()
def evaluate_case_exceptions(
    case_id: str,
    signals: Optional[Dict[str, Any]] = None,
    auto_create: bool = True,
    as_of_date: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Run all 8 exception rules for a Trade Case, optionally create/update exceptions
    idempotently, and compute + persist Trade Case.overall_health.
    """
    cid = str(case_id or "").strip()
    if not cid:
        return {"success": False, "error": "Trade Case ID là bắt buộc."}

    effective_signals = signals if signals is not None else _collect_live_signals(cid, as_of_date=as_of_date)
    candidates = evaluate_8_exception_rules(cid, effective_signals, as_of_date=as_of_date)

    created_names: List[str] = []
    updated_names: List[str] = []
    if auto_create:
        for cand in candidates:
            res = raise_exception_from_rule(
                case_id=cid,
                rule_code=cand["rule_code"],
                exception_type=cand["exception_type"],
                severity=cand["severity"],
                title=cand["title"],
                description=cand["description"],
                department=cand.get("department", "Logistics"),
                source_module=cand.get("source_module", "Manual"),
                due_date=cand.get("due_date"),
                shipment_tracking=cand.get("shipment_tracking"),
                delay_days=cand.get("delay_days", 0),
            )
            if res.get("success"):
                if res.get("created"):
                    created_names.append(res["name"])
                else:
                    updated_names.append(res["name"])

    open_excs = [e for e in _fetch_case_exceptions(cid) if e.get("status") in OPEN_STATUSES]
    health = compute_trade_case_health(effective_signals, open_excs)
    sync_trade_case_exception_and_health(cid, health_override=health["status"])

    return {
        "success": True,
        "case_id": cid,
        "triggered_rules": [c["rule_code"] for c in candidates],
        "triggered_count": len(candidates),
        "created_count": len(created_names),
        "updated_count": len(updated_names),
        "created_exceptions": created_names,
        "open_exceptions_count": len(open_excs),
        "health": health,
    }


@_frappe_whitelist()
def get_case_exceptions_summary(case_id: str, as_of_date: Optional[str] = None) -> Dict[str, Any]:
    """Return Trade Case Overview 'open_exceptions' payload sorted by severity & due date."""
    cid = str(case_id or "").strip()
    today_dt = parse_date_safe(as_of_date) or date.today()
    all_excs = _fetch_case_exceptions(cid)
    open_excs = [e for e in all_excs if str(e.get("status") or "Open") in OPEN_STATUSES]

    sev_rank = {"critical": 0, "high": 1, "warning": 2, "info": 3}
    open_excs.sort(
        key=lambda e: (
            sev_rank.get(str(e.get("severity") or "warning").lower(), 2),
            str(e.get("due_date") or "9999-12-31"),
            str(e.get("name") or ""),
        )
    )

    overdue = 0
    due_soon = 0
    critical_count = 0
    items: List[Dict[str, Any]] = []
    for e in open_excs:
        sev_upper = str(e.get("severity") or "WARNING").upper()
        if sev_upper == "CRITICAL":
            critical_count += 1
        dl_dt = parse_date_safe(e.get("due_date"))
        if dl_dt:
            diff = (dl_dt - today_dt).days
            if diff < 0:
                overdue += 1
            elif diff <= 2:
                due_soon += 1
        items.append(
            {
                "id": e.get("name"),
                "rule_code": e.get("rule_code"),
                "exception_type": e.get("exception_type"),
                "severity": sev_upper,
                "title": e.get("title") or e.get("description"),
                "owner": e.get("assigned_to") or "Unassigned",
                "department": e.get("department") or "Logistics",
                "due_date": str(e.get("due_date")) if e.get("due_date") else None,
                "status": e.get("status") or "Open",
                "escalation_level": int(e.get("escalation_level") or 0),
                "source_module": e.get("source_module") or "Shipment",
            }
        )

    return {
        "case_id": cid,
        "total_open": len(open_excs),
        "critical_count": critical_count,
        "overdue": overdue,
        "due_soon": due_soon,
        "all_count": len(all_excs),
        "items": items,
    }


@_frappe_whitelist()
def assign_exception(
    exception_name: str,
    assigned_to: str,
    department: Optional[str] = None,
    due_date: Optional[str] = None,
    status: Optional[str] = None,
    notes: Optional[str] = None,
) -> Dict[str, Any]:
    """Assign responsible owner, department, and due date with audit logging."""
    use_db = is_frappe_db_ready("Shipment Exception")
    event_msg = f"Assigned to {assigned_to}" + (f" ({department})" if department else "") + (f": {notes}" if notes else "")

    if use_db:
        if not frappe.db.exists("Shipment Exception", exception_name):
            return {"success": False, "error": f"Không tìm thấy sự cố '{exception_name}'."}
        doc = frappe.get_doc("Shipment Exception", exception_name)
        doc.assigned_to = assigned_to
        if department:
            doc.department = department
        if due_date:
            doc.due_date = due_date
        if status:
            doc.status = status
        elif doc.status == "Open":
            doc.status = "Investigating"
        doc.audit_log = _append_audit(doc.audit_log, event_msg)
        doc.save(ignore_permissions=True)
        return {"success": True, "name": doc.name, "assigned_to": doc.assigned_to, "status": doc.status}

    raw = in_memory_exception_store.get(exception_name)
    if not raw:
        return {"success": False, "error": f"Không tìm thấy sự cố '{exception_name}'."}
    raw["assigned_to"] = assigned_to
    if department:
        raw["department"] = department
    if due_date:
        raw["due_date"] = due_date
    if status:
        raw["status"] = status
    elif raw.get("status") == "Open":
        raw["status"] = "Investigating"
    raw["audit_log"] = _append_audit(raw.get("audit_log"), event_msg)
    in_memory_exception_store.save(raw)
    return {"success": True, "name": raw["name"], "assigned_to": raw["assigned_to"], "status": raw["status"]}


@_frappe_whitelist()
def escalate_exception(
    exception_name: str,
    escalated_to: Optional[str] = None,
    reason: Optional[str] = None,
) -> Dict[str, Any]:
    """Escalate an open exception to the next management tier (Level 0 -> 1 -> 2)."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    use_db = is_frappe_db_ready("Shipment Exception")

    if use_db:
        if not frappe.db.exists("Shipment Exception", exception_name):
            return {"success": False, "error": f"Không tìm thấy sự cố '{exception_name}'."}
        doc = frappe.get_doc("Shipment Exception", exception_name)
        new_level = min(2, int(doc.escalation_level or 0) + 1)
        doc.escalation_level = new_level
        doc.status = "Escalated"
        if doc.severity in ("Info", "Warning"):
            doc.severity = "High"
        elif doc.severity == "High":
            doc.severity = "Critical"
        if escalated_to:
            doc.escalated_to = escalated_to
        doc.escalated_at = now_str
        doc.audit_log = _append_audit(
            doc.audit_log,
            f"Escalated to Level {new_level} (Severity: {doc.severity})" + (f" — {reason}" if reason else ""),
        )
        doc.save(ignore_permissions=True)
        return {
            "success": True,
            "name": doc.name,
            "escalation_level": doc.escalation_level,
            "severity": doc.severity,
            "status": doc.status,
        }

    raw = in_memory_exception_store.get(exception_name)
    if not raw:
        return {"success": False, "error": f"Không tìm thấy sự cố '{exception_name}'."}
    new_level = min(2, int(raw.get("escalation_level") or 0) + 1)
    raw["escalation_level"] = new_level
    raw["status"] = "Escalated"
    if raw.get("severity") in ("Info", "Warning"):
        raw["severity"] = "High"
    elif raw.get("severity") == "High":
        raw["severity"] = "Critical"
    if escalated_to:
        raw["escalated_to"] = escalated_to
    raw["escalated_at"] = now_str
    raw["audit_log"] = _append_audit(
        raw.get("audit_log"),
        f"Escalated to Level {new_level} (Severity: {raw['severity']})" + (f" — {reason}" if reason else ""),
    )
    in_memory_exception_store.save(raw)
    if raw.get("trade_case"):
        sync_trade_case_exception_and_health(raw["trade_case"])
    return {
        "success": True,
        "name": raw["name"],
        "escalation_level": raw["escalation_level"],
        "severity": raw["severity"],
        "status": raw["status"],
    }


@_frappe_whitelist()
def resolve_exception(
    exception_name: str,
    resolution_notes: str,
    status: str = "Resolved",
    user: Optional[str] = None,
) -> Dict[str, Any]:
    """Resolve or close an exception with mandatory audit trail and Trade Case health refresh."""
    target = "Closed" if str(status).strip().lower() == "closed" else "Resolved"
    actor = user or _get_current_user()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    use_db = is_frappe_db_ready("Shipment Exception")

    if use_db:
        if not frappe.db.exists("Shipment Exception", exception_name):
            return {"success": False, "error": f"Không tìm thấy sự cố '{exception_name}'."}
        doc = frappe.get_doc("Shipment Exception", exception_name)
        doc.status = target
        doc.resolution_notes = resolution_notes
        doc.resolved_by = actor
        doc.resolved_at = now_str
        doc.audit_log = _append_audit(doc.audit_log, f"Marked {target}: {resolution_notes}", actor=actor)
        doc.save(ignore_permissions=True)
        return {
            "success": True,
            "name": doc.name,
            "case_id": doc.trade_case,
            "status": doc.status,
            "resolved_by": doc.resolved_by,
        }

    raw = in_memory_exception_store.get(exception_name)
    if not raw:
        return {"success": False, "error": f"Không tìm thấy sự cố '{exception_name}'."}
    raw["status"] = target
    raw["resolution_notes"] = resolution_notes
    raw["resolved_by"] = actor
    raw["resolved_at"] = now_str
    raw["audit_log"] = _append_audit(raw.get("audit_log"), f"Marked {target}: {resolution_notes}", actor=actor)
    in_memory_exception_store.save(raw)
    if raw.get("trade_case"):
        sync_trade_case_exception_and_health(raw["trade_case"])
    return {
        "success": True,
        "name": raw["name"],
        "case_id": raw.get("trade_case"),
        "status": raw["status"],
        "resolved_by": raw["resolved_by"],
    }


@_frappe_whitelist()
def create_action_item(
    case_id: str,
    action_title: str,
    department: str = "Logistics",
    owner_user: Optional[str] = None,
    owner_name: Optional[str] = None,
    due_date: Optional[str] = None,
    priority: str = "Medium",
    shipment_exception: Optional[str] = None,
    notes: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a follow-up Trade Action Item linked to a Trade Case."""
    cid = str(case_id or "").strip()
    title = str(action_title or "").strip()
    if not cid or not title:
        return {"success": False, "error": "case_id và action_title là bắt buộc."}

    payload = {
        "doctype": "Trade Action Item",
        "trade_case": cid,
        "shipment_exception": shipment_exception,
        "action_title": title,
        "department": department or "Logistics",
        "owner_user": owner_user,
        "owner_name": owner_name or owner_user or "Unassigned",
        "due_date": due_date,
        "priority": priority or "Medium",
        "status": "Open",
        "notes": notes,
    }

    if is_frappe_db_ready("Trade Action Item"):
        doc = frappe.get_doc(payload)
        doc.insert(ignore_permissions=True)
        saved = _to_dict(doc)
    else:
        act = TradeActionItem(payload)
        act.validate()
        saved = in_memory_action_store.save(act.as_dict())

    return {
        "success": True,
        "name": saved["name"],
        "case_id": cid,
        "action_title": saved["action_title"],
        "status": saved["status"],
    }


@_frappe_whitelist()
def complete_action_item(
    action_name: str,
    notes: Optional[str] = None,
    user: Optional[str] = None,
) -> Dict[str, Any]:
    """Mark a Trade Action Item as Completed."""
    actor = user or _get_current_user()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if is_frappe_db_ready("Trade Action Item"):
        if not frappe.db.exists("Trade Action Item", action_name):
            return {"success": False, "error": f"Không tìm thấy Action Item '{action_name}'."}
        doc = frappe.get_doc("Trade Action Item", action_name)
        doc.status = "Completed"
        doc.completed_by = actor
        doc.completed_at = now_str
        if notes is not None:
            doc.notes = notes
        doc.save(ignore_permissions=True)
        return {"success": True, "name": doc.name, "status": doc.status, "completed_by": doc.completed_by}

    raw = in_memory_action_store.get(action_name)
    if not raw:
        return {"success": False, "error": f"Không tìm thấy Action Item '{action_name}'."}
    raw["status"] = "Completed"
    raw["completed_by"] = actor
    raw["completed_at"] = now_str
    if notes is not None:
        raw["notes"] = notes
    in_memory_action_store.save(raw)
    return {"success": True, "name": raw["name"], "status": raw["status"], "completed_by": raw["completed_by"]}


@_frappe_whitelist()
def get_case_action_items(case_id: str, include_completed: bool = False) -> List[Dict[str, Any]]:
    """Return formatted upcoming_actions list for Trade Case Overview."""
    cid = str(case_id or "").strip()
    if is_frappe_db_ready("Trade Action Item"):
        filters: Dict[str, Any] = {"trade_case": cid}
        if not include_completed:
            filters["status"] = ["in", ["Open", "In Progress"]]
        rows = frappe.get_all(
            "Trade Action Item",
            filters=filters,
            fields=["name", "action_title", "department", "owner_name", "owner_user", "due_date", "priority", "status", "shipment_exception"],
            order_by="due_date asc, modified desc",
        ) or []
        raw_list = [dict(r) if isinstance(r, dict) else r.as_dict() for r in rows]
    else:
        raw_list = in_memory_action_store.list_by_case(cid)
        if not include_completed:
            raw_list = [a for a in raw_list if a.get("status") in ("Open", "In Progress")]

    return [
        {
            "id": a.get("name"),
            "date": str(a.get("due_date")) if a.get("due_date") else None,
            "action": a.get("action_title"),
            "department": a.get("department") or "Logistics",
            "owner": a.get("owner_name") or a.get("owner_user") or "Unassigned",
            "priority": a.get("priority") or "Medium",
            "status": a.get("status") or "Open",
            "shipment_exception": a.get("shipment_exception"),
        }
        for a in raw_list
    ]


def sync_trade_case_exception_and_health(
    case_id: str,
    health_override: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Roll up open_exceptions_count, critical_exceptions_count, and auto-computed
    overall_health onto Trade Case (Zero Data Duplication).
    """
    cid = str(case_id or "").strip()
    open_excs = [e for e in _fetch_case_exceptions(cid) if str(e.get("status") or "Open") in OPEN_STATUSES]
    crit_count = sum(1 for e in open_excs if str(e.get("severity") or "").lower() == "critical")

    if health_override:
        health_status = health_override
    else:
        health_status = compute_trade_case_health(signals=None, open_exceptions=open_excs)["status"]

    if is_frappe_db_ready("Trade Case") and frappe.db.exists("Trade Case", cid):
        try:
            frappe.db.set_value(
                "Trade Case",
                cid,
                {
                    "open_exceptions_count": len(open_excs),
                    "critical_exceptions_count": crit_count,
                    "overall_health": health_status,
                },
                update_modified=False,
            )
        except Exception:
            pass

    return {
        "case_id": cid,
        "open_exceptions_count": len(open_excs),
        "critical_exceptions_count": crit_count,
        "overall_health": health_status,
    }


def scheduled_evaluate_all_active_cases(as_of_date: Optional[str] = None) -> Dict[str, Any]:
    """Hourly scheduler job: evaluate all 8 exception rules on active Trade Cases and auto-escalate overdue exceptions."""
    today_dt = parse_date_safe(as_of_date) or date.today()
    cases_evaluated = 0
    exceptions_created = 0
    escalated_count = 0

    if is_frappe_db_ready("Trade Case"):
        active_cases = frappe.get_all(
            "Trade Case",
            filters={"status": ["not in", ["Closed", "Cancelled", "Completed"]]},
            pluck="name",
        ) or []
        for cid in active_cases:
            res = evaluate_case_exceptions(cid, auto_create=True, as_of_date=str(today_dt))
            cases_evaluated += 1
            exceptions_created += int(res.get("created_count") or 0)

        # Auto-escalate overdue open exceptions still at escalation_level == 0
        overdue_rows = frappe.get_all(
            "Shipment Exception",
            filters={
                "status": ["in", ["Open", "Investigating", "Pending Vendor"]],
                "escalation_level": 0,
                "due_date": ["<", str(today_dt)],
            },
            pluck="name",
        ) or []
        for exc_name in overdue_rows:
            esc = escalate_exception(exc_name, reason="Tự động escalation do quá hạn xử lý (SLA Overdue)")
            if esc.get("success"):
                escalated_count += 1
        try:
            frappe.db.commit()
        except Exception:
            pass

    return {
        "success": True,
        "cases_evaluated": cases_evaluated,
        "exceptions_created": exceptions_created,
        "escalated_count": escalated_count,
    }


__all__ = [
    "OPEN_STATUSES",
    "InMemoryExceptionStore",
    "InMemoryActionStore",
    "in_memory_exception_store",
    "in_memory_action_store",
    "is_frappe_db_ready",
    "raise_exception_from_rule",
    "evaluate_case_exceptions",
    "get_case_exceptions_summary",
    "assign_exception",
    "escalate_exception",
    "resolve_exception",
    "create_action_item",
    "complete_action_item",
    "get_case_action_items",
    "sync_trade_case_exception_and_health",
    "scheduled_evaluate_all_active_cases",
]
