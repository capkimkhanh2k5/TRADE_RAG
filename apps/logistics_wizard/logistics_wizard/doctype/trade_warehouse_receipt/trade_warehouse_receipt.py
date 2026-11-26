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


class TradeWarehouseReceipt(Document):
    """
    Warehouse Receiving & Inspection record for a Trade Case (Section 3.4 & Scenario 4).
    Tracks warehouse reservation, unloading inspection, Expected vs Received/Missing/Damaged
    quantities, ERPNext Purchase Receipt link, and auto-triggers Warehouse Discrepancy alerts.
    """

    VALID_STATUSES = (
        "NOT READY",
        "SCHEDULED",
        "IN PROGRESS",
        "INSPECTING",
        "DISCREPANCY",
        "COMPLETED",
    )

    def validate(self):
        if not getattr(self, "naming_series", None):
            self.naming_series = "TWHR-.YYYY.-.#####"
        if not getattr(self, "trade_type", None):
            self.trade_type = "Import"
        if not getattr(self, "receiving_status", None):
            self.receiving_status = "NOT READY"
        if self.receiving_status not in self.VALID_STATUSES:
            _raise_validation_error(
                _("Trạng thái tiếp nhận kho không hợp lệ: {0}").format(self.receiving_status)
            )

        expected = float(getattr(self, "expected_qty", 0) or 0)
        received = getattr(self, "received_qty", None)
        damaged = float(getattr(self, "damaged_qty", 0) or 0)
        seal_intact = int(getattr(self, "container_seal_intact", 1) if getattr(self, "container_seal_intact", None) is not None else 1)

        if expected < 0 or (received is not None and float(received) < 0) or damaged < 0:
            _raise_validation_error(_("Số lượng kiểm đếm kho không được âm."))

        has_count = (
            received is not None
            and (
                float(received) > 0
                or self.receiving_status in ("INSPECTING", "DISCREPANCY", "COMPLETED")
            )
        )
        if has_count:
            rec_val = float(received or 0)
            if damaged > rec_val and rec_val > 0:
                _raise_validation_error(
                    _("Số lượng hư hỏng ({0}) không thể lớn hơn số lượng thực nhận ({1}).").format(
                        damaged, rec_val
                    )
                )
            missing = max(0.0, round(expected - rec_val, 3))
            self.missing_qty = missing

            has_discrepancy = (missing > 0) or (damaged > 0) or (seal_intact == 0)
            self.discrepancy_alert = 1 if has_discrepancy else 0

            if has_discrepancy:
                parts = [f"Expected: {expected:g}", f"Received: {rec_val:g}"]
                if missing > 0:
                    parts.append(f"Missing: {missing:g}")
                if damaged > 0:
                    parts.append(f"Damaged: {damaged:g}")
                if seal_intact == 0:
                    parts.append("Seal Broken")
                self.discrepancy_details = f"DISCREPANCY DETECTED ({' / '.join(parts)})"
                if self.receiving_status in ("IN PROGRESS", "INSPECTING"):
                    self.receiving_status = "DISCREPANCY"
            else:
                self.discrepancy_details = ""

            if not getattr(self, "inspected_at", None):
                self.inspected_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if not getattr(self, "inspected_by", None):
                self.inspected_by = _get_current_user()
        else:
            self.missing_qty = 0.0
            self.discrepancy_alert = 0
            self.discrepancy_details = ""
            if (
                self.receiving_status == "NOT READY"
                and int(getattr(self, "space_reserved", 0) or 0) == 1
                and getattr(self, "expected_arrival", None)
            ):
                self.receiving_status = "SCHEDULED"

    def _trigger_discrepancy_exception(self):
        if int(getattr(self, "discrepancy_alert", 0) or 0) != 1:
            return
        case_id = getattr(self, "trade_case", None)
        if not case_id:
            return
        try:
            from logistics_wizard.exception_engine.api import raise_exception_from_rule
            raise_exception_from_rule(
                case_id=case_id,
                rule_code="RULE_08_WAREHOUSE_DISCREPANCY",
                exception_type="Warehouse Discrepancy",
                severity="Critical" if float(getattr(self, "damaged_qty", 0) or 0) > 0 or int(getattr(self, "container_seal_intact", 1) or 0) == 0 else "High",
                title=f"Bất thường nhập kho: {getattr(self, 'discrepancy_details', '')}",
                description=getattr(self, "discrepancy_details", "") or "Phát hiện chênh lệch số lượng/hư hỏng khi dỡ container tại kho.",
                department="Warehouse",
                source_module="Warehouse",
                shipment_tracking=getattr(self, "shipment_tracking", None),
                reference_doctype="Trade Warehouse Receipt",
                reference_name=getattr(self, "name", None),
            )
        except Exception:
            pass

    def after_insert(self):
        self._trigger_discrepancy_exception()

    def on_update(self):
        self._trigger_discrepancy_exception()
