# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

from datetime import date, datetime
import re
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


HS_CODE_PATTERN = re.compile(r"^\d{4}(\.?\d{2}){0,3}$")


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


def _item_get(item: Any, key: str, default: Any = None) -> Any:
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)


def _item_set(item: Any, key: str, value: Any) -> None:
    if isinstance(item, dict):
        item[key] = value
    else:
        setattr(item, key, value)


def _is_valid_hs_code(code: Optional[str]) -> bool:
    if not code:
        return False
    cleaned = str(code).strip()
    return bool(HS_CODE_PATTERN.match(cleaned))


class CustomsDeclaration(Document):
    """
    Master DocType for Module 4: Customs & Trade Compliance.
    Enforces:
    - Workflow lifecycle: Preparing -> Ready -> Declared -> Processing -> Cleared / Rejected
    - Human-in-the-loop HS approval gate before declaration/clearance
    - Duty & tax auto-calculation (Import/Export Duty, Special Consumption Tax, VAT)
    - Customs office master lookup and Trade Case summary rollup
    """

    VALID_WORKFLOW_STATUSES = (
        "Preparing",
        "Ready",
        "Declared",
        "Processing",
        "Cleared",
        "Rejected",
    )
    VALID_LANES = ("Not Declared", "Green", "Yellow", "Red")

    def validate(self):
        if not getattr(self, "naming_series", None):
            self.naming_series = "CDEC-.YYYY.-.#####"
        if not getattr(self, "trade_type", None):
            self.trade_type = "Import"
        if not getattr(self, "workflow_status", None):
            self.workflow_status = "Preparing"
        if not getattr(self, "customs_lane", None):
            self.customs_lane = "Not Declared"
        if not getattr(self, "currency", None):
            self.currency = "USD"
        if not getattr(self, "exchange_rate", None):
            self.exchange_rate = 1.0

        if self.workflow_status not in self.VALID_WORKFLOW_STATUSES:
            _raise_validation_error(
                _("Trạng thái tờ khai không hợp lệ: {0}").format(self.workflow_status)
            )
        if self.customs_lane not in self.VALID_LANES:
            _raise_validation_error(
                _("Phân luồng hải quan không hợp lệ: {0}").format(self.customs_lane)
            )

        self._resolve_customs_office_name()
        self._calculate_items_and_taxes()
        self._enforce_hs_and_declaration_gates()
        self._sync_clearance_and_processing_days()

    def _resolve_customs_office_name(self):
        code = str(getattr(self, "customs_office_code", "") or "").strip().upper()
        if not hasattr(self, "customs_office_name"):
            self.customs_office_name = ""
        if not code:
            return
        self.customs_office_code = code
        if self.customs_office_name:
            return
        try:
            from logistics_wizard.master_config import CUSTOMS_OFFICES_VN
            for office in CUSTOMS_OFFICES_VN:
                if str(office.get("code", "")).upper() == code or str(office.get("port_code", "")).upper() == code:
                    self.customs_office_name = office.get("name", "")
                    self.customs_office_code = office.get("code", code)
                    break
        except Exception:
            pass

    def _calculate_items_and_taxes(self):
        items = getattr(self, "items", None) or []
        total_val = 0.0
        total_duty = 0.0
        total_sct = 0.0
        total_vat = 0.0

        approved_count = 0
        primary_hs = None
        any_license_required = False
        any_inspection_required = False

        for idx, item in enumerate(items, start=1):
            qty = float(_item_get(item, "qty", 0) or 0)
            unit_price = float(_item_get(item, "unit_price", 0) or 0)
            customs_value = float(_item_get(item, "customs_value", 0) or 0)
            if customs_value <= 0 and qty > 0 and unit_price > 0:
                customs_value = round(qty * unit_price, 2)
                _item_set(item, "customs_value", customs_value)

            duty_rate = float(_item_get(item, "import_duty_rate", 0) or 0)
            sct_rate = float(_item_get(item, "special_consumption_tax_rate", 0) or 0)
            vat_rate = float(_item_get(item, "vat_rate", 0) or 0)

            duty_amt = round(customs_value * duty_rate / 100.0, 2)
            sct_amt = round((customs_value + duty_amt) * sct_rate / 100.0, 2)
            vat_amt = round((customs_value + duty_amt + sct_amt) * vat_rate / 100.0, 2)
            line_tax = round(duty_amt + sct_amt + vat_amt, 2)

            _item_set(item, "import_duty_amount", duty_amt)
            _item_set(item, "special_consumption_tax_amount", sct_amt)
            _item_set(item, "vat_amount", vat_amt)
            _item_set(item, "total_tax_amount", line_tax)

            total_val += customs_value
            total_duty += duty_amt
            total_sct += sct_amt
            total_vat += vat_amt

            # HS code syntax check if provided
            suggested_hs = str(_item_get(item, "suggested_hs_code", "") or "").strip()
            approved_hs = str(_item_get(item, "approved_hs_code", "") or "").strip()
            hs_status = str(_item_get(item, "hs_approval_status", "Pending") or "Pending")

            if suggested_hs and not _is_valid_hs_code(suggested_hs):
                _raise_validation_error(
                    _("Dòng {0}: Mã HS đề xuất '{1}' không đúng định dạng chuẩn (4-10 chữ số).").format(
                        idx, suggested_hs
                    )
                )
            if approved_hs and not _is_valid_hs_code(approved_hs):
                _raise_validation_error(
                    _("Dòng {0}: Mã HS phê duyệt '{1}' không đúng định dạng chuẩn (4-10 chữ số).").format(
                        idx, approved_hs
                    )
                )
            if hs_status == "Approved":
                if not approved_hs:
                    _raise_validation_error(
                        _("Dòng {0}: Không thể chuyển trạng thái HS sang Approved khi chưa có mã HS chính thức (approved_hs_code).").format(
                            idx
                        )
                    )
                approved_count += 1
                if not primary_hs:
                    primary_hs = approved_hs
            elif suggested_hs and not primary_hs:
                primary_hs = suggested_hs

            if int(_item_get(item, "requires_license", 0) or 0) == 1:
                any_license_required = True
            insp = str(_item_get(item, "specialized_inspection_type", "None") or "None")
            if insp not in ("", "None"):
                any_inspection_required = True

        self.total_customs_value = round(total_val, 2)
        self.total_import_duty = round(total_duty, 2)
        self.total_special_consumption_tax = round(total_sct, 2)
        self.total_vat = round(total_vat, 2)
        self.total_duty_tax = round(total_duty + total_sct + total_vat, 2)

        self.primary_hs_code = primary_hs or ""
        total_items = len(items)
        if total_items == 0:
            self.hs_approval_summary = "No Items Declared"
        elif approved_count == total_items:
            self.hs_approval_summary = f"Approved by Customs Specialist ({approved_count}/{total_items})"
        else:
            self.hs_approval_summary = f"Pending HS Approval ({approved_count}/{total_items})"

        if any_license_required and getattr(self, "license_status", "N/A") == "N/A":
            self.license_status = "Required"
        if any_inspection_required and getattr(self, "inspection_status", "Not Required") == "Not Required":
            self.inspection_status = "Pending"

    def _enforce_hs_and_declaration_gates(self):
        items = getattr(self, "items", None) or []
        if self.workflow_status in ("Declared", "Processing", "Cleared"):
            decl_no = str(getattr(self, "declaration_no", "") or "").strip()
            if not decl_no:
                _raise_validation_error(
                    _("Bắt buộc nhập Số tờ khai VNACCS/VCIS (declaration_no) khi chuyển sang trạng thái '{0}'.").format(
                        self.workflow_status
                    )
                )
            if not items:
                _raise_validation_error(
                    _("Tờ khai phải có ít nhất 1 dòng hàng hóa đã được chuyên viên phê duyệt mã HS trước khi truyền tờ khai.")
                )
            unapproved = [
                idx
                for idx, it in enumerate(items, start=1)
                if str(_item_get(it, "hs_approval_status", "Pending")) != "Approved"
                or not str(_item_get(it, "approved_hs_code", "") or "").strip()
            ]
            if unapproved:
                _raise_validation_error(
                    _("Chặn truyền/thông quan: Dòng hàng {0} chưa được chuyên viên Hải quan phê duyệt mã HS (Human Approval bắt buộc).").format(
                        ", ".join(str(i) for i in unapproved)
                    )
                )

    def _sync_clearance_and_processing_days(self):
        as_of = _parse_date_safe(getattr(self, "_as_of_date", None)) or date.today()
        decl_dt = _parse_date_safe(getattr(self, "declaration_date", None))
        clear_dt = _parse_date_safe(getattr(self, "clearance_date", None))

        if self.workflow_status == "Cleared":
            self.clearance_status = "CLEARED"
            if not clear_dt:
                self.clearance_date = str(as_of)
                clear_dt = as_of
            if self.customs_lane == "Not Declared":
                self.customs_lane = "Green"
            if getattr(self, "inspection_status", None) in (None, "", "Pending", "Document Check", "Physical Inspection"):
                self.inspection_status = "Passed"
        elif self.workflow_status == "Rejected":
            self.clearance_status = "REJECTED"
        else:
            self.clearance_status = "NOT CLEARED"

        if self.workflow_status in ("Declared", "Processing") and not decl_dt:
            self.declaration_date = str(as_of)
            decl_dt = as_of

        if decl_dt and clear_dt and clear_dt < decl_dt:
            _raise_validation_error(
                _("Ngày thông quan ({0}) không thể nhỏ hơn ngày đăng ký tờ khai ({1}).").format(
                    clear_dt, decl_dt
                )
            )

        if decl_dt:
            end_dt = clear_dt if clear_dt else (as_of if self.workflow_status in ("Declared", "Processing") else decl_dt)
            self.processing_days = max(0, (end_dt - decl_dt).days)
        else:
            self.processing_days = 0

        # Auto-align inspection_status with channel when active
        if self.workflow_status in ("Declared", "Processing"):
            if self.customs_lane == "Red" and getattr(self, "inspection_status", "") in ("", "Not Required", "Pending", "Document Check"):
                self.inspection_status = "Physical Inspection"
            elif self.customs_lane == "Yellow" and getattr(self, "inspection_status", "") in ("", "Not Required", "Pending"):
                self.inspection_status = "Document Check"

    def _trigger_case_rollup(self):
        case_id = getattr(self, "trade_case", None)
        if not case_id:
            return
        try:
            from logistics_wizard.customs_engine.api import sync_trade_case_customs_metrics
            sync_trade_case_customs_metrics(case_id)
        except Exception:
            pass

    def after_insert(self):
        self._trigger_case_rollup()

    def on_update(self):
        self._trigger_case_rollup()

    def on_trash(self):
        self._trigger_case_rollup()
