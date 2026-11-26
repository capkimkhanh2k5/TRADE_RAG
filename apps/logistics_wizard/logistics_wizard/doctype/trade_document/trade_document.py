# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

from datetime import date, datetime
from typing import Any, Optional

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

        def append(self, table_field, value):
            if not hasattr(self, table_field) or getattr(self, table_field) is None:
                setattr(self, table_field, [])
            table = getattr(self, table_field)
            table.append(value)
            return value

        def as_dict(self):
            return dict(self.__dict__)


def _parse_date_safe(val: Any) -> Optional[date]:
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


def _raise_validation_error(msg: str) -> None:
    if frappe and hasattr(frappe, "throw"):
        frappe.throw(msg)
    raise ValueError(msg)


def _get_current_user() -> str:
    if frappe and getattr(frappe, "session", None) and getattr(frappe.session, "user", None):
        return str(frappe.session.user)
    return "Administrator"


class TradeDocument(Document):
    """
    Master DocType for Trade Document Management (Module 3).
    Manages import/export document checklist items, file version history,
    expiry enforcement, verification workflow, and readiness rollup to Trade Case.
    """

    VALID_STATUSES = ("Required", "Received", "Verified", "Missing", "Expired", "N/A")
    VALID_CATEGORIES = ("Commercial", "Transport", "Customs", "Compliance")

    def validate(self):
        if not getattr(self, "naming_series", None):
            self.naming_series = "TDOC-.YYYY.-.#####"
        if not getattr(self, "status", None):
            self.status = "Required"
        if not getattr(self, "category", None):
            self.category = "Commercial"
        if self.status not in self.VALID_STATUSES:
            _raise_validation_error(
                _("Trạng thái chứng từ không hợp lệ: {0}").format(self.status)
            )
        if self.category not in self.VALID_CATEGORIES:
            _raise_validation_error(
                _("Nhóm chứng từ không hợp lệ: {0}").format(self.category)
            )

        # 1. Validate issue_date vs expiry_date
        issue_dt = _parse_date_safe(getattr(self, "issue_date", None))
        expiry_dt = _parse_date_safe(getattr(self, "expiry_date", None))
        if issue_dt and expiry_dt and expiry_dt < issue_dt:
            _raise_validation_error(
                _("Ngày hết hạn ({0}) không thể nhỏ hơn ngày phát hành ({1}).").format(
                    expiry_dt, issue_dt
                )
            )

        # 2. Track file version history when a new file_url is attached
        self._sync_file_version_history()

        # 3. Automatically flag Expired if past expiry_date
        as_of = _parse_date_safe(getattr(self, "_as_of_date", None)) or date.today()
        if expiry_dt and expiry_dt < as_of and self.status not in ("N/A", "Expired"):
            self.status = "Expired"

        # 4. Enforce verification rule: mandatory documents must have a file attached
        if self.status == "Verified":
            is_mandatory = int(getattr(self, "is_mandatory", 1) or 0) == 1
            file_url = str(getattr(self, "file_url", "") or "").strip()
            if is_mandatory and not file_url:
                _raise_validation_error(
                    _("Chứng từ bắt buộc '{0}' chưa có tệp đính kèm, không thể xác nhận Verified.").format(
                        getattr(self, "document_name", None) or getattr(self, "document_code", "N/A")
                    )
                )
            if not getattr(self, "verified_at", None):
                self.verified_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if not getattr(self, "verified_by", None):
                self.verified_by = _get_current_user()

    def _sync_file_version_history(self):
        file_url = str(getattr(self, "file_url", "") or "").strip()
        versions = getattr(self, "versions", None)
        if versions is None:
            self.versions = []
            versions = self.versions

        if file_url:
            latest_file = None
            max_ver = 0
            for v in versions:
                v_num = int((v.get("version_number") if isinstance(v, dict) else getattr(v, "version_number", 0)) or 0)
                if v_num >= max_ver:
                    max_ver = v_num
                    latest_file = (v.get("file_url") if isinstance(v, dict) else getattr(v, "file_url", None))

            if latest_file != file_url:
                next_ver = max_ver + 1
                notes = getattr(self, "_pending_change_notes", None) or f"Uploaded version v{next_ver}"
                uploader = getattr(self, "_pending_uploaded_by", None) or _get_current_user()
                self.append(
                    "versions",
                    {
                        "version_number": next_ver,
                        "file_url": file_url,
                        "uploaded_by": uploader,
                        "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "change_notes": notes,
                    },
                )
                self.current_version = next_ver
                if self.status in ("Required", "Missing") or (max_ver > 0 and self.status in ("Verified", "Expired")):
                    self.status = "Received"
                    self.verified_by = None
                    self.verified_at = None
            else:
                self.current_version = max(int(getattr(self, "current_version", 0) or 0), max_ver)
        else:
            self.current_version = max(int(getattr(self, "current_version", 0) or 0), len(versions))

    def _trigger_case_rollup(self):
        case_id = getattr(self, "trade_case", None)
        if not case_id:
            return
        try:
            from logistics_wizard.document_engine.api import sync_trade_case_document_metrics
            sync_trade_case_document_metrics(case_id)
        except Exception:
            pass

    def after_insert(self):
        self._trigger_case_rollup()

    def on_update(self):
        self._trigger_case_rollup()

    def on_trash(self):
        self._trigger_case_rollup()
