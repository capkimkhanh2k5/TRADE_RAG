# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""
customs_engine — Module 4: Customs & Trade Compliance Engine
=============================================================
Provides:
- Duty & tax computation (Import/Export Duty, Special Consumption Tax, VAT)
- Standardized HS suggestion & human specialist approval workflow
- Strict 6-state declaration lifecycle (Preparing -> Ready -> Declared -> Processing -> Cleared / Rejected)
- Exact Section 3.2 readiness contract for Trade Case Overview
- Overdue customs processing monitor & Trade Case rollup
"""

from .tax_calculator import (
    is_valid_hs_code,
    normalize_hs_code,
    calculate_item_taxes,
    calculate_declaration_totals,
)
from .workflow_engine import (
    ALLOWED_TRANSITIONS,
    can_transition,
    compute_customs_readiness_payload,
    is_declaration_overdue,
)
from .ai_hs_advisor import (
    extract_query_terms,
    recommend_hs_codes,
    strip_accents,
)
from .api import (
    InMemoryCustomsStore,
    in_memory_customs_store,
    get_case_customs_status,
    get_case_customs_declarations,
    create_customs_declaration,
    propose_hs_code,
    suggest_hs_code_with_rag,
    approve_hs_code,
    advance_customs_workflow,
    sync_trade_case_customs_metrics,
    scheduled_check_overdue_customs,
)

__all__ = [
    "is_valid_hs_code",
    "normalize_hs_code",
    "calculate_item_taxes",
    "calculate_declaration_totals",
    "ALLOWED_TRANSITIONS",
    "can_transition",
    "compute_customs_readiness_payload",
    "is_declaration_overdue",
    "extract_query_terms",
    "recommend_hs_codes",
    "strip_accents",
    "InMemoryCustomsStore",
    "in_memory_customs_store",
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
