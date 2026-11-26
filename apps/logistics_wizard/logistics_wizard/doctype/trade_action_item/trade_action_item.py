# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

from datetime import datetime

try:
    import frappe
    from frappe.model.document import Document
except ImportError:
    frappe = None

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


class TradeActionItem(Document):
    """Actionable follow-up task linked to a Trade Case and optionally a Shipment Exception."""

    def validate(self):
        if not getattr(self, "naming_series", None):
            self.naming_series = "TACT-.YYYY.-.#####"
        if not getattr(self, "status", None):
            self.status = "Open"
        if not getattr(self, "department", None):
            self.department = "Logistics"
        if not getattr(self, "owner_name", None) and getattr(self, "owner_user", None):
            self.owner_name = str(self.owner_user)
        if self.status == "Completed":
            if not getattr(self, "completed_at", None):
                self.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if not getattr(self, "completed_by", None):
                user = (
                    getattr(getattr(frappe, "session", None), "user", None)
                    if frappe
                    else None
                )
                self.completed_by = user or "Administrator"
