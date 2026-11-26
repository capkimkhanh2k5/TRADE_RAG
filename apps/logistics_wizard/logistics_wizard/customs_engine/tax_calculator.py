# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""
tax_calculator.py — HS Validation & Vietnam Customs Duty/Tax Calculation Engine
================================================================================
Pure calculation module for:
- HS code format validation & canonical dotted formatting (e.g. 85176299 -> 8517.62.99)
- Import/Export Duty, Special Consumption Tax (TTDB), and VAT cascading calculation
"""

import re
from typing import Any, Dict, List, Optional

HS_CODE_PATTERN = re.compile(r"^\d{4}(\.?\d{2}){0,3}$")


def is_valid_hs_code(code: Optional[str]) -> bool:
    """Validate HS code syntax (4, 6, 8, or 10 digits with optional dots)."""
    if not code:
        return False
    return bool(HS_CODE_PATTERN.match(str(code).strip()))


def normalize_hs_code(code: Optional[str]) -> str:
    """Format 8-digit HS code into canonical XXXX.XX.XX form when possible."""
    if not code:
        return ""
    digits = re.sub(r"[^0-9]", "", str(code).strip())
    if len(digits) == 8:
        return f"{digits[:4]}.{digits[4:6]}.{digits[6:8]}"
    if len(digits) == 6:
        return f"{digits[:4]}.{digits[4:6]}"
    if len(digits) == 10:
        return f"{digits[:4]}.{digits[4:6]}.{digits[6:8]}.{digits[8:10]}"
    return str(code).strip()


def calculate_item_taxes(
    customs_value: float,
    import_duty_rate: float = 0.0,
    special_consumption_tax_rate: float = 0.0,
    vat_rate: float = 10.0,
) -> Dict[str, float]:
    """
    Compute Vietnam statutory cascading customs taxes:
    1. Import/Export Duty = Customs Value * duty_rate
    2. Special Consumption Tax = (Customs Value + Duty) * sct_rate
    3. VAT = (Customs Value + Duty + SCT) * vat_rate
    """
    cv = max(0.0, float(customs_value or 0.0))
    d_rate = max(0.0, float(import_duty_rate or 0.0))
    s_rate = max(0.0, float(special_consumption_tax_rate or 0.0))
    v_rate = max(0.0, float(vat_rate or 0.0))

    duty_amt = round(cv * d_rate / 100.0, 2)
    sct_amt = round((cv + duty_amt) * s_rate / 100.0, 2)
    vat_amt = round((cv + duty_amt + sct_amt) * v_rate / 100.0, 2)
    total_tax = round(duty_amt + sct_amt + vat_amt, 2)

    return {
        "customs_value": round(cv, 2),
        "import_duty_amount": duty_amt,
        "special_consumption_tax_amount": sct_amt,
        "vat_amount": vat_amt,
        "total_tax_amount": total_tax,
    }


def calculate_declaration_totals(items: List[Dict[str, Any]]) -> Dict[str, float]:
    """Aggregate line-level customs value and taxes across all declaration items."""
    total_val = 0.0
    total_duty = 0.0
    total_sct = 0.0
    total_vat = 0.0

    for item in items or []:
        qty = float(item.get("qty", 0) or 0)
        unit_price = float(item.get("unit_price", 0) or 0)
        cv = float(item.get("customs_value", 0) or 0)
        if cv <= 0 and qty > 0 and unit_price > 0:
            cv = round(qty * unit_price, 2)

        taxes = calculate_item_taxes(
            customs_value=cv,
            import_duty_rate=float(item.get("import_duty_rate", 0) or 0),
            special_consumption_tax_rate=float(item.get("special_consumption_tax_rate", 0) or 0),
            vat_rate=float(item.get("vat_rate", 0) or 0),
        )
        total_val += taxes["customs_value"]
        total_duty += taxes["import_duty_amount"]
        total_sct += taxes["special_consumption_tax_amount"]
        total_vat += taxes["vat_amount"]

    return {
        "total_customs_value": round(total_val, 2),
        "total_import_duty": round(total_duty, 2),
        "total_special_consumption_tax": round(total_sct, 2),
        "total_vat": round(total_vat, 2),
        "total_duty_tax": round(total_duty + total_sct + total_vat, 2),
    }


__all__ = [
    "HS_CODE_PATTERN",
    "is_valid_hs_code",
    "normalize_hs_code",
    "calculate_item_taxes",
    "calculate_declaration_totals",
]
