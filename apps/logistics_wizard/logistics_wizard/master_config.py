# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""
Trade Master Config — Centralized Global Trade Reference Data & Thresholds
===========================================================================
Provides configurable reference catalogs and operational thresholds for all
Global Trade modules without hard-coding business rules inside controllers:
- INCOTERMS_2020 (all 11 ICC Incoterms 2020 rules)
- DOCUMENT_TYPES_CATALOG (Commercial, Transport, Customs, Compliance)
- get_required_documents_template(trade_type, incoterm, shipping_mode)
- validate_incoterm_for_mode(incoterm, shipping_mode)
- CUSTOMS_OFFICES_VN (Vietnam Customs Sub-departments & Ports)
- get_trade_thresholds() (reads live Shipment Tracking Settings when available)
"""

from typing import Any, Dict, List, Optional

try:
    import frappe
except ImportError:
    frappe = None


ALL_TRANSPORT_MODES = ["Ocean", "Air", "Road", "Rail", "Multimodal"]
SEA_ONLY_MODES = ["Ocean"]


INCOTERMS_2020: Dict[str, Dict[str, Any]] = {
    "EXW": {
        "code": "EXW",
        "name": "Ex Works",
        "allowed_modes": list(ALL_TRANSPORT_MODES),
        "seller_pays_main_freight": False,
        "insurance_mandatory": False,
        "export_clearance_responsibility": "Buyer",
        "import_clearance_responsibility": "Buyer",
    },
    "FCA": {
        "code": "FCA",
        "name": "Free Carrier",
        "allowed_modes": list(ALL_TRANSPORT_MODES),
        "seller_pays_main_freight": False,
        "insurance_mandatory": False,
        "export_clearance_responsibility": "Seller",
        "import_clearance_responsibility": "Buyer",
    },
    "FAS": {
        "code": "FAS",
        "name": "Free Alongside Ship",
        "allowed_modes": list(SEA_ONLY_MODES),
        "seller_pays_main_freight": False,
        "insurance_mandatory": False,
        "export_clearance_responsibility": "Seller",
        "import_clearance_responsibility": "Buyer",
    },
    "FOB": {
        "code": "FOB",
        "name": "Free On Board",
        "allowed_modes": list(SEA_ONLY_MODES),
        "seller_pays_main_freight": False,
        "insurance_mandatory": False,
        "export_clearance_responsibility": "Seller",
        "import_clearance_responsibility": "Buyer",
    },
    "CFR": {
        "code": "CFR",
        "name": "Cost and Freight",
        "allowed_modes": list(SEA_ONLY_MODES),
        "seller_pays_main_freight": True,
        "insurance_mandatory": False,
        "export_clearance_responsibility": "Seller",
        "import_clearance_responsibility": "Buyer",
    },
    "CIF": {
        "code": "CIF",
        "name": "Cost, Insurance and Freight",
        "allowed_modes": list(SEA_ONLY_MODES),
        "seller_pays_main_freight": True,
        "insurance_mandatory": True,
        "export_clearance_responsibility": "Seller",
        "import_clearance_responsibility": "Buyer",
    },
    "CPT": {
        "code": "CPT",
        "name": "Carriage Paid To",
        "allowed_modes": list(ALL_TRANSPORT_MODES),
        "seller_pays_main_freight": True,
        "insurance_mandatory": False,
        "export_clearance_responsibility": "Seller",
        "import_clearance_responsibility": "Buyer",
    },
    "CIP": {
        "code": "CIP",
        "name": "Carriage and Insurance Paid To",
        "allowed_modes": list(ALL_TRANSPORT_MODES),
        "seller_pays_main_freight": True,
        "insurance_mandatory": True,
        "export_clearance_responsibility": "Seller",
        "import_clearance_responsibility": "Buyer",
    },
    "DAP": {
        "code": "DAP",
        "name": "Delivered at Place",
        "allowed_modes": list(ALL_TRANSPORT_MODES),
        "seller_pays_main_freight": True,
        "insurance_mandatory": False,
        "export_clearance_responsibility": "Seller",
        "import_clearance_responsibility": "Buyer",
    },
    "DPU": {
        "code": "DPU",
        "name": "Delivered at Place Unloaded",
        "allowed_modes": list(ALL_TRANSPORT_MODES),
        "seller_pays_main_freight": True,
        "insurance_mandatory": False,
        "export_clearance_responsibility": "Seller",
        "import_clearance_responsibility": "Buyer",
    },
    "DDP": {
        "code": "DDP",
        "name": "Delivered Duty Paid",
        "allowed_modes": list(ALL_TRANSPORT_MODES),
        "seller_pays_main_freight": True,
        "insurance_mandatory": False,
        "export_clearance_responsibility": "Seller",
        "import_clearance_responsibility": "Seller",
    },
}


DOCUMENT_TYPES_CATALOG: Dict[str, List[Dict[str, Any]]] = {
    "Commercial": [
        {
            "code": "DOC-SC",
            "name": "Sales Contract",
            "trade_types": ["Import", "Export"],
            "modes": list(ALL_TRANSPORT_MODES),
            "default_mandatory": False,
            "required_before_stage": "Booking",
        },
        {
            "code": "DOC-CI",
            "name": "Commercial Invoice",
            "trade_types": ["Import", "Export"],
            "modes": list(ALL_TRANSPORT_MODES),
            "default_mandatory": True,
            "required_before_stage": "Customs",
        },
        {
            "code": "DOC-PL",
            "name": "Packing List",
            "trade_types": ["Import", "Export"],
            "modes": list(ALL_TRANSPORT_MODES),
            "default_mandatory": True,
            "required_before_stage": "Customs",
        },
    ],
    "Transport": [
        {
            "code": "DOC-BKG",
            "name": "Booking Confirmation",
            "trade_types": ["Export"],
            "modes": list(ALL_TRANSPORT_MODES),
            "default_mandatory": True,
            "required_before_stage": "Export Port",
        },
        {
            "code": "DOC-BL",
            "name": "Bill of Lading (B/L)",
            "trade_types": ["Import", "Export"],
            "modes": ["Ocean"],
            "default_mandatory": True,
            "required_before_stage": "Customs",
        },
        {
            "code": "DOC-AWB",
            "name": "Air Waybill (AWB)",
            "trade_types": ["Import", "Export"],
            "modes": ["Air"],
            "default_mandatory": True,
            "required_before_stage": "Customs",
        },
        {
            "code": "DOC-CMR",
            "name": "Road Waybill / Truck Manifest",
            "trade_types": ["Import", "Export"],
            "modes": ["Road", "Rail", "Multimodal"],
            "default_mandatory": True,
            "required_before_stage": "Customs",
        },
        {
            "code": "DOC-DO",
            "name": "Delivery Order (D/O)",
            "trade_types": ["Import"],
            "modes": list(ALL_TRANSPORT_MODES),
            "default_mandatory": True,
            "required_before_stage": "Warehouse",
        },
        {
            "code": "DOC-INS",
            "name": "Cargo Insurance Policy",
            "trade_types": ["Import", "Export"],
            "modes": list(ALL_TRANSPORT_MODES),
            "default_mandatory": False,
            "required_before_stage": "Customs",
        },
    ],
    "Customs": [
        {
            "code": "DOC-CUS-IMP",
            "name": "Import Customs Declaration",
            "trade_types": ["Import"],
            "modes": list(ALL_TRANSPORT_MODES),
            "default_mandatory": True,
            "required_before_stage": "Warehouse",
        },
        {
            "code": "DOC-CUS-EXP",
            "name": "Export Customs Declaration",
            "trade_types": ["Export"],
            "modes": list(ALL_TRANSPORT_MODES),
            "default_mandatory": True,
            "required_before_stage": "In Transit",
        },
    ],
    "Compliance": [
        {
            "code": "DOC-CO",
            "name": "Certificate of Origin (C/O)",
            "trade_types": ["Import", "Export"],
            "modes": list(ALL_TRANSPORT_MODES),
            "default_mandatory": True,
            "required_before_stage": "Customs",
        },
        {
            "code": "DOC-PHYTO",
            "name": "Quarantine / Quality Inspection Certificate",
            "trade_types": ["Import", "Export"],
            "modes": list(ALL_TRANSPORT_MODES),
            "default_mandatory": False,
            "required_before_stage": "Customs",
        },
        {
            "code": "DOC-LIC",
            "name": "Import/Export Permit",
            "trade_types": ["Import", "Export"],
            "modes": list(ALL_TRANSPORT_MODES),
            "default_mandatory": False,
            "required_before_stage": "Customs",
        },
    ],
}


CUSTOMS_OFFICES_VN: List[Dict[str, str]] = [
    {
        "code": "02CI",
        "name": "Chi cục Hải quan cửa khẩu cảng Sài Gòn khu vực I (Cát Lái)",
        "port_code": "VNCLI",
        "mode": "Ocean",
        "region": "South",
    },
    {
        "code": "51C1",
        "name": "Chi cục Hải quan cửa khẩu cảng Cái Mép",
        "port_code": "VNVUT",
        "mode": "Ocean",
        "region": "South",
    },
    {
        "code": "03CC",
        "name": "Chi cục Hải quan cửa khẩu cảng Hải Phòng khu vực I",
        "port_code": "VNHPH",
        "mode": "Ocean",
        "region": "North",
    },
    {
        "code": "03CL",
        "name": "Chi cục Hải quan cửa khẩu cảng Đình Vũ / Lạch Huyện",
        "port_code": "VNLCH",
        "mode": "Ocean",
        "region": "North",
    },
    {
        "code": "01B1",
        "name": "Chi cục Hải quan cửa khẩu sân bay quốc tế Nội Bài",
        "port_code": "VNHAN",
        "mode": "Air",
        "region": "North",
    },
    {
        "code": "02B1",
        "name": "Chi cục Hải quan cửa khẩu sân bay quốc tế Tân Sơn Nhất",
        "port_code": "VNSGN",
        "mode": "Air",
        "region": "South",
    },
    {
        "code": "32C1",
        "name": "Chi cục Hải quan cửa khẩu cảng Đà Nẵng (Tiên Sa)",
        "port_code": "VNDAD",
        "mode": "Ocean",
        "region": "Central",
    },
    {
        "code": "34C1",
        "name": "Chi cục Hải quan cửa khẩu cảng Quy Nhơn",
        "port_code": "VNUIH",
        "mode": "Ocean",
        "region": "Central",
    },
    {
        "code": "15BE",
        "name": "Chi cục Hải quan cửa khẩu Hữu Nghị",
        "port_code": "VNHNG",
        "mode": "Road",
        "region": "North",
    },
]


DEFAULT_TRADE_THRESHOLDS: Dict[str, Any] = {
    "enable_auto_polling": True,
    "auto_create_exceptions": True,
    "polling_interval_minutes": 60,
    "stale_threshold_hours": 48,
    "eta_warning_days": 1,
    "eta_critical_days": 3,
    "cost_variance_warning_pct": 5.0,
    "cost_variance_critical_pct": 15.0,
    "demurrage_free_days": 5,
    "doc_urgent_days_before_eta": 3,
}


def _normalize_trade_type(trade_type: Optional[str]) -> str:
    val = str(trade_type or "Import").strip().lower()
    return "Export" if val == "export" else "Import"


def _normalize_shipping_mode(shipping_mode: Optional[str]) -> str:
    val = str(shipping_mode or "Ocean").strip().lower()
    if val in ("sea", "ocean", "maritime"):
        return "Ocean"
    if val in ("air", "flight", "plane"):
        return "Air"
    if val in ("road", "truck", "inland"):
        return "Road"
    if val in ("rail", "train"):
        return "Rail"
    if val in ("multimodal", "multi"):
        return "Multimodal"
    return "Ocean"


def get_required_documents_template(
    trade_type: str = "Import",
    incoterm: str = "FOB",
    shipping_mode: str = "Ocean",
) -> List[Dict[str, Any]]:
    """
    Build the applicable document checklist template for a Trade Case based on
    Trade Type (Import/Export), Incoterm 2020 rule, and Shipping Mode.
    """
    norm_type = _normalize_trade_type(trade_type)
    norm_incoterm = str(incoterm or "FOB").strip().upper()
    norm_mode = _normalize_shipping_mode(shipping_mode)

    incoterm_rule = INCOTERMS_2020.get(norm_incoterm, {})
    insurance_mandatory = bool(incoterm_rule.get("insurance_mandatory", norm_incoterm in ("CIF", "CIP")))

    template: List[Dict[str, Any]] = []
    for category, doc_defs in DOCUMENT_TYPES_CATALOG.items():
        for doc_def in doc_defs:
            if norm_type not in doc_def["trade_types"]:
                continue
            if norm_mode not in doc_def["modes"]:
                continue

            is_mandatory = bool(doc_def["default_mandatory"])
            if doc_def["code"] == "DOC-INS":
                is_mandatory = insurance_mandatory

            template.append(
                {
                    "code": doc_def["code"],
                    "name": doc_def["name"],
                    "category": category,
                    "is_mandatory": is_mandatory,
                    "required_before_stage": doc_def["required_before_stage"],
                }
            )

    return template


def validate_incoterm_for_mode(incoterm: str, shipping_mode: str) -> Dict[str, Any]:
    """
    Validate compatibility between an Incoterms 2020 code and a transport mode.
    Returns {valid, incoterm, shipping_mode, warning}.
    """
    norm_incoterm = str(incoterm or "").strip().upper()
    norm_mode = _normalize_shipping_mode(shipping_mode)

    rule = INCOTERMS_2020.get(norm_incoterm)
    if not rule:
        return {
            "valid": False,
            "incoterm": norm_incoterm,
            "shipping_mode": norm_mode,
            "warning": f"Incoterm '{norm_incoterm}' không thuộc danh mục chuẩn ICC Incoterms 2020.",
        }

    allowed = rule["allowed_modes"]
    if norm_mode not in allowed:
        return {
            "valid": False,
            "incoterm": norm_incoterm,
            "shipping_mode": norm_mode,
            "warning": (
                f"Incoterm {norm_incoterm} theo chuẩn ICC 2020 chỉ áp dụng cho vận tải đường biển/thủy nội địa; "
                f"với phương thức {norm_mode} khuyến nghị chuyển sang FCA, CPT hoặc CIP."
            ),
        }

    return {
        "valid": True,
        "incoterm": norm_incoterm,
        "shipping_mode": norm_mode,
        "warning": None,
    }


def _coerce_int(val: Any, default: int) -> int:
    try:
        return int(val) if val is not None and val != "" else default
    except (TypeError, ValueError):
        return default


def _coerce_float(val: Any, default: float) -> float:
    try:
        return float(val) if val is not None and val != "" else default
    except (TypeError, ValueError):
        return default


def get_trade_thresholds() -> Dict[str, Any]:
    """
    Return active operational thresholds, reading from Single DocType
    'Shipment Tracking Settings' when Frappe DB is connected, with safe defaults.
    """
    thresholds = dict(DEFAULT_TRADE_THRESHOLDS)

    if not (
        frappe
        and getattr(frappe, "db", None)
        and hasattr(frappe.db, "exists")
        and frappe.db.exists("DocType", "Shipment Tracking Settings")
    ):
        return thresholds

    try:
        settings_dict: Dict[str, Any] = {}
        if hasattr(frappe.db, "get_singles_dict"):
            settings_dict = frappe.db.get_singles_dict("Shipment Tracking Settings") or {}
        elif hasattr(frappe, "get_single"):
            doc = frappe.get_single("Shipment Tracking Settings")
            settings_dict = doc.as_dict() if hasattr(doc, "as_dict") else vars(doc)

        if isinstance(settings_dict, dict) and settings_dict:
            if "enable_auto_polling" in settings_dict and settings_dict["enable_auto_polling"] is not None:
                thresholds["enable_auto_polling"] = bool(int(settings_dict["enable_auto_polling"]))
            if "auto_create_exceptions" in settings_dict and settings_dict["auto_create_exceptions"] is not None:
                thresholds["auto_create_exceptions"] = bool(int(settings_dict["auto_create_exceptions"]))
            thresholds["polling_interval_minutes"] = _coerce_int(
                settings_dict.get("polling_interval_minutes"), thresholds["polling_interval_minutes"]
            )
            thresholds["stale_threshold_hours"] = _coerce_int(
                settings_dict.get("stale_threshold_hours"), thresholds["stale_threshold_hours"]
            )
            thresholds["cost_variance_warning_pct"] = _coerce_float(
                settings_dict.get("cost_variance_warning_pct"), thresholds["cost_variance_warning_pct"]
            )
            thresholds["cost_variance_critical_pct"] = _coerce_float(
                settings_dict.get("cost_variance_critical_pct"), thresholds["cost_variance_critical_pct"]
            )
            thresholds["demurrage_free_days"] = _coerce_int(
                settings_dict.get("demurrage_free_days"), thresholds["demurrage_free_days"]
            )
            thresholds["doc_urgent_days_before_eta"] = _coerce_int(
                settings_dict.get("doc_urgent_days_before_eta"), thresholds["doc_urgent_days_before_eta"]
            )
    except Exception:
        pass

    return thresholds


__all__ = [
    "INCOTERMS_2020",
    "DOCUMENT_TYPES_CATALOG",
    "CUSTOMS_OFFICES_VN",
    "DEFAULT_TRADE_THRESHOLDS",
    "get_required_documents_template",
    "validate_incoterm_for_mode",
    "get_trade_thresholds",
]
