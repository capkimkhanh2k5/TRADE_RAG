# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""
checklist_manager.py — Automated Document Checklist Generation & Storage Layer
==============================================================================
Generates standardized Import/Export document checklists from master_config.py
templates with idempotency and dual-mode storage (Frappe MariaDB + In-Memory).
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

try:
    import frappe
except ImportError:
    frappe = None

from logistics_wizard.master_config import (
    get_required_documents_template,
    get_trade_thresholds,
)
from .readiness_evaluator import parse_date_safe


class InMemoryDocumentStore:
    """In-memory store enabling standalone unit tests without MariaDB."""

    def __init__(self):
        self.documents: Dict[str, Dict[str, Any]] = {}
        self._seq: int = 0

    def reset(self) -> None:
        self.documents.clear()
        self._seq = 0

    def next_name(self) -> str:
        self._seq += 1
        year = datetime.now().year
        return f"TDOC-{year}-{self._seq:05d}"

    def save(self, doc_dict: Dict[str, Any]) -> Dict[str, Any]:
        name = doc_dict.get("name") or self.next_name()
        doc_dict["name"] = name
        self.documents[name] = doc_dict
        return doc_dict

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        return self.documents.get(name)

    def list_by_case(self, case_id: str) -> List[Dict[str, Any]]:
        return [
            d for d in self.documents.values()
            if str(d.get("trade_case") or "") == str(case_id)
        ]

    def find_by_case_and_code(self, case_id: str, doc_code: str) -> Optional[Dict[str, Any]]:
        for d in self.documents.values():
            if str(d.get("trade_case") or "") == str(case_id) and str(d.get("document_code") or "") == str(doc_code):
                return d
        return None


in_memory_document_store = InMemoryDocumentStore()


def is_frappe_db_ready() -> bool:
    """Return True only when Frappe DB is genuinely connected and Trade Document DocType exists."""
    if not (frappe and getattr(frappe, "db", None)):
        return False
    exists_fn = getattr(frappe.db, "exists", None)
    if not callable(exists_fn):
        return False
    try:
        return bool(exists_fn("DocType", "Trade Document"))
    except Exception:
        return False


def _compute_default_deadline(eta_val: Any, required_before_stage: str, urgent_days: int) -> Optional[str]:
    eta_dt = parse_date_safe(eta_val)
    if not eta_dt:
        return None
    offset = urgent_days
    if required_before_stage in ("Booking", "Export Port"):
        offset = max(urgent_days + 2, 5)
    elif required_before_stage == "Warehouse":
        offset = max(1, urgent_days - 1)
    return str(eta_dt - timedelta(days=offset))


def _resolve_case_context(
    case_id: str,
    trade_type: Optional[str] = None,
    incoterm: Optional[str] = None,
    shipping_mode: Optional[str] = None,
    eta_date: Optional[str] = None,
    shipment_tracking: Optional[str] = None,
) -> Dict[str, Any]:
    ctx = {
        "trade_type": trade_type or "Import",
        "incoterm": incoterm or "FOB",
        "shipping_mode": shipping_mode or "Ocean",
        "eta_date": eta_date,
        "shipment_tracking": shipment_tracking,
    }
    if not is_frappe_db_ready():
        return ctx

    try:
        if frappe.db.exists("Trade Case", case_id):
            tc = frappe.db.get_value(
                "Trade Case",
                case_id,
                ["trade_type", "incoterm", "shipping_mode", "mode", "shipment_tracking", "target_completion_date"],
                as_dict=True,
            )
            if tc:
                ctx["trade_type"] = trade_type or tc.get("trade_type") or ctx["trade_type"]
                ctx["incoterm"] = incoterm or tc.get("incoterm") or ctx["incoterm"]
                ctx["shipping_mode"] = shipping_mode or tc.get("shipping_mode") or tc.get("mode") or ctx["shipping_mode"]
                ctx["shipment_tracking"] = shipment_tracking or tc.get("shipment_tracking")
                if not ctx["eta_date"]:
                    if ctx["shipment_tracking"] and frappe.db.exists("Shipment Tracking", ctx["shipment_tracking"]):
                        st_dates = frappe.db.get_value(
                            "Shipment Tracking",
                            ctx["shipment_tracking"],
                            ["eta", "etd"],
                            as_dict=True,
                        )
                        if st_dates:
                            ctx["eta_date"] = st_dates.get("eta") or st_dates.get("etd")
                    if not ctx["eta_date"]:
                        ctx["eta_date"] = tc.get("target_completion_date")
    except Exception:
        pass

    return ctx


def generate_case_document_checklist(
    case_id: str,
    trade_type: Optional[str] = None,
    incoterm: Optional[str] = None,
    shipping_mode: Optional[str] = None,
    eta_date: Optional[str] = None,
    shipment_tracking: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Idempotently initialize the standardized Trade Document checklist for a Trade Case
    based on master_config.get_required_documents_template().
    """
    cid = str(case_id or "").strip()
    if not cid:
        return {"success": False, "error": "Trade Case ID là bắt buộc."}

    ctx = _resolve_case_context(
        cid,
        trade_type=trade_type,
        incoterm=incoterm,
        shipping_mode=shipping_mode,
        eta_date=eta_date,
        shipment_tracking=shipment_tracking,
    )
    thresholds = get_trade_thresholds()
    urgent_days = int(thresholds.get("doc_urgent_days_before_eta", 3))
    template_items = get_required_documents_template(
        trade_type=ctx["trade_type"],
        incoterm=ctx["incoterm"],
        shipping_mode=ctx["shipping_mode"],
    )

    use_db = is_frappe_db_ready()
    existing_codes = set()
    if use_db:
        rows = frappe.get_all(
            "Trade Document",
            filters={"trade_case": cid},
            fields=["document_code"],
        ) or []
        existing_codes = {
            str(r.get("document_code") if isinstance(r, dict) else getattr(r, "document_code", ""))
            for r in rows
        }
    else:
        existing_codes = {
            str(d.get("document_code") or "")
            for d in in_memory_document_store.list_by_case(cid)
        }

    created_codes: List[str] = []
    for item in template_items:
        code = item["code"]
        if code in existing_codes:
            continue

        deadline_str = _compute_default_deadline(
            ctx.get("eta_date"),
            item.get("required_before_stage", "Customs"),
            urgent_days,
        )
        payload = {
            "doctype": "Trade Document",
            "trade_case": cid,
            "trade_type": ctx["trade_type"],
            "shipment_tracking": ctx.get("shipment_tracking"),
            "document_code": code,
            "document_name": item["name"],
            "category": item["category"],
            "is_mandatory": 1 if item.get("is_mandatory") else 0,
            "required_before_stage": item.get("required_before_stage", "Customs"),
            "status": "Required" if item.get("is_mandatory") else "N/A",
            "deadline": deadline_str,
            "current_version": 0,
            "versions": [],
        }

        if use_db:
            doc = frappe.get_doc(payload)
            doc.insert(ignore_permissions=True)
        else:
            in_memory_document_store.save(payload)

        created_codes.append(code)
        existing_codes.add(code)

    return {
        "success": True,
        "case_id": cid,
        "trade_type": ctx["trade_type"],
        "incoterm": ctx["incoterm"],
        "shipping_mode": ctx["shipping_mode"],
        "created_count": len(created_codes),
        "existing_count": len(existing_codes) - len(created_codes),
        "total_count": len(existing_codes),
        "created_codes": created_codes,
    }


__all__ = [
    "InMemoryDocumentStore",
    "in_memory_document_store",
    "is_frappe_db_ready",
    "generate_case_document_checklist",
]
