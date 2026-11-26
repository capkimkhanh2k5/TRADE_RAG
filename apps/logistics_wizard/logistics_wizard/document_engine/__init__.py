# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""
document_engine — Module 3: Trade Document Management Engine
=============================================================
Provides checklist auto-generation, file versioning, expiry & deadline evaluation,
Trade Case readiness rollup, and Section 3.1 API contract implementation.
"""

from .readiness_evaluator import (
    CANONICAL_CATEGORIES,
    evaluate_document_state,
    compute_document_readiness_payload,
)
from .checklist_manager import (
    InMemoryDocumentStore,
    in_memory_document_store,
    generate_case_document_checklist,
)
from .api import (
    get_case_documents_status,
    get_case_documents_list,
    init_case_document_checklist,
    upload_trade_document_version,
    verify_trade_document,
    sync_trade_case_document_metrics,
    on_trade_case_after_insert,
    scheduled_check_expiring_documents,
)

__all__ = [
    "CANONICAL_CATEGORIES",
    "evaluate_document_state",
    "compute_document_readiness_payload",
    "InMemoryDocumentStore",
    "in_memory_document_store",
    "generate_case_document_checklist",
    "get_case_documents_status",
    "get_case_documents_list",
    "init_case_document_checklist",
    "upload_trade_document_version",
    "verify_trade_document",
    "sync_trade_case_document_metrics",
    "on_trade_case_after_insert",
    "scheduled_check_expiring_documents",
]
