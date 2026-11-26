# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""
exception_engine — Module 6: Exception, Workflow, Action & Health Engine
=========================================================================
Implements:
- All 8 automated risk detection rules from docsTitleProject/ToDo.md Section 4.6
- Idempotent exception creation, assignment, escalation, resolution, and audit trail
- Action Item management (Trade Action Item)
- Automatic Trade Case overall_health calculation (Healthy / Attention / Critical)
"""

from .rule_evaluator import (
    EXCEPTION_RULES_CATALOG,
    evaluate_8_exception_rules,
    compute_trade_case_health,
)
from .api import (
    InMemoryExceptionStore,
    InMemoryActionStore,
    in_memory_exception_store,
    in_memory_action_store,
    raise_exception_from_rule,
    evaluate_case_exceptions,
    get_case_exceptions_summary,
    assign_exception,
    escalate_exception,
    resolve_exception,
    create_action_item,
    complete_action_item,
    get_case_action_items,
    sync_trade_case_exception_and_health,
    scheduled_evaluate_all_active_cases,
)

__all__ = [
    "EXCEPTION_RULES_CATALOG",
    "evaluate_8_exception_rules",
    "compute_trade_case_health",
    "InMemoryExceptionStore",
    "InMemoryActionStore",
    "in_memory_exception_store",
    "in_memory_action_store",
    "raise_exception_from_rule",
    "evaluate_case_exceptions",
    "get_case_exceptions_summary",
    "assign_exception",
    "escalate_exception",
    "resolve_exception",
    "create_action_item",
    "complete_action_item",
    "get_case_action_items",
    "sync_trade_case_exception_and_health",
    "scheduled_evaluate_all_active_cases",
]
