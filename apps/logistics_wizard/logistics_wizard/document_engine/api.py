# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""
document_engine.api — Public API Facade & Data Contract Implementation
======================================================================
Module 3: Trade Document Management (Phase 2)

Implements Section 3.1 contract from docs/todoTradeCase.md:
- get_case_documents_status(case_id)
- get_case_documents_list(case_id, category=None, status=None)
- init_case_document_checklist(case_id, ...)
- upload_trade_document_version(case_id, document_code, file_url, ...)
- verify_trade_document(doc_name, action="verify", notes=None, user=None)
- sync_trade_case_document_metrics(case_id)
- on_trade_case_after_insert(doc, method=None)
- scheduled_check_expiring_documents(as_of_date=None)
"""

from datetime import date, datetime
from typing import Any, Dict, List, Optional

try:
    import frappe
except ImportError:
    frappe = None

from logistics_wizard.doctype.trade_document.trade_document import TradeDocument
from .checklist_manager import (
    generate_case_document_checklist,
    in_memory_document_store,
    is_frappe_db_ready,
)
from .readiness_evaluator import (
    compute_document_readiness_payload,
    parse_date_safe,
)


def _frappe_whitelist():
    if frappe and hasattr(frappe, "whitelist"):
        return frappe.whitelist(allow_guest=True)
    return lambda fn: fn


def _get_case_stage(case_id: str) -> str:
    if is_frappe_db_ready() and frappe.db.exists("Trade Case", case_id):
        try:
            stage = frappe.db.get_value("Trade Case", case_id, "current_stage")
            if stage:
                return str(stage)
        except Exception:
            pass
    return "In Transit"


def _fetch_case_documents(case_id: str) -> List[Dict[str, Any]]:
    if is_frappe_db_ready():
        fields = [
            "name", "trade_case", "trade_type", "shipment_tracking", "customs_declaration_ref",
            "document_code", "document_name", "category", "is_mandatory", "required_before_stage",
            "status", "document_number", "issuer", "issue_date", "expiry_date", "deadline",
            "verified_by", "verified_at", "verification_notes", "file_url", "current_version", "remarks",
        ]
        rows = frappe.get_all(
            "Trade Document",
            filters={"trade_case": case_id},
            fields=fields,
            order_by="category asc, document_code asc",
        ) or []
        return [dict(r) if isinstance(r, dict) else r.as_dict() for r in rows]

    return list(in_memory_document_store.list_by_case(case_id))


@_frappe_whitelist()
def get_case_documents_status(case_id: str, as_of_date: Optional[str] = None) -> Dict[str, Any]:
    """
    Exact Section 3.1 API contract for Trade Case Overview:
    logistics_wizard.document_engine.api.get_case_documents_status(case_id)
    """
    cid = str(case_id or "").strip()
    docs = _fetch_case_documents(cid)
    stage = _get_case_stage(cid)
    return compute_document_readiness_payload(
        case_id=cid,
        docs=docs,
        current_stage=stage,
        as_of_date=as_of_date,
    )


@_frappe_whitelist()
def get_case_documents_list(
    case_id: str,
    category: Optional[str] = None,
    status: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Return full list of Trade Document records for a Trade Case with optional filters."""
    cid = str(case_id or "").strip()
    docs = _fetch_case_documents(cid)
    if category:
        docs = [d for d in docs if str(d.get("category") or "").lower() == str(category).strip().lower()]
    if status:
        docs = [d for d in docs if str(d.get("status") or "").lower() == str(status).strip().lower()]
    return docs


@_frappe_whitelist()
def init_case_document_checklist(
    case_id: str,
    trade_type: Optional[str] = None,
    incoterm: Optional[str] = None,
    shipping_mode: Optional[str] = None,
    eta_date: Optional[str] = None,
) -> Dict[str, Any]:
    """Initialize required document checklist for a Trade Case and sync case readiness."""
    res = generate_case_document_checklist(
        case_id=case_id,
        trade_type=trade_type,
        incoterm=incoterm,
        shipping_mode=shipping_mode,
        eta_date=eta_date,
    )
    if res.get("success"):
        sync_trade_case_document_metrics(case_id)
    return res


@_frappe_whitelist()
def upload_trade_document_version(
    case_id: str,
    document_code: str,
    file_url: str,
    document_name: Optional[str] = None,
    category: Optional[str] = None,
    document_number: Optional[str] = None,
    issuer: Optional[str] = None,
    issue_date: Optional[str] = None,
    expiry_date: Optional[str] = None,
    deadline: Optional[str] = None,
    change_notes: Optional[str] = None,
    user: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Upload or replace the attached file for a Trade Document, incrementing its
    version history automatically and advancing status Required/Missing -> Received.
    """
    cid = str(case_id or "").strip()
    code = str(document_code or "").strip()
    f_url = str(file_url or "").strip()
    if not cid or not code or not f_url:
        return {"success": False, "error": "case_id, document_code và file_url là bắt buộc."}

    use_db = is_frappe_db_ready()
    if use_db:
        existing_name = frappe.db.get_value(
            "Trade Document",
            {"trade_case": cid, "document_code": code},
            "name",
        )
        if existing_name:
            doc = frappe.get_doc("Trade Document", existing_name)
        else:
            doc = frappe.get_doc({
                "doctype": "Trade Document",
                "trade_case": cid,
                "document_code": code,
                "document_name": document_name or code,
                "category": category or "Commercial",
                "is_mandatory": 1,
                "status": "Required",
            })

        if document_name:
            doc.document_name = document_name
        if category:
            doc.category = category
        if document_number is not None:
            doc.document_number = document_number
        if issuer is not None:
            doc.issuer = issuer
        if issue_date is not None:
            doc.issue_date = issue_date
        if expiry_date is not None:
            doc.expiry_date = expiry_date
        if deadline is not None:
            doc.deadline = deadline

        doc._pending_change_notes = change_notes
        doc._pending_uploaded_by = user
        doc.file_url = f_url

        if existing_name:
            doc.save(ignore_permissions=True)
        else:
            doc.insert(ignore_permissions=True)

        return {
            "success": True,
            "name": doc.name,
            "case_id": cid,
            "document_code": doc.document_code,
            "status": doc.status,
            "current_version": doc.current_version,
            "file_url": doc.file_url,
            "versions_count": len(doc.versions or []),
        }

    # In-memory standalone mode
    existing = in_memory_document_store.find_by_case_and_code(cid, code)
    raw = dict(existing) if existing else {
        "trade_case": cid,
        "document_code": code,
        "document_name": document_name or code,
        "category": category or "Commercial",
        "is_mandatory": 1,
        "status": "Required",
        "versions": [],
    }
    if document_name:
        raw["document_name"] = document_name
    if category:
        raw["category"] = category
    if document_number is not None:
        raw["document_number"] = document_number
    if issuer is not None:
        raw["issuer"] = issuer
    if issue_date is not None:
        raw["issue_date"] = issue_date
    if expiry_date is not None:
        raw["expiry_date"] = expiry_date
    if deadline is not None:
        raw["deadline"] = deadline
    raw["file_url"] = f_url

    td = TradeDocument(raw)
    td._pending_change_notes = change_notes
    td._pending_uploaded_by = user
    td.validate()
    saved = in_memory_document_store.save(td.as_dict())
    return {
        "success": True,
        "name": saved["name"],
        "case_id": cid,
        "document_code": saved["document_code"],
        "status": saved["status"],
        "current_version": saved["current_version"],
        "file_url": saved["file_url"],
        "versions_count": len(saved.get("versions") or []),
    }


@_frappe_whitelist()
def verify_trade_document(
    doc_name: str,
    action: str = "verify",
    notes: Optional[str] = None,
    user: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Transition a Trade Document through verification actions:
    - 'verify'  -> Verified (validates attached file for mandatory docs)
    - 'reject'  -> Required (clears verification)
    - 'mark_na' -> N/A
    - 'mark_missing' -> Missing
    """
    act = str(action or "verify").strip().lower()
    action_to_status = {
        "verify": "Verified",
        "approve": "Verified",
        "reject": "Required",
        "mark_na": "N/A",
        "na": "N/A",
        "mark_missing": "Missing",
        "missing": "Missing",
    }
    if act not in action_to_status:
        return {"success": False, "error": f"Hành động không hợp lệ: {action}"}

    target_status = action_to_status[act]
    use_db = is_frappe_db_ready()

    if use_db:
        if not frappe.db.exists("Trade Document", doc_name):
            return {"success": False, "error": f"Không tìm thấy Trade Document '{doc_name}'."}
        doc = frappe.get_doc("Trade Document", doc_name)
        doc.status = target_status
        if target_status == "Verified":
            doc.verified_by = user or (getattr(getattr(frappe, "session", None), "user", None) or "Administrator")
            doc.verified_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            doc.verified_by = None
            doc.verified_at = None
        if notes is not None:
            doc.verification_notes = notes
        doc.save(ignore_permissions=True)
        return {
            "success": True,
            "name": doc.name,
            "case_id": doc.trade_case,
            "status": doc.status,
            "verified_by": doc.verified_by,
            "verified_at": str(doc.verified_at) if doc.verified_at else None,
        }

    # In-memory standalone mode
    raw = in_memory_document_store.get(doc_name)
    if not raw:
        return {"success": False, "error": f"Không tìm thấy Trade Document '{doc_name}'."}
    updated = dict(raw)
    updated["status"] = target_status
    if target_status == "Verified":
        updated["verified_by"] = user or "Administrator"
        updated["verified_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        updated["verified_by"] = None
        updated["verified_at"] = None
    if notes is not None:
        updated["verification_notes"] = notes

    td = TradeDocument(updated)
    td.validate()
    saved = in_memory_document_store.save(td.as_dict())
    return {
        "success": True,
        "name": saved["name"],
        "case_id": saved.get("trade_case"),
        "status": saved["status"],
        "verified_by": saved.get("verified_by"),
        "verified_at": saved.get("verified_at"),
    }


def sync_trade_case_document_metrics(case_id: str) -> Dict[str, Any]:
    """
    Roll up document_readiness_pct and missing_critical_docs summary onto Trade Case
    without duplicating child document records (Zero Data Duplication).
    """
    cid = str(case_id or "").strip()
    summary = get_case_documents_status(cid)

    critical_names = [
        f"{item['code']}: {item['name']}"
        for item in summary.get("missing_urgent", [])
        if item.get("type") == "critical"
    ]
    missing_text = "; ".join(critical_names)

    if is_frappe_db_ready() and frappe.db.exists("Trade Case", cid):
        try:
            frappe.db.set_value(
                "Trade Case",
                cid,
                {
                    "document_readiness_pct": summary["percentage"],
                    "missing_critical_docs": missing_text,
                },
                update_modified=False,
            )
        except Exception:
            pass

    return {
        "case_id": cid,
        "document_readiness_pct": summary["percentage"],
        "missing_critical_docs": missing_text,
    }


def on_trade_case_after_insert(doc, method=None) -> None:
    """Frappe doc_event hook: auto-generate required document checklist on Trade Case creation."""
    case_id = getattr(doc, "name", None)
    if not case_id:
        return
    try:
        generate_case_document_checklist(
            case_id=case_id,
            trade_type=getattr(doc, "trade_type", None),
            incoterm=getattr(doc, "incoterm", None),
            shipping_mode=getattr(doc, "shipping_mode", None) or getattr(doc, "mode", None),
            eta_date=getattr(doc, "target_completion_date", None),
            shipment_tracking=getattr(doc, "shipment_tracking", None),
        )
        sync_trade_case_document_metrics(case_id)
    except Exception:
        pass


def scheduled_check_expiring_documents(as_of_date: Optional[str] = None) -> Dict[str, Any]:
    """
    Daily scheduler job: detect documents past expiry_date (mark Expired) and mandatory
    documents past deadline (mark Missing), then refresh Trade Case readiness rollups.
    """
    today_dt = parse_date_safe(as_of_date) or date.today()
    use_db = is_frappe_db_ready()

    if use_db:
        rows = frappe.get_all(
            "Trade Document",
            filters={"status": ["not in", ["N/A"]]},
            fields=["name", "trade_case", "status", "is_mandatory", "expiry_date", "deadline"],
        ) or []
        docs = [dict(r) if isinstance(r, dict) else r.as_dict() for r in rows]
    else:
        docs = [
            d for d in in_memory_document_store.documents.values()
            if d.get("status") != "N/A"
        ]

    expired_names: List[str] = []
    overdue_missing_names: List[str] = []
    affected_cases = set()

    for d in docs:
        d_name = d.get("name")
        case_id = d.get("trade_case")
        cur_status = d.get("status")
        exp_dt = parse_date_safe(d.get("expiry_date"))
        dl_dt = parse_date_safe(d.get("deadline"))
        is_mandatory = int(d.get("is_mandatory", 1) or 0) == 1

        new_status = None
        if exp_dt and exp_dt < today_dt and cur_status != "Expired":
            new_status = "Expired"
            expired_names.append(d_name)
        elif is_mandatory and cur_status == "Required" and dl_dt and dl_dt < today_dt:
            new_status = "Missing"
            overdue_missing_names.append(d_name)

        if new_status:
            if use_db:
                frappe.db.set_value("Trade Document", d_name, "status", new_status)
            else:
                d["status"] = new_status
                in_memory_document_store.save(d)
            if case_id:
                affected_cases.add(case_id)

    for cid in affected_cases:
        sync_trade_case_document_metrics(cid)

    if use_db and (expired_names or overdue_missing_names):
        try:
            frappe.db.commit()
        except Exception:
            pass

    return {
        "success": True,
        "scanned_count": len(docs),
        "expired_count": len(expired_names),
        "overdue_missing_count": len(overdue_missing_names),
        "expired_documents": expired_names,
        "overdue_missing_documents": overdue_missing_names,
        "affected_cases": sorted(affected_cases),
    }


__all__ = [
    "get_case_documents_status",
    "get_case_documents_list",
    "init_case_document_checklist",
    "upload_trade_document_version",
    "verify_trade_document",
    "sync_trade_case_document_metrics",
    "on_trade_case_after_insert",
    "scheduled_check_expiring_documents",
]
