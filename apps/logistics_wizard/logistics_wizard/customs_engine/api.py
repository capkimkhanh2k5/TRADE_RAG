# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""
customs_engine.api — Public API Facade & Section 3.2 Data Contract
===================================================================
Module 4: Customs & Trade Compliance (Phase 3)

Implements:
- get_case_customs_status(case_id, as_of_date=None)  [Section 3.2 exact contract]
- get_case_customs_declarations(case_id)
- create_customs_declaration(case_id, ...)
- propose_hs_code(declaration_name, item_idx, suggested_hs_code, ...)
- approve_hs_code(declaration_name, item_idx, action="approve", ...)
- advance_customs_workflow(declaration_name, target_status, ...)
- sync_trade_case_customs_metrics(case_id)
- scheduled_check_overdue_customs(as_of_date=None)
"""

from datetime import date, datetime
import json
from typing import Any, Dict, List, Optional

try:
    import frappe
except ImportError:
    frappe = None

from logistics_wizard.doctype.customs_declaration.customs_declaration import CustomsDeclaration
from .ai_hs_advisor import recommend_hs_codes
from .tax_calculator import is_valid_hs_code, normalize_hs_code
from .ai_hs_advisor import recommend_hs_codes
from .workflow_engine import (
    ALLOWED_TRANSITIONS,
    can_transition,
    compute_customs_readiness_payload,
    is_declaration_overdue,
    parse_date_safe,
)


def _frappe_whitelist():
    if frappe and hasattr(frappe, "whitelist"):
        return frappe.whitelist(allow_guest=True)
    return lambda fn: fn


class InMemoryCustomsStore:
    """In-memory store enabling fast standalone unit tests without MariaDB."""

    def __init__(self):
        self.declarations: Dict[str, Dict[str, Any]] = {}
        self._seq: int = 0

    def reset(self) -> None:
        self.declarations.clear()
        self._seq = 0

    def next_name(self) -> str:
        self._seq += 1
        year = datetime.now().year
        return f"CDEC-{year}-{self._seq:05d}"

    def save(self, doc_dict: Dict[str, Any]) -> Dict[str, Any]:
        name = doc_dict.get("name") or self.next_name()
        doc_dict["name"] = name
        self.declarations[name] = doc_dict
        return doc_dict

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        return self.declarations.get(name)

    def list_by_case(self, case_id: str) -> List[Dict[str, Any]]:
        return [
            d for d in self.declarations.values()
            if str(d.get("trade_case") or "") == str(case_id)
        ]


in_memory_customs_store = InMemoryCustomsStore()


def is_frappe_db_ready() -> bool:
    """Return True only when Frappe DB is genuinely connected and Customs Declaration exists."""
    if not (frappe and getattr(frappe, "db", None)):
        return False
    exists_fn = getattr(frappe.db, "exists", None)
    if not callable(exists_fn):
        return False
    try:
        return bool(exists_fn("DocType", "Customs Declaration"))
    except Exception:
        return False


def _get_current_user() -> str:
    if frappe and getattr(frappe, "session", None) and getattr(frappe.session, "user", None):
        return str(frappe.session.user)
    return "Administrator"


def _doc_to_dict(doc: Any) -> Dict[str, Any]:
    if isinstance(doc, dict):
        d = dict(doc)
    elif callable(getattr(doc, "as_dict", None)):
        d = doc.as_dict()
    else:
        d = dict(doc.__dict__)
    items = d.get("items") or []
    d["items"] = [
        (
            dict(it)
            if isinstance(it, dict)
            else (it.as_dict() if callable(getattr(it, "as_dict", None)) else dict(it.__dict__))
        )
        for it in items
    ]
    return d


def _fetch_case_declarations(case_id: str) -> List[Dict[str, Any]]:
    if is_frappe_db_ready():
        names = frappe.get_all(
            "Customs Declaration",
            filters={"trade_case": case_id},
            pluck="name",
            order_by="modified desc",
        ) or []
        return [_doc_to_dict(frappe.get_doc("Customs Declaration", n)) for n in names]

    return list(reversed(in_memory_customs_store.list_by_case(case_id)))


def _get_doc_readiness_safe(case_id: str) -> Optional[Dict[str, Any]]:
    try:
        from logistics_wizard.document_engine.api import get_case_documents_status
        return get_case_documents_status(case_id)
    except Exception:
        return None


@_frappe_whitelist()
def get_case_customs_status(case_id: str, as_of_date: Optional[str] = None) -> Dict[str, Any]:
    """
    Exact Section 3.2 API contract for Trade Case Overview:
    logistics_wizard.customs_engine.api.get_case_customs_status(case_id)
    """
    cid = str(case_id or "").strip()
    declarations = _fetch_case_declarations(cid)
    latest = declarations[0] if declarations else None
    doc_readiness = _get_doc_readiness_safe(cid)
    return compute_customs_readiness_payload(
        case_id=cid,
        declaration=latest,
        doc_readiness=doc_readiness,
        as_of_date=as_of_date,
    )


@_frappe_whitelist()
def get_case_customs_declarations(case_id: str) -> List[Dict[str, Any]]:
    """Return all Customs Declaration records (including line items) for a Trade Case."""
    cid = str(case_id or "").strip()
    return _fetch_case_declarations(cid)


@_frappe_whitelist()
def create_customs_declaration(
    case_id: str,
    trade_type: Optional[str] = None,
    customs_office_code: Optional[str] = None,
    declaration_type: Optional[str] = None,
    shipment_tracking: Optional[str] = None,
    co_form: str = "None",
    currency: str = "USD",
    items: Optional[Any] = None,
) -> Dict[str, Any]:
    """Create a new Customs Declaration (starting in 'Preparing' workflow_status)."""
    cid = str(case_id or "").strip()
    if not cid:
        return {"success": False, "error": "Trade Case ID là bắt buộc."}

    parsed_items: List[Dict[str, Any]] = []
    if isinstance(items, str):
        parsed_items = json.loads(items)
    elif isinstance(items, list):
        parsed_items = [dict(it) for it in items]

    use_db = is_frappe_db_ready()
    resolved_trade_type = trade_type
    resolved_shipment = shipment_tracking
    if use_db and frappe.db.exists("Trade Case", cid):
        tc = frappe.db.get_value(
            "Trade Case", cid, ["trade_type", "shipment_tracking"], as_dict=True
        )
        if tc:
            resolved_trade_type = resolved_trade_type or tc.get("trade_type")
            resolved_shipment = resolved_shipment or tc.get("shipment_tracking")

    resolved_trade_type = resolved_trade_type or "Import"
    default_decl_type = (
        "B11 - Xuất kinh doanh"
        if resolved_trade_type == "Export"
        else "A11 - Nhập kinh doanh tiêu dùng"
    )

    payload = {
        "doctype": "Customs Declaration",
        "trade_case": cid,
        "trade_type": resolved_trade_type,
        "shipment_tracking": resolved_shipment,
        "declaration_type": declaration_type or default_decl_type,
        "customs_office_code": customs_office_code or "",
        "workflow_status": "Preparing",
        "customs_lane": "Not Declared",
        "co_form": co_form or "None",
        "currency": currency or "USD",
        "items": parsed_items,
    }

    if use_db:
        doc = frappe.get_doc(payload)
        doc.insert(ignore_permissions=True)
        out = _doc_to_dict(doc)
    else:
        cd = CustomsDeclaration(payload)
        cd.validate()
        out = in_memory_customs_store.save(cd.as_dict())

    sync_trade_case_customs_metrics(cid)
    return {
        "success": True,
        "name": out["name"],
        "case_id": cid,
        "workflow_status": out["workflow_status"],
        "customs_office_name": out.get("customs_office_name"),
        "total_customs_value": out.get("total_customs_value", 0.0),
        "total_duty_tax": out.get("total_duty_tax", 0.0),
        "items_count": len(out.get("items") or []),
    }


@_frappe_whitelist()
def propose_hs_code(
    declaration_name: str,
    item_idx: int,
    suggested_hs_code: str,
    confidence_score: Optional[float] = None,
    legal_basis: Optional[str] = None,
    source: str = "AI/RAG Suggestion",
) -> Dict[str, Any]:
    """
    Standardized HS Recommendation Slot (ready for future AI/RAG integration).
    Records suggested_hs_code + confidence_score + legal_basis and marks the item
    as 'Proposed' — NEVER auto-approving without explicit specialist review.
    """
    idx = int(item_idx or 0)
    if idx < 1:
        return {"success": False, "error": "item_idx phải >= 1 (1-based)."}
    if not is_valid_hs_code(suggested_hs_code):
        return {
            "success": False,
            "error": f"Mã HS đề xuất '{suggested_hs_code}' không đúng định dạng (4-10 chữ số).",
        }

    normalized = normalize_hs_code(suggested_hs_code)
    use_db = is_frappe_db_ready()

    if use_db:
        if not frappe.db.exists("Customs Declaration", declaration_name):
            return {"success": False, "error": f"Không tìm thấy Customs Declaration '{declaration_name}'."}
        doc = frappe.get_doc("Customs Declaration", declaration_name)
        if idx > len(doc.items or []):
            return {"success": False, "error": f"Không tìm thấy dòng hàng thứ {idx}."}
        row = doc.items[idx - 1]
        row.suggested_hs_code = normalized
        if confidence_score is not None:
            row.hs_confidence_score = float(confidence_score)
        if legal_basis is not None:
            row.hs_legal_basis = legal_basis
        row.hs_source = source or "AI/RAG Suggestion"
        # Submitting a new proposal resets approval state to Proposed
        row.hs_approval_status = "Proposed"
        row.approved_hs_code = None
        row.approved_by = None
        row.approved_at = None
        doc.save(ignore_permissions=True)
        return {
            "success": True,
            "declaration_name": doc.name,
            "item_idx": idx,
            "suggested_hs_code": row.suggested_hs_code,
            "hs_confidence_score": row.hs_confidence_score,
            "hs_source": row.hs_source,
            "hs_approval_status": row.hs_approval_status,
            "hs_approval_summary": doc.hs_approval_summary,
        }

    raw = in_memory_customs_store.get(declaration_name)
    if not raw:
        return {"success": False, "error": f"Không tìm thấy Customs Declaration '{declaration_name}'."}
    updated = dict(raw)
    items = [dict(it) for it in (updated.get("items") or [])]
    if idx > len(items):
        return {"success": False, "error": f"Không tìm thấy dòng hàng thứ {idx}."}

    row = items[idx - 1]
    row["suggested_hs_code"] = normalized
    if confidence_score is not None:
        row["hs_confidence_score"] = float(confidence_score)
    if legal_basis is not None:
        row["hs_legal_basis"] = legal_basis
    row["hs_source"] = source or "AI/RAG Suggestion"
    row["hs_approval_status"] = "Proposed"
    row["approved_hs_code"] = None
    row["approved_by"] = None
    row["approved_at"] = None
    updated["items"] = items

    cd = CustomsDeclaration(updated)
    cd.validate()
    saved = in_memory_customs_store.save(cd.as_dict())
    return {
        "success": True,
        "declaration_name": saved["name"],
        "item_idx": idx,
        "suggested_hs_code": saved["items"][idx - 1]["suggested_hs_code"],
        "hs_confidence_score": saved["items"][idx - 1].get("hs_confidence_score"),
        "hs_source": saved["items"][idx - 1].get("hs_source"),
        "hs_approval_status": saved["items"][idx - 1]["hs_approval_status"],
        "hs_approval_summary": saved.get("hs_approval_summary"),
    }


@_frappe_whitelist()
def suggest_hs_code_with_rag(
    declaration_name: Optional[str] = None,
    item_idx: int = 1,
    item_description: Optional[str] = None,
    material: Optional[str] = None,
    function: Optional[str] = None,
    top_k: int = 5,
    auto_propose: Any = True,
    use_llm: Any = False,
    prefer_postgres: Any = True,
    corpus_nodes: Optional[List[Dict[str, Any]]] = None,
    corpus_edges: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Deep AI/RAG HS Recommendation RPC integrated into Module 4's `propose_hs_code` slot.
    - Queries live PostgreSQL `hs_rag` + Knowledge Graph (+ optional CLIProxyAPI LLM rerank).
    - If `declaration_name` and `auto_propose` are truthy, writes top suggestion into
      `Customs Declaration Item` via `propose_hs_code(..., source='AI/RAG Suggestion')`.
    - STRICT GOVERNANCE: ALWAYS sets `hs_approval_status = 'Proposed'`, NEVER auto-approves.
    """
    def _to_bool(val: Any, default: bool = False) -> bool:
        if isinstance(val, bool):
            return val
        if isinstance(val, (int, float)):
            return bool(val)
        if isinstance(val, str):
            return val.strip().lower() in ("1", "true", "yes", "on")
        return default

    should_propose = _to_bool(auto_propose, True)
    should_use_llm = _to_bool(use_llm, False)
    should_prefer_pg = _to_bool(prefer_postgres, True)
    idx = int(item_idx or 1)

    resolved_desc = (item_description or "").strip()
    row_snapshot: Optional[Dict[str, Any]] = None

    if declaration_name:
        use_db = is_frappe_db_ready()
        if use_db:
            if not frappe.db.exists("Customs Declaration", declaration_name):
                return {
                    "success": False,
                    "error": f"Không tìm thấy Customs Declaration '{declaration_name}'.",
                    "requires_human_approval": True,
                    "automatic_hs_decision": False,
                }
            doc = frappe.get_doc("Customs Declaration", declaration_name)
            items = doc.items or []
            if idx < 1 or idx > len(items):
                return {
                    "success": False,
                    "error": f"Không tìm thấy dòng hàng thứ {idx} trong {declaration_name}.",
                    "requires_human_approval": True,
                    "automatic_hs_decision": False,
                }
            row = items[idx - 1]
            row_snapshot = {
                "item_code": getattr(row, "item_code", None),
                "item_name": getattr(row, "item_name", None),
                "description": getattr(row, "description", None),
            }
        else:
            raw = in_memory_customs_store.get(declaration_name)
            if not raw:
                return {
                    "success": False,
                    "error": f"Không tìm thấy Customs Declaration '{declaration_name}'.",
                    "requires_human_approval": True,
                    "automatic_hs_decision": False,
                }
            items = raw.get("items") or []
            if idx < 1 or idx > len(items):
                return {
                    "success": False,
                    "error": f"Không tìm thấy dòng hàng thứ {idx} trong {declaration_name}.",
                    "requires_human_approval": True,
                    "automatic_hs_decision": False,
                }
            row_snapshot = dict(items[idx - 1])

        if not resolved_desc and row_snapshot:
            resolved_desc = " ".join(
                str(p).strip()
                for p in (row_snapshot.get("item_name"), row_snapshot.get("description"))
                if p and str(p).strip()
            )

    recommendation = recommend_hs_codes(
        item_description=resolved_desc,
        material=material,
        function=function,
        top_k=int(top_k or 5),
        use_llm=should_use_llm,
        prefer_postgres=should_prefer_pg,
        corpus_nodes=corpus_nodes,
        corpus_edges=corpus_edges,
    )

    proposal_result: Optional[Dict[str, Any]] = None
    primary = recommendation.get("primary_recommendation")
    if declaration_name and should_propose and recommendation.get("success") and primary:
        proposal_result = propose_hs_code(
            declaration_name=declaration_name,
            item_idx=idx,
            suggested_hs_code=primary["hs_code"],
            confidence_score=primary.get("confidence_score"),
            legal_basis=primary.get("legal_basis"),
            source="AI/RAG Suggestion",
        )

    return {
        **recommendation,
        "declaration_name": declaration_name,
        "item_idx": idx,
        "item_context": row_snapshot,
        "proposal_applied": bool(proposal_result and proposal_result.get("success")),
        "proposal_result": proposal_result,
        "requires_human_approval": True,
        "automatic_hs_decision": False,
    }


@_frappe_whitelist()
def approve_hs_code(
    declaration_name: str,
    item_idx: int,
    action: str = "approve",
    approved_hs_code: Optional[str] = None,
    notes: Optional[str] = None,
    user: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Human-in-the-loop HS Approval Gate performed by a Customs Specialist.
    - action='approve': confirms approved_hs_code (defaults to suggested_hs_code),
      records approved_by & approved_at, sets hs_approval_status='Approved'.
    - action='reject': sets hs_approval_status='Rejected' and clears approved_hs_code.
    """
    idx = int(item_idx or 0)
    if idx < 1:
        return {"success": False, "error": "item_idx phải >= 1 (1-based)."}

    act = str(action or "approve").strip().lower()
    if act not in ("approve", "reject"):
        return {"success": False, "error": f"Hành động không hợp lệ: {action}"}

    approver = user or _get_current_user()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    use_db = is_frappe_db_ready()

    if use_db:
        if not frappe.db.exists("Customs Declaration", declaration_name):
            return {"success": False, "error": f"Không tìm thấy Customs Declaration '{declaration_name}'."}
        doc = frappe.get_doc("Customs Declaration", declaration_name)
        if idx > len(doc.items or []):
            return {"success": False, "error": f"Không tìm thấy dòng hàng thứ {idx}."}
        row = doc.items[idx - 1]
        if act == "approve":
            final_hs = approved_hs_code or row.suggested_hs_code
            if not is_valid_hs_code(final_hs):
                return {"success": False, "error": f"Mã HS phê duyệt không hợp lệ: '{final_hs}'."}
            row.approved_hs_code = normalize_hs_code(final_hs)
            row.hs_approval_status = "Approved"
            row.approved_by = approver
            row.approved_at = now_str
        else:
            row.hs_approval_status = "Rejected"
            row.approved_hs_code = None
            row.approved_by = None
            row.approved_at = None
        if notes is not None:
            row.approval_notes = notes
        doc.save(ignore_permissions=True)
        return {
            "success": True,
            "declaration_name": doc.name,
            "item_idx": idx,
            "hs_approval_status": row.hs_approval_status,
            "approved_hs_code": row.approved_hs_code,
            "approved_by": row.approved_by,
            "approved_at": str(row.approved_at) if row.approved_at else None,
            "hs_approval_summary": doc.hs_approval_summary,
        }

    raw = in_memory_customs_store.get(declaration_name)
    if not raw:
        return {"success": False, "error": f"Không tìm thấy Customs Declaration '{declaration_name}'."}
    updated = dict(raw)
    items = [dict(it) for it in (updated.get("items") or [])]
    if idx > len(items):
        return {"success": False, "error": f"Không tìm thấy dòng hàng thứ {idx}."}

    row = items[idx - 1]
    if act == "approve":
        final_hs = approved_hs_code or row.get("suggested_hs_code")
        if not is_valid_hs_code(final_hs):
            return {"success": False, "error": f"Mã HS phê duyệt không hợp lệ: '{final_hs}'."}
        row["approved_hs_code"] = normalize_hs_code(final_hs)
        row["hs_approval_status"] = "Approved"
        row["approved_by"] = approver
        row["approved_at"] = now_str
    else:
        row["hs_approval_status"] = "Rejected"
        row["approved_hs_code"] = None
        row["approved_by"] = None
        row["approved_at"] = None
    if notes is not None:
        row["approval_notes"] = notes
    updated["items"] = items

    cd = CustomsDeclaration(updated)
    cd.validate()
    saved = in_memory_customs_store.save(cd.as_dict())
    res_row = saved["items"][idx - 1]
    return {
        "success": True,
        "declaration_name": saved["name"],
        "item_idx": idx,
        "hs_approval_status": res_row["hs_approval_status"],
        "approved_hs_code": res_row.get("approved_hs_code"),
        "approved_by": res_row.get("approved_by"),
        "approved_at": res_row.get("approved_at"),
        "hs_approval_summary": saved.get("hs_approval_summary"),
    }


@_frappe_whitelist()
def advance_customs_workflow(
    declaration_name: str,
    target_status: str,
    declaration_no: Optional[str] = None,
    customs_lane: Optional[str] = None,
    rejection_reason: Optional[str] = None,
    origin_verified: Optional[int] = None,
    customs_value_verified: Optional[int] = None,
    force_skip_doc_check: bool = False,
    as_of_date: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Advance Customs Declaration along the strict 6-state workflow:
        Preparing -> Ready -> Declared -> Processing -> Cleared / Rejected
    Validates:
    - State machine transition legality
    - Document readiness check from document_engine on Ready/Declared (unless overridden)
    - Mandatory HS approval on all items before Declared/Processing/Cleared
    - Updates Trade Case rollup automatically
    """
    tgt = str(target_status or "").strip()
    use_db = is_frappe_db_ready()

    if use_db:
        if not frappe.db.exists("Customs Declaration", declaration_name):
            return {"success": False, "error": f"Không tìm thấy Customs Declaration '{declaration_name}'."}
        doc = frappe.get_doc("Customs Declaration", declaration_name)
        cur_status = doc.workflow_status
        case_id = doc.trade_case
    else:
        raw = in_memory_customs_store.get(declaration_name)
        if not raw:
            return {"success": False, "error": f"Không tìm thấy Customs Declaration '{declaration_name}'."}
        cur_status = raw.get("workflow_status", "Preparing")
        case_id = raw.get("trade_case")

    if not can_transition(cur_status, tgt):
        allowed = ", ".join(ALLOWED_TRANSITIONS.get(cur_status, ())) or "None (Terminal)"
        return {
            "success": False,
            "error": f"Không thể chuyển trạng thái từ '{cur_status}' sang '{tgt}'. Các bước hợp lệ: {allowed}.",
        }

    # Cross-module gate: verify mandatory Trade Documents before Ready/Declared when documents exist
    if tgt in ("Ready", "Declared") and not force_skip_doc_check:
        doc_readiness = _get_doc_readiness_safe(case_id)
        if doc_readiness and doc_readiness.get("total_count", 0) > 0:
            critical_missing = [
                m for m in (doc_readiness.get("missing_urgent") or [])
                if m.get("type") == "critical"
            ]
            if critical_missing:
                names = ", ".join(m.get("name", m.get("code", "")) for m in critical_missing[:3])
                return {
                    "success": False,
                    "error": f"Chặn chuyển sang '{tgt}': Hồ sơ còn {len(critical_missing)} chứng từ khẩn cấp chưa sẵn sàng ({names}).",
                    "missing_critical_docs": critical_missing,
                }

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if use_db:
        doc.workflow_status = tgt
        if declaration_no is not None:
            doc.declaration_no = declaration_no
        if customs_lane is not None:
            doc.customs_lane = customs_lane
        if rejection_reason is not None:
            doc.rejection_reason = rejection_reason
        if origin_verified is not None:
            doc.origin_verified = int(origin_verified)
        if customs_value_verified is not None:
            doc.customs_value_verified = int(customs_value_verified)
        if tgt == "Declared" and not doc.submitted_at:
            doc.submitted_at = now_str
        if as_of_date:
            doc._as_of_date = as_of_date
        try:
            doc.save(ignore_permissions=True)
        except Exception as exc:
            return {"success": False, "error": str(exc)}
        return {
            "success": True,
            "name": doc.name,
            "case_id": doc.trade_case,
            "workflow_status": doc.workflow_status,
            "customs_lane": doc.customs_lane,
            "declaration_no": doc.declaration_no,
            "clearance_status": doc.clearance_status,
            "clearance_date": str(doc.clearance_date) if doc.clearance_date else None,
        }

    # In-memory standalone mode
    updated = dict(raw)
    updated["workflow_status"] = tgt
    if declaration_no is not None:
        updated["declaration_no"] = declaration_no
    if customs_lane is not None:
        updated["customs_lane"] = customs_lane
    if rejection_reason is not None:
        updated["rejection_reason"] = rejection_reason
    if origin_verified is not None:
        updated["origin_verified"] = int(origin_verified)
    if customs_value_verified is not None:
        updated["customs_value_verified"] = int(customs_value_verified)
    if tgt == "Declared" and not updated.get("submitted_at"):
        updated["submitted_at"] = now_str
    if as_of_date:
        updated["_as_of_date"] = as_of_date

    cd = CustomsDeclaration(updated)
    try:
        cd.validate()
    except Exception as exc:
        return {"success": False, "error": str(exc)}

    saved = in_memory_customs_store.save(cd.as_dict())
    sync_trade_case_customs_metrics(case_id)
    return {
        "success": True,
        "name": saved["name"],
        "case_id": saved.get("trade_case"),
        "workflow_status": saved["workflow_status"],
        "customs_lane": saved.get("customs_lane"),
        "declaration_no": saved.get("declaration_no"),
        "clearance_status": saved.get("clearance_status"),
        "clearance_date": saved.get("clearance_date"),
    }


def sync_trade_case_customs_metrics(case_id: str) -> Dict[str, Any]:
    """
    Roll up customs_declaration_no, customs_lane, and customs_cleared summary onto Trade Case
    (Zero Data Duplication).
    """
    cid = str(case_id or "").strip()
    declarations = _fetch_case_declarations(cid)
    latest = declarations[0] if declarations else None

    decl_no = (latest.get("declaration_no") or "") if latest else ""
    lane = (latest.get("customs_lane") or "Not Declared") if latest else "Not Declared"
    cleared = 1 if (latest and latest.get("workflow_status") == "Cleared") else 0

    if is_frappe_db_ready() and frappe.db.exists("Trade Case", cid):
        try:
            frappe.db.set_value(
                "Trade Case",
                cid,
                {
                    "customs_declaration_no": decl_no,
                    "customs_lane": lane,
                    "customs_cleared": cleared,
                },
                update_modified=False,
            )
        except Exception:
            pass

    return {
        "case_id": cid,
        "customs_declaration_no": decl_no,
        "customs_lane": lane,
        "customs_cleared": cleared,
    }


def scheduled_check_overdue_customs(as_of_date: Optional[str] = None) -> Dict[str, Any]:
    """
    Daily scheduler job: detect active Declared/Processing customs declarations
    exceeding customs_max_processing_days threshold and update processing_days.
    """
    today_dt = parse_date_safe(as_of_date) or date.today()
    use_db = is_frappe_db_ready()

    if use_db:
        rows = frappe.get_all(
            "Customs Declaration",
            filters={"workflow_status": ["in", ["Declared", "Processing"]]},
            fields=[
                "name", "trade_case", "declaration_no", "workflow_status",
                "customs_lane", "declaration_date", "clearance_date", "processing_days",
            ],
        ) or []
        decls = [dict(r) if isinstance(r, dict) else r.as_dict() for r in rows]
    else:
        decls = [
            d for d in in_memory_customs_store.declarations.values()
            if d.get("workflow_status") in ("Declared", "Processing")
        ]

    overdue_records: List[Dict[str, Any]] = []
    for d in decls:
        overdue, elapsed = is_declaration_overdue(d, as_of_date=today_dt)
        if use_db:
            frappe.db.set_value(
                "Customs Declaration", d["name"], "processing_days", elapsed, update_modified=False
            )
        else:
            d["processing_days"] = elapsed
            in_memory_customs_store.save(d)

        if overdue:
            overdue_records.append(
                {
                    "name": d["name"],
                    "trade_case": d.get("trade_case"),
                    "declaration_no": d.get("declaration_no"),
                    "customs_lane": d.get("customs_lane"),
                    "processing_days": elapsed,
                }
            )

    if use_db and decls:
        try:
            frappe.db.commit()
        except Exception:
            pass

    return {
        "success": True,
        "scanned_count": len(decls),
        "overdue_count": len(overdue_records),
        "overdue_declarations": overdue_records,
    }


__all__ = [
    "InMemoryCustomsStore",
    "in_memory_customs_store",
    "is_frappe_db_ready",
    "get_case_customs_status",
    "get_case_customs_declarations",
    "create_customs_declaration",
    "propose_hs_code",
    "suggest_hs_code_with_rag",
    "approve_hs_code",
    "advance_customs_workflow",
    "sync_trade_case_customs_metrics",
    "scheduled_check_overdue_customs",
]
