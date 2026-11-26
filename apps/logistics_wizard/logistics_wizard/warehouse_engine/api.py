# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""
warehouse_engine.api — Public API Facade & Section 3.4 Data Contract
=====================================================================
Implements:
- get_case_warehouse_status(case_id)   [Section 3.4 exact contract]
- schedule_warehouse_receiving(case_id, ...)
- record_warehouse_inspection(receipt_name, ...)
- on_purchase_receipt_submit(doc, method=None)
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    import frappe
except ImportError:
    frappe = None

from logistics_wizard.doctype.trade_warehouse_receipt.trade_warehouse_receipt import (
    TradeWarehouseReceipt,
)


def _frappe_whitelist():
    if frappe and hasattr(frappe, "whitelist"):
        return frappe.whitelist(allow_guest=True)
    return lambda fn: fn


class InMemoryWarehouseStore:
    """In-memory store enabling fast standalone unit testing without MariaDB."""

    def __init__(self):
        self.receipts: Dict[str, Dict[str, Any]] = {}
        self._seq: int = 0

    def reset(self) -> None:
        self.receipts.clear()
        self._seq = 0

    def next_name(self) -> str:
        self._seq += 1
        return f"TWHR-{datetime.now().year}-{self._seq:05d}"

    def save(self, doc_dict: Dict[str, Any]) -> Dict[str, Any]:
        name = doc_dict.get("name") or self.next_name()
        doc_dict["name"] = name
        self.receipts[name] = doc_dict
        return doc_dict

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        return self.receipts.get(name)

    def list_by_case(self, case_id: str) -> List[Dict[str, Any]]:
        return [
            r for r in self.receipts.values()
            if str(r.get("trade_case") or "") == str(case_id)
        ]


in_memory_warehouse_store = InMemoryWarehouseStore()


def is_frappe_db_ready() -> bool:
    if not (frappe and getattr(frappe, "db", None)):
        return False
    exists_fn = getattr(frappe.db, "exists", None)
    if not callable(exists_fn):
        return False
    try:
        return bool(exists_fn("DocType", "Trade Warehouse Receipt"))
    except Exception:
        return False


def _to_dict(doc: Any) -> Dict[str, Any]:
    if isinstance(doc, dict):
        return dict(doc)
    if callable(getattr(doc, "as_dict", None)):
        return doc.as_dict()
    return dict(doc.__dict__)


def _fetch_latest_receipt(case_id: str) -> Optional[Dict[str, Any]]:
    if is_frappe_db_ready():
        names = frappe.get_all(
            "Trade Warehouse Receipt",
            filters={"trade_case": case_id},
            pluck="name",
            order_by="modified desc",
            limit=1,
        ) or []
        if not names:
            return None
        return _to_dict(frappe.get_doc("Trade Warehouse Receipt", names[0]))

    rows = in_memory_warehouse_store.list_by_case(case_id)
    return rows[-1] if rows else None


@_frappe_whitelist()
def get_case_warehouse_status(case_id: str) -> Dict[str, Any]:
    """
    Exact Section 3.4 API contract for Trade Case Overview:
    logistics_wizard.warehouse_engine.api.get_case_warehouse_status(case_id)
    """
    cid = str(case_id or "").strip()
    rec = _fetch_latest_receipt(cid)
    if not rec:
        return {
            "case_id": cid,
            "has_receipt": False,
            "receipt_name": None,
            "expected_arrival": None,
            "warehouse": None,
            "receiving_status": "NOT READY",
            "expected_qty": 0,
            "received_qty": None,
            "missing_qty": 0,
            "damaged_qty": 0,
            "space_reserved": False,
            "receiving_team": None,
            "discrepancy_alert": False,
            "discrepancy_details": None,
            "purchase_receipt": None,
            "delivery_note": None,
        }

    status = str(rec.get("receiving_status") or "NOT READY")
    rec_qty = rec.get("received_qty")
    if status in ("NOT READY", "SCHEDULED") and (rec_qty is None or float(rec_qty or 0) == 0):
        rec_qty_out = None
    else:
        rec_qty_out = float(rec_qty or 0)

    return {
        "case_id": cid,
        "has_receipt": True,
        "receipt_name": rec.get("name"),
        "expected_arrival": str(rec.get("expected_arrival")) if rec.get("expected_arrival") else None,
        "actual_arrival": str(rec.get("actual_arrival")) if rec.get("actual_arrival") else None,
        "warehouse": rec.get("warehouse"),
        "receiving_status": status,
        "expected_qty": float(rec.get("expected_qty") or 0),
        "received_qty": rec_qty_out,
        "missing_qty": float(rec.get("missing_qty") or 0),
        "damaged_qty": float(rec.get("damaged_qty") or 0),
        "space_reserved": bool(int(rec.get("space_reserved") or 0)),
        "receiving_team": rec.get("receiving_team"),
        "container_seal_intact": bool(
            int(rec.get("container_seal_intact") if rec.get("container_seal_intact") is not None else 1)
        ),
        "discrepancy_alert": bool(int(rec.get("discrepancy_alert") or 0)),
        "discrepancy_details": rec.get("discrepancy_details") or None,
        "purchase_receipt": rec.get("purchase_receipt") or None,
        "delivery_note": rec.get("delivery_note") or None,
    }


@_frappe_whitelist()
def schedule_warehouse_receiving(
    case_id: str,
    warehouse: str,
    expected_arrival: Optional[str] = None,
    expected_qty: float = 0,
    space_reserved: int = 1,
    receiving_team: Optional[str] = None,
    shipment_tracking: Optional[str] = None,
    trade_type: Optional[str] = None,
) -> Dict[str, Any]:
    """Create or update a Trade Warehouse Receipt plan for a Trade Case."""
    cid = str(case_id or "").strip()
    if not cid:
        return {"success": False, "error": "Trade Case ID là bắt buộc."}

    use_db = is_frappe_db_ready()
    if use_db:
        existing_name = frappe.db.get_value(
            "Trade Warehouse Receipt", {"trade_case": cid}, "name"
        )
        if existing_name:
            doc = frappe.get_doc("Trade Warehouse Receipt", existing_name)
        else:
            doc = frappe.get_doc(
                {
                    "doctype": "Trade Warehouse Receipt",
                    "trade_case": cid,
                    "trade_type": trade_type or "Import",
                }
            )
        doc.warehouse = warehouse
        if expected_arrival is not None:
            doc.expected_arrival = expected_arrival
        doc.expected_qty = float(expected_qty or 0)
        doc.space_reserved = int(space_reserved or 0)
        if receiving_team is not None:
            doc.receiving_team = receiving_team
        if shipment_tracking is not None:
            doc.shipment_tracking = shipment_tracking
        if doc.receiving_status == "NOT READY" and int(doc.space_reserved or 0) == 1:
            doc.receiving_status = "SCHEDULED"

        if existing_name:
            doc.save(ignore_permissions=True)
        else:
            doc.insert(ignore_permissions=True)
        saved = _to_dict(doc)
    else:
        existing = _fetch_latest_receipt(cid)
        raw = dict(existing) if existing else {
            "trade_case": cid,
            "trade_type": trade_type or "Import",
            "receiving_status": "NOT READY",
        }
        raw["warehouse"] = warehouse
        if expected_arrival is not None:
            raw["expected_arrival"] = expected_arrival
        raw["expected_qty"] = float(expected_qty or 0)
        raw["space_reserved"] = int(space_reserved or 0)
        if receiving_team is not None:
            raw["receiving_team"] = receiving_team
        if shipment_tracking is not None:
            raw["shipment_tracking"] = shipment_tracking
        if raw.get("receiving_status") == "NOT READY" and int(raw.get("space_reserved") or 0) == 1:
            raw["receiving_status"] = "SCHEDULED"

        wh = TradeWarehouseReceipt(raw)
        wh.validate()
        saved = in_memory_warehouse_store.save(wh.as_dict())

    return {
        "success": True,
        "name": saved["name"],
        "case_id": cid,
        "warehouse": saved.get("warehouse"),
        "receiving_status": saved.get("receiving_status"),
        "expected_qty": saved.get("expected_qty"),
        "space_reserved": bool(int(saved.get("space_reserved") or 0)),
    }


@_frappe_whitelist()
def record_warehouse_inspection(
    receipt_name: str,
    received_qty: float,
    damaged_qty: float = 0,
    container_seal_intact: int = 1,
    actual_arrival: Optional[str] = None,
    purchase_receipt: Optional[str] = None,
    delivery_note: Optional[str] = None,
    finalize_if_clean: bool = True,
    remarks: Optional[str] = None,
    user: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Record physical unloading & KCS inspection quantities.
    - If missing_qty > 0 or damaged_qty > 0 or seal broken -> marks DISCREPANCY
      and automatically raises a Warehouse Discrepancy exception (Scenario 4).
    - If clean and finalize_if_clean=True -> marks COMPLETED.
    """
    use_db = is_frappe_db_ready()
    if use_db:
        if not frappe.db.exists("Trade Warehouse Receipt", receipt_name):
            return {"success": False, "error": f"Không tìm thấy phiếu kho '{receipt_name}'."}
        doc = frappe.get_doc("Trade Warehouse Receipt", receipt_name)
        doc.received_qty = float(received_qty)
        doc.damaged_qty = float(damaged_qty or 0)
        doc.container_seal_intact = int(container_seal_intact)
        if actual_arrival:
            doc.actual_arrival = actual_arrival
        if purchase_receipt:
            doc.purchase_receipt = purchase_receipt
        if delivery_note:
            doc.delivery_note = delivery_note
        if remarks is not None:
            doc.remarks = remarks
        if user:
            doc.inspected_by = user
        doc.receiving_status = "INSPECTING"
        try:
            doc.save(ignore_permissions=True)
            if int(doc.discrepancy_alert or 0) == 0 and finalize_if_clean:
                doc.receiving_status = "COMPLETED"
                doc.save(ignore_permissions=True)
        except Exception as exc:
            return {"success": False, "error": str(exc)}
        saved = _to_dict(doc)
    else:
        raw = in_memory_warehouse_store.get(receipt_name)
        if not raw:
            return {"success": False, "error": f"Không tìm thấy phiếu kho '{receipt_name}'."}
        updated = dict(raw)
        updated["received_qty"] = float(received_qty)
        updated["damaged_qty"] = float(damaged_qty or 0)
        updated["container_seal_intact"] = int(container_seal_intact)
        if actual_arrival:
            updated["actual_arrival"] = actual_arrival
        if purchase_receipt:
            updated["purchase_receipt"] = purchase_receipt
        if delivery_note:
            updated["delivery_note"] = delivery_note
        if remarks is not None:
            updated["remarks"] = remarks
        if user:
            updated["inspected_by"] = user
        updated["receiving_status"] = "INSPECTING"

        wh = TradeWarehouseReceipt(updated)
        try:
            wh.validate()
        except Exception as exc:
            return {"success": False, "error": str(exc)}
        if int(wh.discrepancy_alert or 0) == 0 and finalize_if_clean:
            wh.receiving_status = "COMPLETED"
        saved = in_memory_warehouse_store.save(wh.as_dict())
        if int(wh.discrepancy_alert or 0) == 1:
            wh.name = saved["name"]
            wh._trigger_discrepancy_exception()

    return {
        "success": True,
        "name": saved["name"],
        "case_id": saved.get("trade_case"),
        "receiving_status": saved.get("receiving_status"),
        "expected_qty": float(saved.get("expected_qty") or 0),
        "received_qty": float(saved.get("received_qty") or 0),
        "missing_qty": float(saved.get("missing_qty") or 0),
        "damaged_qty": float(saved.get("damaged_qty") or 0),
        "discrepancy_alert": bool(int(saved.get("discrepancy_alert") or 0)),
        "discrepancy_details": saved.get("discrepancy_details") or None,
    }


def on_purchase_receipt_submit(doc, method=None) -> None:
    """Link submitted ERPNext Purchase Receipt back to matching Trade Warehouse Receipt."""
    if not is_frappe_db_ready():
        return
    try:
        po_names = {
            getattr(it, "purchase_order", None)
            for it in (getattr(doc, "items", None) or [])
            if getattr(it, "purchase_order", None)
        }
        if not po_names:
            return
        case_id = frappe.db.get_value(
            "Trade Case", {"purchase_order": ["in", list(po_names)]}, "name"
        )
        if not case_id:
            return
        receipt_name = frappe.db.get_value(
            "Trade Warehouse Receipt", {"trade_case": case_id}, "name"
        )
        if receipt_name:
            frappe.db.set_value(
                "Trade Warehouse Receipt",
                receipt_name,
                {"purchase_receipt": doc.name},
                update_modified=False,
            )
    except Exception:
        pass


__all__ = [
    "InMemoryWarehouseStore",
    "in_memory_warehouse_store",
    "is_frappe_db_ready",
    "get_case_warehouse_status",
    "schedule_warehouse_receiving",
    "record_warehouse_inspection",
    "on_purchase_receipt_submit",
]
