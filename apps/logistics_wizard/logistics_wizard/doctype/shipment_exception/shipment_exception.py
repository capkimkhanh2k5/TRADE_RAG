# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

from datetime import datetime

try:
    import frappe
    from frappe import _
    from frappe.model.document import Document
except ImportError:
    frappe = None
    _ = lambda msg: msg

    class Document:
        def __init__(self, *args, **kwargs):
            self.__dict__.update(kwargs)
            if args and isinstance(args[0], dict):
                self.__dict__.update(args[0])

        def get(self, key, default=None):
            return getattr(self, key, default)

        def set(self, key, value):
            setattr(self, key, value)

        def as_dict(self):
            return dict(self.__dict__)


def _raise_validation_error(msg: str) -> None:
    if frappe and hasattr(frappe, "throw"):
        frappe.throw(msg)
    raise ValueError(msg)


def _get_current_user() -> str:
    if frappe and getattr(frappe, "session", None) and getattr(frappe.session, "user", None):
        return str(frappe.session.user)
    return "Administrator"


class ShipmentException(Document):
    """
    Unified Trade & Shipment Exception DocType (Module 6).
    Covers all 8 exception rules across Shipment, Document, Customs, Costing, and Warehouse,
    with ownership assignment, escalation levels, audit trail, and Trade Case health rollup.
    """

    def validate(self):
        if not getattr(self, "trade_case", None) and not getattr(self, "shipment_tracking", None):
            _raise_validation_error(
                _("Sự cố phải gắn với ít nhất một Hồ sơ XNK (Trade Case) hoặc Vận đơn (Shipment Tracking).")
            )

        # Backfill trade_case from shipment_tracking when possible in DB mode
        if (
            not getattr(self, "trade_case", None)
            and getattr(self, "shipment_tracking", None)
            and frappe
            and getattr(frappe, "db", None)
            and frappe.db.exists("Shipment Tracking", self.shipment_tracking)
        ):
            try:
                tc = frappe.db.get_value("Shipment Tracking", self.shipment_tracking, "trade_case")
                if tc:
                    self.trade_case = tc
            except Exception:
                pass

        if not getattr(self, "status", None):
            self.status = "Open"
        if not getattr(self, "severity", None):
            self.severity = "Warning"
        if not getattr(self, "raised_at", None):
            self.raised_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not getattr(self, "title", None):
            exc_type = getattr(self, "exception_type", "Exception")
            desc = str(getattr(self, "description", "") or "")
            self.title = f"{exc_type}: {desc[:90]}" if desc else str(exc_type)

        if self.status in ("Resolved", "Closed"):
            if not getattr(self, "resolved_at", None):
                self.resolved_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if not getattr(self, "resolved_by", None):
                self.resolved_by = _get_current_user()

    def _trigger_case_health_rollup(self):
        case_id = getattr(self, "trade_case", None)
        if not case_id:
            return
        try:
            from logistics_wizard.exception_engine.api import sync_trade_case_exception_and_health
            sync_trade_case_exception_and_health(case_id)
        except Exception:
            pass

    def after_insert(self):
        self._trigger_case_health_rollup()

    def on_update(self):
        self._trigger_case_health_rollup()

    def on_trash(self):
        self._trigger_case_health_rollup()
