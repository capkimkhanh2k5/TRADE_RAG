# Copyright (c) 2026, Logistics Wizard and contributors
# For license information, please see license.txt

"""
customs_engine.ai_hs_advisor — Deep AI/RAG HS Code Recommendation Engine
========================================================================
Connects `apps/ai_service/ai_rag` (PostgreSQL `hs_rag` active snapshot +
Authoritative Knowledge Graph + optional CLIProxyAPI LLM reasoning) into
Module 4's standardized `propose_hs_code` slot.

Governance Guarantee (STRICT):
- NEVER approves HS codes automatically (`automatic_hs_decision = False`,
  `requires_human_approval = True`).
- Returns ranked 8-digit AHTN/VN HS candidates grounded in authentic tariff
  hierarchy paths (Section -> Chapter -> Heading 4 -> Subheading 6 -> HS 8)
  and governing legal notes (Section Notes, Chapter Notes, GIR 1-6).
- Multi-tier fault-tolerant retrieval:
  1. Tier 1: Live PostgreSQL `hs_rag` active snapshot (`rag.chunks` + `rag.graph_edges`).
  2. Tier 2: Authoritative `UnifiedGraphService` in-memory corpus fallback.
  3. Tier 3: Optional `CLIProxyAPI` LLM rerank & Vietnamese GIR synthesis
     (strictly bounded to retrieved candidates, short timeout, deterministic fallback).
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
import unicodedata
from collections import defaultdict
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .tax_calculator import is_valid_hs_code, normalize_hs_code

logger = logging.getLogger(__name__)

# Bilingual English -> Vietnamese AHTN/TT31 keyword enrichment for commercial invoices
BILINGUAL_TERM_MAP: Dict[str, List[str]] = {
    "laptop": ["may tinh xach tay", "notebook", "xu ly du lieu tu dong", "8471"],
    "notebook": ["may tinh xach tay", "xu ly du lieu tu dong", "8471"],
    "computer": ["may xu ly du lieu tu dong", "may tinh", "8471"],
    "server": ["may xu ly du lieu tu dong", "8471"],
    "pump": ["bom", "bom chat long", "8413"],
    "centrifugal": ["ly tam", "bom ly tam", "8413"],
    "water": ["nuoc"],
    "electric": ["dien", "hoat dong bang dien"],
    "motor": ["dong co dien", "8501"],
    "generator": ["may phat dien", "8502"],
    "transformer": ["may bien ap", "8504"],
    "solar": ["quang dien", "pin mat troi", "te bao quang dien", "8541"],
    "photovoltaic": ["quang dien", "te bao quang dien", "8541"],
    "panel": ["da lap rap", "thanh tam", "mang mo dun", "quang dien", "8541"],
    "module": ["da lap rap", "mo dun", "thanh tam", "8541"],
    "semiconductor": ["ban dan", "mach tich hop", "8541", "8542"],
    "chip": ["mach dien tu tich hop", "8542"],
    "ic": ["mach dien tu tich hop", "8542"],
    "microcontroller": ["bo vi dieu khien", "mach dien tu tich hop", "8542"],
    "battery": ["ac quy", "pin", "lithium", "8507", "8506"],
    "lithium": ["liti", "lithium", "ac quy dien", "8507"],
    "router": ["thiet bi truyen", "chuyen mach", "dinh tuyen", "8517"],
    "switch": ["chuyen mach", "dinh tuyen", "thiet bi vien thong", "8517"],
    "network": ["mang", "truyen du lieu", "8517"],
    "smartphone": ["dien thoai thong minh", "dien thoai di dong", "8517"],
    "phone": ["dien thoai", "8517"],
    "camera": ["may anh", "camera", "8525"],
    "television": ["tivi", "may thu hinh", "8528"],
    "monitor": ["man hinh", "8528"],
    "cable": ["cap dien", "day dan dien", "8544"],
    "wire": ["day dien", "cap dien", "8544"],
    "compressor": ["may nen khi", "8414"],
    "fan": ["quat", "8414"],
    "air": ["khong khi", "dieu hoa"],
    "conditioner": ["may dieu hoa khong khi", "8415"],
    "refrigerator": ["tu lanh", "8418"],
    "cnc": ["dieu khien so", "may cong cu", "8458", "8459"],
    "lathe": ["may tien", "8458"],
    "milling": ["may phay", "8459"],
    "valve": ["van", "voi", "8481"],
    "bearing": ["o bi", "o dua", "8482"],
    "tractor": ["may keo", "8701"],
    "truck": ["xe co dong co cho hang", "xe tai", "8704"],
    "car": ["xe o to", "xe co dong co", "8703"],
    "motorcycle": ["xe mo to", "xe gan may", "8711"],
    "bicycle": ["xe dap", "8712"],
    "forklift": ["xe nang", "8427"],
    "crane": ["can truc", "cau", "8426"],
    "gold": ["vang", "kim loai quy", "7108", "7113"],
    "silver": ["bac", "7106"],
    "diamond": ["kim cuong", "7102"],
    "jewelry": ["do kim hoan", "trang suc", "7113"],
    "sensor": ["cam bien", "thiet bi do", "9031", "8541"],
    "inverter": ["bien tan", "bo bien doi tinh", "8504"],
    "led": ["diot phat quang", "den led", "8539", "8541"],
    "printer": ["may in", "8443"],
    "excavator": ["may xuc", "may dao", "8429"],
    "boiler": ["noi hoi", "8402"],
    "turbine": ["tua bin", "8406", "8410", "8411"],
}

STOPWORDS = {
    "va", "cua", "cho", "voi", "cac", "loai", "khac", "co", "khong", "duoc",
    "bang", "hoac", "theo", "trong", "tu", "den", "la", "mot", "nhung",
    "the", "and", "for", "with", "from", "into", "type", "other", "model",
    "new", "brand", "pcs", "unit", "set", "grade", "standard", "industrial",
    "cong", "nghiep", "chinh", "hang", "nhap", "khau", "xuat",
}

GENERIC_LEAF_MARKERS = (
    "loai khac",
    "- loai khac",
    "- - loai khac",
    "- - - loai khac",
    "loai khac (sen)",
)

NOTE_RELATIONS_FROM_TARIFF = {
    "CONSTRAINED_BY",
    "GOVERNED_BY",
    "HAS_LEGAL_NOTE",
    "SUBJECT_TO",
    "EXCLUDED_BY",
}

NOTE_RELATIONS_TO_TARIFF = {
    "APPLIES_TO",
    "APPLIES_WITHIN",
    "GOVERNS",
    "DEFINES_FOR",
    "DEFINITION_APPLIES_TO",
    "INCLUDES_IN_SCOPE",
    "DEFINES_SCOPE_OF",
}


def ensure_ai_rag_path() -> Optional[str]:
    """Ensure `apps/ai_service/ai_rag` is on `sys.path`."""
    candidates = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../ai_service/ai_rag")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ai_service/ai_rag")),
        "/home/frappe/frappe-bench/apps/ai_service/ai_rag",
    ]
    for path in candidates:
        if os.path.isdir(path):
            if path not in sys.path:
                sys.path.insert(0, path)
            return path
    return None


def strip_accents(text: str) -> str:
    """Normalize Vietnamese/Unicode string to lowercase ASCII tokens."""
    if not text:
        return ""
    s = str(text).replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return s.lower()


def extract_query_terms(
    item_description: str,
    material: Optional[str] = None,
    function: Optional[str] = None,
) -> Dict[str, Any]:
    """Extract normalized tokens, bigrams, HS hints, and bilingual expansions."""
    combined_raw = " ".join(
        part.strip()
        for part in (item_description or "", material or "", function or "")
        if part and str(part).strip()
    )
    norm_text = strip_accents(combined_raw)
    raw_tokens = re.findall(r"[a-z0-9]{2,}", norm_text)

    hs_hints: List[str] = []
    for m in re.findall(r"\b(\d{4}(?:\.?\d{2})?(?:\.?\d{2})?)\b", combined_raw):
        digits = re.sub(r"\D", "", m)
        if 4 <= len(digits) <= 8:
            hs_hints.append(digits)

    base_tokens: List[str] = []
    expanded_phrases: List[str] = []
    expanded_tokens: List[str] = []

    for tok in raw_tokens:
        if tok in STOPWORDS:
            continue
        if tok not in base_tokens:
            base_tokens.append(tok)
        if tok in BILINGUAL_TERM_MAP:
            for mapped in BILINGUAL_TERM_MAP[tok]:
                if mapped.isdigit():
                    if mapped not in hs_hints:
                        hs_hints.append(mapped)
                else:
                    expanded_phrases.append(mapped)
                    for sub in re.findall(r"[a-z0-9]{2,}", mapped):
                        if sub not in STOPWORDS and sub not in expanded_tokens:
                            expanded_tokens.append(sub)

    # Bigrams from original normalized text give strong phrase precision
    bigrams: List[str] = []
    clean_words = [w for w in raw_tokens if w not in STOPWORDS and not w.isdigit()]
    for i in range(len(clean_words) - 1):
        bg = f"{clean_words[i]} {clean_words[i + 1]}"
        if bg not in bigrams:
            bigrams.append(bg)
    for phrase in expanded_phrases:
        if phrase not in bigrams:
            bigrams.append(phrase)

    all_search_tokens = list(dict.fromkeys([*base_tokens, *expanded_tokens]))
    return {
        "raw_query": combined_raw,
        "normalized_query": norm_text,
        "base_tokens": base_tokens,
        "expanded_tokens": expanded_tokens,
        "all_tokens": all_search_tokens,
        "phrases": bigrams,
        "hs_hints": list(dict.fromkeys(hs_hints)),
    }


def _is_generic_leaf(text: str) -> bool:
    norm = re.sub(r"[^a-z0-9\s]", " ", strip_accents(text)).strip()
    norm = re.sub(r"\s+", " ", norm)
    return norm in {"loai khac", "loai khac sen", "khac", "khac sen", ""}


def _score_candidate(
    query_info: Dict[str, Any],
    code: str,
    leaf_text: str,
    hierarchy_texts: Sequence[str],
    chapter: str = "",
) -> Tuple[float, List[str]]:
    """Deterministic lexical + hierarchy + HS-prefix relevance scoring."""
    leaf_norm = strip_accents(leaf_text)
    full_norm = strip_accents(" ".join([*hierarchy_texts, leaf_text]))
    leaf_words = set(re.findall(r"[a-z0-9]{2,}", leaf_norm))
    full_words = set(re.findall(r"[a-z0-9]{2,}", full_norm))

    digits = re.sub(r"\D", "", str(code or ""))
    score = 0.0
    matched_signals: List[str] = []

    # 1. Exact or prefix HS code hint boost
    for hint in query_info["hs_hints"]:
        if digits == hint:
            score += 6.0
            matched_signals.append(f"HS exact:{hint}")
        elif digits.startswith(hint):
            score += 3.2 if len(hint) >= 6 else 2.2
            matched_signals.append(f"HS prefix:{hint}")

    # 2. Phrase / bigram hits (highest semantic precision)
    for phrase in query_info["phrases"]:
        if len(phrase) < 4:
            continue
        if phrase in leaf_norm:
            score += 3.0
            matched_signals.append(phrase)
        elif phrase in full_norm:
            score += 1.8
            matched_signals.append(phrase)

    # 3. Token coverage across leaf & parent hierarchy
    base_hits = 0
    for tok in query_info["base_tokens"]:
        if tok in leaf_words:
            score += 1.4
            base_hits += 1
        elif tok in full_words:
            score += 0.85
            base_hits += 1

    exp_hits = 0
    for tok in query_info["expanded_tokens"]:
        if tok in query_info["base_tokens"]:
            continue
        if tok in leaf_words:
            score += 1.15
            exp_hits += 1
        elif tok in full_words:
            score += 0.70
            exp_hits += 1

    total_query_tokens = max(1, len(query_info["all_tokens"]))
    coverage = (base_hits + exp_hits) / total_query_tokens
    score += coverage * 2.5

    # 4. Prefer specific HS8 leaf wording over catch-all "Loại khác" when siblings match
    if _is_generic_leaf(leaf_text):
        score -= 0.45

    return round(score, 4), list(dict.fromkeys(matched_signals))[:6]


def _raw_score_to_confidence(raw_score: float, top_score: float) -> float:
    """Map raw retrieval score into calibrated 35%..95% human-review confidence range."""
    if raw_score <= 0:
        return 35.0
    # Never claim 100% — specialist approval is always mandatory
    base = 42.0 + min(45.0, raw_score * 5.2)
    if top_score > 0 and raw_score < top_score:
        ratio = max(0.2, raw_score / top_score)
        base = base * (0.72 + 0.28 * ratio)
    return round(max(35.0, min(95.0, base)), 1)


def _format_legal_basis(
    candidate: Dict[str, Any],
    notes: Sequence[Dict[str, Any]],
    gir_rules: Sequence[Dict[str, Any]],
    llm_rationale: Optional[str] = None,
) -> str:
    """Format concise, auditable Vietnamese legal basis for `hs_legal_basis` field."""
    parts: List[str] = []
    if llm_rationale:
        parts.append(f"[Phân tích AI/GIR] {llm_rationale.strip()}")
    hierarchy = candidate.get("full_hierarchy_path") or candidate.get("description") or ""
    if hierarchy:
        parts.append(f"[Phân cấp Biểu thuế TT31/AHTN] {hierarchy[:260]}")
    if notes:
        note_snippets = [
            f"{n.get('id')}: {(n.get('text') or '')[:140]}"
            for n in notes[:2]
            if n.get("text")
        ]
        if note_snippets:
            parts.append("[Chú giải pháp lý] " + " | ".join(note_snippets))
    if gir_rules:
        gir_titles = ", ".join(str(g.get("code") or g.get("id")) for g in gir_rules[:2])
        parts.append(f"[Quy tắc GIR] {gir_titles} (TT31/2022/TT-BTC)")
    else:
        parts.append("[Quy tắc GIR] GIR 1 & GIR 6 (TT31/2022/TT-BTC)")
    return "\n".join(parts)[:900]


def _open_pg_connection():
    """
    Open a lightweight PostgreSQL connection to `hs_rag` supporting both `psycopg2`
    (installed in Frappe backend container) and `psycopg` v3 without requiring `numpy`.
    Returns `(conn, cursor_fn, close_fn)` where `cursor_fn(sql, params)` returns list[dict].
    """
    ensure_ai_rag_path()
    host = os.getenv("RAG_DB_HOST") or os.getenv("PGHOST") or "postgres"
    port = int(os.getenv("RAG_DB_PORT") or os.getenv("PGPORT") or "5432")
    dbname = os.getenv("RAG_DB_NAME") or os.getenv("PGDATABASE") or "hs_rag"
    user = os.getenv("RAG_DB_USER") or os.getenv("PGUSER") or "rag"
    password = os.getenv("RAG_DB_PASSWORD") or os.getenv("PGPASSWORD") or ""
    try:
        from config.settings import DatabaseConfig

        cfg = DatabaseConfig.from_env()
        host, port, dbname, user, password = (
            cfg.host,
            cfg.port,
            cfg.dbname,
            cfg.user,
            cfg.password,
        )
    except Exception:
        pass

    # Prefer psycopg2 (natively available in Frappe container) then psycopg v3
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor

        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            connect_timeout=3,
        )
        conn.autocommit = True

        def _query(sql: str, params: Tuple[Any, ...] = ()) -> List[Dict[str, Any]]:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, params)
                return [dict(r) for r in cur.fetchall()]

        return conn, _query, conn.close
    except ImportError:
        pass

    import psycopg
    from psycopg.rows import dict_row

    conn = psycopg.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
        row_factory=dict_row,
        autocommit=True,
        connect_timeout=3,
    )

    def _query_v3(sql: str, params: Tuple[Any, ...] = ()) -> List[Dict[str, Any]]:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]

    return conn, _query_v3, conn.close


def _retrieve_from_postgres(
    query_info: Dict[str, Any],
    top_k: int = 5,
) -> Optional[Dict[str, Any]]:
    """
    Tier 1: Query live PostgreSQL `hs_rag` active snapshot (`rag.chunks` + `rag.graph_edges`).
    Fast (<150ms), zero ML model loading, full 8-digit tariff hierarchy & governing notes.
    """
    search_tokens = [
        t for t in query_info["all_tokens"]
        if re.fullmatch(r"[a-z0-9]+", t) and len(t) >= 2
    ][:18]
    hs_hints = query_info["hs_hints"][:6]
    if not search_tokens and not hs_hints:
        return None

    conn = None
    close_fn = None
    try:
        conn, query_rows, close_fn = _open_pg_connection()
        active_rows = query_rows("SELECT snapshot, profile FROM rag.active LIMIT 1")
        if not active_rows:
            return None
        snapshot = active_rows[0]["snapshot"]

        # Build PostgreSQL OR tsquery over unaccented tokens
        tsquery_expr = " | ".join(search_tokens) if search_tokens else ""
        matched_rows: List[Dict[str, Any]] = []

        if tsquery_expr:
            matched_rows.extend(
                query_rows(
                    """
                    SELECT id, code, level, chapter, heading, section, hs6, ahtn8,
                           chunk_type, source_text, embedding_text,
                           ts_rank_cd(lexical, to_tsquery('simple', %s)) AS lex_rank
                    FROM rag.chunks
                    WHERE snapshot = %s
                      AND chunk_type = 'tariff_entry'
                      AND level IN (4, 6, 8)
                      AND lexical @@ to_tsquery('simple', %s)
                    ORDER BY lex_rank DESC, level DESC
                    LIMIT 90
                    """,
                    (tsquery_expr, snapshot, tsquery_expr),
                )
            )

        # Also pull direct HS code hints (e.g. 8471, 8541, 8413)
        for hint in hs_hints:
            matched_rows.extend(
                query_rows(
                    """
                    SELECT id, code, level, chapter, heading, section, hs6, ahtn8,
                           chunk_type, source_text, embedding_text, 2.0 AS lex_rank
                    FROM rag.chunks
                    WHERE snapshot = %s
                      AND chunk_type = 'tariff_entry'
                      AND level IN (4, 6, 8)
                      AND code LIKE %s
                    ORDER BY level DESC, code ASC
                    LIMIT 30
                    """,
                    (snapshot, f"{hint}%"),
                )
            )

        if not matched_rows:
            return None

        # Expand matched level-4 headings & level-6 subheadings to their level-8 leaves
        hs8_by_id: Dict[str, Dict[str, Any]] = {}
        headings_to_expand: List[str] = []
        hs6_to_expand: List[str] = []

        for r in matched_rows:
            lvl = r.get("level")
            if lvl == 8 and r.get("code"):
                hs8_by_id[r["id"]] = r
            elif lvl == 6 and r.get("hs6"):
                if r["hs6"] not in hs6_to_expand:
                    hs6_to_expand.append(r["hs6"])
            elif lvl == 4 and r.get("heading"):
                if r["heading"] not in headings_to_expand:
                    headings_to_expand.append(r["heading"])

        if hs6_to_expand:
            for r in query_rows(
                """
                SELECT id, code, level, chapter, heading, section, hs6, ahtn8,
                       chunk_type, source_text, embedding_text, 0.5 AS lex_rank
                FROM rag.chunks
                WHERE snapshot = %s
                  AND chunk_type = 'tariff_entry'
                  AND level = 8
                  AND hs6 = ANY(%s)
                LIMIT 120
                """,
                (snapshot, hs6_to_expand[:15]),
            ):
                hs8_by_id.setdefault(r["id"], r)

        if headings_to_expand and len(hs8_by_id) < 40:
            for r in query_rows(
                """
                SELECT id, code, level, chapter, heading, section, hs6, ahtn8,
                       chunk_type, source_text, embedding_text, 0.35 AS lex_rank
                FROM rag.chunks
                WHERE snapshot = %s
                  AND chunk_type = 'tariff_entry'
                  AND level = 8
                  AND heading = ANY(%s)
                LIMIT 100
                """,
                (snapshot, headings_to_expand[:8]),
            ):
                hs8_by_id.setdefault(r["id"], r)

        if not hs8_by_id:
            return None

        # Fetch parent level-4 and level-6 context rows for full hierarchy wording
        all_headings = list({r["heading"] for r in hs8_by_id.values() if r.get("heading")})
        all_hs6 = list({r["hs6"] for r in hs8_by_id.values() if r.get("hs6")})
        parent_lookup: Dict[Tuple[int, str], Dict[str, Any]] = {}
        if all_headings or all_hs6:
            for p in query_rows(
                """
                SELECT id, code, level, chapter, heading, hs6, source_text
                FROM rag.chunks
                WHERE snapshot = %s
                  AND chunk_type = 'tariff_entry'
                  AND (
                    (level = 4 AND heading = ANY(%s))
                    OR (level = 6 AND hs6 = ANY(%s))
                  )
                """,
                (snapshot, all_headings or [""], all_hs6 or [""]),
            ):
                if p["level"] == 4 and p.get("heading"):
                    parent_lookup[(4, p["heading"])] = p
                elif p["level"] == 6 and p.get("hs6"):
                    parent_lookup[(6, p["hs6"])] = p

        # Score every level-8 candidate using full hierarchy wording + leaf wording
        scored: List[Tuple[float, Dict[str, Any], List[str], List[str]]] = []
        seen_codes: set[str] = set()
        for r in hs8_by_id.values():
            raw_code = str(r.get("code") or "")
            if not is_valid_hs_code(raw_code):
                continue
            norm_code = normalize_hs_code(raw_code)
            if norm_code in seen_codes:
                continue
            seen_codes.add(norm_code)

            h4 = parent_lookup.get((4, r.get("heading") or ""))
            h6 = parent_lookup.get((6, r.get("hs6") or ""))
            hierarchy_texts: List[str] = []
            if h4 and h4.get("source_text"):
                hierarchy_texts.append(f"Nhóm {h4['code']}: {h4['source_text']}")
            if h6 and h6.get("source_text"):
                hierarchy_texts.append(f"Phân nhóm {h6['code']}: {h6['source_text']}")

            leaf_text = str(r.get("source_text") or r.get("embedding_text") or "").strip()
            score, signals = _score_candidate(
                query_info,
                raw_code,
                leaf_text,
                hierarchy_texts,
                chapter=str(r.get("chapter") or ""),
            )
            score += float(r.get("lex_rank") or 0.0) * 1.2
            if score > 0:
                scored.append((round(score, 4), r, hierarchy_texts, signals))

        if not scored:
            return None

        scored.sort(key=lambda item: (-item[0], item[1].get("code") or ""))
        top_items = scored[: max(1, min(int(top_k or 5), 10))]
        top_score = top_items[0][0]

        # Fetch governing legal notes via rag.graph_edges for top candidates + their chapters/headings
        target_node_ids: List[str] = []
        chapters_hit: List[str] = []
        for _, row, _, _ in top_items:
            target_node_ids.append(row["id"])
            h4 = parent_lookup.get((4, row.get("heading") or ""))
            if h4:
                target_node_ids.append(h4["id"])
            if row.get("chapter") and row["chapter"] not in chapters_hit:
                chapters_hit.append(str(row["chapter"]))

        note_rows: List[Dict[str, Any]] = []
        if target_node_ids:
            note_rows.extend(
                query_rows(
                    """
                    SELECT DISTINCT c.id, c.code, c.chunk_type, c.chapter, c.section, c.source_text
                    FROM rag.graph_edges e
                    JOIN rag.chunks c
                      ON c.snapshot = e.snapshot
                     AND (
                         (e.source = ANY(%s) AND e.target = c.id AND e.relation = ANY(%s))
                         OR (e.target = ANY(%s) AND e.source = c.id AND e.relation = ANY(%s))
                     )
                    WHERE e.snapshot = %s
                      AND c.chunk_type IN ('section_note', 'chapter_note', 'subheading_note', 'legal_clause')
                    LIMIT 12
                    """,
                    (
                        target_node_ids,
                        list(NOTE_RELATIONS_FROM_TARIFF),
                        target_node_ids,
                        list(NOTE_RELATIONS_TO_TARIFF),
                        snapshot,
                    ),
                )
            )

        if not note_rows and chapters_hit:
            note_rows.extend(
                query_rows(
                    """
                    SELECT id, code, chunk_type, chapter, section, source_text
                    FROM rag.chunks
                    WHERE snapshot = %s
                      AND chunk_type IN ('chapter_note', 'section_note')
                      AND chapter = ANY(%s)
                    LIMIT 6
                    """,
                    (snapshot, chapters_hit),
                )
            )

        gir_rows = query_rows(
            """
            SELECT id, code, chunk_type, source_text
            FROM rag.chunks
            WHERE snapshot = %s AND chunk_type = 'gir_rule'
            ORDER BY id ASC
            LIMIT 4
            """,
            (snapshot,),
        )
        gir_list = [
            {
                "id": g["id"],
                "code": g.get("code") or g["id"],
                "chunk_type": "gir_rule",
                "text": " ".join(str(g.get("source_text") or "").split())[:240],
            }
            for g in gir_rows
        ]

        formatted_notes = [
            {
                "id": n["id"],
                "code": n.get("code") or "",
                "chunk_type": n.get("chunk_type") or "legal_note",
                "chapter": n.get("chapter") or "",
                "section": n.get("section") or "",
                "text": " ".join(str(n.get("source_text") or "").split())[:260],
            }
            for n in note_rows
        ]

        candidates: List[Dict[str, Any]] = []
        for score, row, hierarchy_texts, signals in top_items:
            formatted_code = normalize_hs_code(row["code"])
            raw_digits = re.sub(r"\D", "", formatted_code)
            leaf_desc = " ".join(str(row.get("source_text") or "").split())
            full_path = " → ".join([*hierarchy_texts, f"{formatted_code}: {leaf_desc}"])
            cand_notes = [
                n for n in formatted_notes
                if not n.get("chapter") or n.get("chapter") == str(row.get("chapter") or "")
            ][:3] or formatted_notes[:2]

            cand = {
                "node_id": row["id"],
                "hs_code": formatted_code,
                "hs_code_compact": raw_digits,
                "description": leaf_desc,
                "full_hierarchy_path": full_path,
                "chapter": str(row.get("chapter") or raw_digits[:2]),
                "heading": str(row.get("heading") or raw_digits[:4]),
                "section": str(row.get("section") or ""),
                "raw_score": score,
                "confidence_score": _raw_score_to_confidence(score, top_score),
                "matched_signals": signals,
                "evidence_sources": cand_notes,
            }
            cand["legal_basis"] = _format_legal_basis(cand, cand_notes, gir_list)
            candidates.append(cand)

        return {
            "retrieval_engine": "postgres_rag_graph",
            "snapshot": snapshot,
            "candidates": candidates,
            "legal_notes": formatted_notes[:6],
            "gir_rules": gir_list,
        }
    except Exception as exc:
        logger.warning("PostgreSQL RAG retrieval fallback triggered: %s", exc)
        return None
    finally:
        if close_fn:
            try:
                close_fn()
            except Exception:
                pass


def _retrieve_from_graph_corpus(
    query_info: Dict[str, Any],
    top_k: int = 5,
    corpus_nodes: Optional[List[Dict[str, Any]]] = None,
    corpus_edges: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Tier 2: Retrieve from `UnifiedGraphService` authoritative in-memory corpus
    (or injected node/edge fixtures for fast standalone unit testing).
    """
    engine_label = "injected_corpus"
    nodes_map: Dict[str, Dict[str, Any]] = {}
    parents_index: Dict[str, List[str]] = defaultdict(list)
    notes_index: Dict[str, List[str]] = defaultdict(list)

    if corpus_nodes is not None:
        for n in corpus_nodes:
            nid = n["id"]
            nodes_map[nid] = dict(n)
        for e in (corpus_edges or []):
            src, tgt, rel = e["source"], e["target"], e["relation"]
            if rel == "CONTAINS":
                parents_index[tgt].append(src)
            elif rel in NOTE_RELATIONS_FROM_TARIFF:
                notes_index[src].append(tgt)
            elif rel in NOTE_RELATIONS_TO_TARIFF:
                notes_index[tgt].append(src)
    else:
        engine_label = "inmemory_graph_corpus"
        ensure_ai_rag_path()
        try:
            from rag.graph.service import get_graph_service

            svc = get_graph_service()
            svc.load_inmemory_if_needed()
            nodes_map = svc._nodes
            parents_index = svc._parents_index
            notes_index = svc._notes_index
        except Exception as exc:
            logger.warning("UnifiedGraphService unavailable: %s", exc)
            return {
                "retrieval_engine": "unavailable",
                "candidates": [],
                "legal_notes": [],
                "gir_rules": [],
            }

    scored: List[Tuple[float, Dict[str, Any], List[str], List[str]]] = []
    seen_codes: set[str] = set()

    for nid, node in nodes_map.items():
        code = str(node.get("code") or "")
        digits = re.sub(r"\D", "", code)
        level = node.get("level")
        if level != 8 and len(digits) != 8:
            continue
        if not is_valid_hs_code(digits):
            continue
        norm_code = normalize_hs_code(digits)
        if norm_code in seen_codes:
            continue

        # Walk ancestors via CONTAINS edges
        ancestors: List[str] = []
        curr = nid
        for _ in range(4):
            ps = parents_index.get(curr) or []
            if not ps:
                break
            p_node = nodes_map.get(ps[0])
            if p_node and p_node.get("type") not in ("root", "section"):
                p_desc = str(p_node.get("description") or p_node.get("label") or "").strip()
                p_code = str(p_node.get("code") or "")
                ancestors.insert(0, f"{p_code}: {p_desc}" if p_code else p_desc)
            curr = ps[0]

        leaf_desc = str(node.get("description") or node.get("label") or "").strip()
        score, signals = _score_candidate(
            query_info,
            digits,
            leaf_desc,
            ancestors,
            chapter=str(node.get("chapter") or digits[:2]),
        )
        if score > 0:
            seen_codes.add(norm_code)
            scored.append((score, node, ancestors, signals))

    scored.sort(key=lambda item: (-item[0], str(item[1].get("code") or "")))
    top_items = scored[: max(1, min(int(top_k or 5), 10))]
    if not top_items:
        return {
            "retrieval_engine": engine_label,
            "candidates": [],
            "legal_notes": [],
            "gir_rules": [],
        }

    top_score = top_items[0][0]
    all_notes: List[Dict[str, Any]] = []
    seen_note_ids: set[str] = set()
    candidates: List[Dict[str, Any]] = []

    for score, node, ancestors, signals in top_items:
        nid = node["id"]
        formatted_code = normalize_hs_code(str(node.get("code") or ""))
        raw_digits = re.sub(r"\D", "", formatted_code)
        leaf_desc = " ".join(str(node.get("description") or node.get("label") or "").split())

        cand_notes: List[Dict[str, Any]] = []
        curr = nid
        for _ in range(4):
            for note_id in notes_index.get(curr, [])[:3]:
                n_obj = nodes_map.get(note_id)
                if not n_obj:
                    continue
                note_entry = {
                    "id": note_id,
                    "code": str(n_obj.get("code") or ""),
                    "chunk_type": str(n_obj.get("chunk_type") or n_obj.get("type") or "legal_note"),
                    "chapter": str(n_obj.get("chapter") or ""),
                    "section": str(n_obj.get("section") or ""),
                    "text": " ".join(str(n_obj.get("description") or n_obj.get("label") or "").split())[:260],
                }
                if note_id not in {x["id"] for x in cand_notes}:
                    cand_notes.append(note_entry)
                if note_id not in seen_note_ids:
                    seen_note_ids.add(note_id)
                    all_notes.append(note_entry)
            ps = parents_index.get(curr) or []
            if not ps:
                break
            curr = ps[0]

        full_path = " → ".join([*ancestors, f"{formatted_code}: {leaf_desc}"])
        cand = {
            "node_id": nid,
            "hs_code": formatted_code,
            "hs_code_compact": raw_digits,
            "description": leaf_desc,
            "full_hierarchy_path": full_path,
            "chapter": str(node.get("chapter") or raw_digits[:2]),
            "heading": raw_digits[:4],
            "section": str(node.get("section") or ""),
            "raw_score": score,
            "confidence_score": _raw_score_to_confidence(score, top_score),
            "matched_signals": signals,
            "evidence_sources": cand_notes[:3],
        }
        cand["legal_basis"] = _format_legal_basis(cand, cand_notes[:2], [])
        candidates.append(cand)

    return {
        "retrieval_engine": engine_label,
        "candidates": candidates,
        "legal_notes": all_notes[:6],
        "gir_rules": [],
    }


def _optional_llm_rerank(
    query_info: Dict[str, Any],
    candidates: List[Dict[str, Any]],
    legal_notes: List[Dict[str, Any]],
    timeout_seconds: float = 12.0,
) -> Optional[Dict[str, Any]]:
    """
    Tier 3: Optional bounded LLM reasoning via CLIProxyAPI.
    Strictly constrains the LLM to pick from retrieved candidates (zero hallucination).
    """
    if not candidates:
        return None
    ensure_ai_rag_path()
    try:
        from dataclasses import replace
        from config.settings import CLIProxyConfig
        from rag.llm.providers.cliproxy_client import CLIProxyClient

        cfg = replace(
            CLIProxyConfig.from_env(),
            timeout_seconds=float(timeout_seconds),
            transport_retries=0,
            max_output_tokens=512,
        )
        client = CLIProxyClient(cfg)
    except Exception as exc:
        logger.debug("CLIProxyClient unavailable for LLM rerank: %s", exc)
        return None

    allowed_codes = [c["hs_code"] for c in candidates]
    cand_lines = "\n".join(
        f"- {c['hs_code']} | {c['full_hierarchy_path'][:220]}"
        for c in candidates
    )
    note_lines = "\n".join(
        f"- {n['id']}: {n['text'][:180]}"
        for n in legal_notes[:4]
    ) or "(Áp dụng Quy tắc tổng quát GIR 1 và GIR 6 theo TT31/2022/TT-BTC)"

    schema = {
        "type": "object",
        "properties": {
            "selected_hs_code": {"type": "string", "enum": allowed_codes},
            "confidence_score": {"type": "number"},
            "gir_rationale_vi": {"type": "string"},
            "specialist_check_points": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["selected_hs_code", "confidence_score", "gir_rationale_vi", "specialist_check_points"],
        "additionalProperties": False,
    }
    messages = [
        {
            "role": "system",
            "content": (
                "Bạn là trợ lý phân loại mã HS Hải quan Việt Nam (TT31/2022/TT-BTC). "
                "CHỈ được chọn 1 mã HS phù hợp nhất từ danh sách ứng viên đã truy xuất, "
                "không tự bịa mã mới. Trả lời bằng tiếng Việt ngắn gọn, rõ căn cứ GIR."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Mô tả hàng hóa: {query_info['raw_query']}\n\n"
                f"Ứng viên HS truy xuất từ RAG:\n{cand_lines}\n\n"
                f"Chú giải pháp lý liên quan:\n{note_lines}"
            ),
        },
    ]

    try:
        resp = client.complete(messages, schema, model=os.getenv("HS_ADVISOR_LLM_MODEL") or "gemini-3-flash")
        parsed = json.loads(resp["content"])
        selected = normalize_hs_code(parsed.get("selected_hs_code", ""))
        if selected not in allowed_codes:
            return None
        conf = float(parsed.get("confidence_score") or 0)
        if 0 < conf <= 1.0:
            conf *= 100.0
        conf = round(max(40.0, min(95.0, conf or 80.0)), 1)
        return {
            "selected_hs_code": selected,
            "confidence_score": conf,
            "gir_rationale_vi": str(parsed.get("gir_rationale_vi") or "").strip(),
            "specialist_check_points": list(parsed.get("specialist_check_points") or [])[:4],
            "model": resp.get("model") or resp.get("requested_model"),
            "elapsed_ms": round(float(resp.get("elapsed_ms") or 0), 1),
        }
    except Exception as exc:
        logger.warning("LLM HS rerank skipped (falling back to deterministic RAG): %s", exc)
        return None


def recommend_hs_codes(
    item_description: str,
    material: Optional[str] = None,
    function: Optional[str] = None,
    top_k: int = 5,
    use_llm: bool = False,
    prefer_postgres: bool = True,
    corpus_nodes: Optional[List[Dict[str, Any]]] = None,
    corpus_edges: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Main entry point for AI/RAG HS code recommendation.
    Always preserves Human-in-the-loop governance (`requires_human_approval=True`,
    `automatic_hs_decision=False`).
    """
    query_info = extract_query_terms(item_description, material=material, function=function)
    if not query_info["raw_query"]:
        return {
            "success": False,
            "error": "Vui lòng cung cấp tên hoặc mô tả kỹ thuật mặt hàng để AI/RAG tra cứu mã HS.",
            "requires_human_approval": True,
            "automatic_hs_decision": False,
            "candidates": [],
        }

    retrieval: Optional[Dict[str, Any]] = None
    if corpus_nodes is not None:
        retrieval = _retrieve_from_graph_corpus(
            query_info, top_k=top_k, corpus_nodes=corpus_nodes, corpus_edges=corpus_edges
        )
    else:
        if prefer_postgres:
            retrieval = _retrieve_from_postgres(query_info, top_k=top_k)
        if not retrieval or not retrieval.get("candidates"):
            retrieval = _retrieve_from_graph_corpus(query_info, top_k=top_k)

    candidates = list((retrieval or {}).get("candidates") or [])
    legal_notes = list((retrieval or {}).get("legal_notes") or [])
    gir_rules = list((retrieval or {}).get("gir_rules") or [])
    engine = (retrieval or {}).get("retrieval_engine") or "unavailable"

    llm_meta: Optional[Dict[str, Any]] = None
    if use_llm and candidates:
        llm_meta = _optional_llm_rerank(query_info, candidates, legal_notes)
        if llm_meta:
            engine = f"{engine}+llm"
            selected_code = llm_meta["selected_hs_code"]
            candidates.sort(key=lambda c: (0 if c["hs_code"] == selected_code else 1, -c["raw_score"]))
            top_cand = candidates[0]
            top_cand["confidence_score"] = llm_meta["confidence_score"]
            top_cand["legal_basis"] = _format_legal_basis(
                top_cand,
                top_cand.get("evidence_sources") or legal_notes[:2],
                gir_rules,
                llm_rationale=llm_meta["gir_rationale_vi"],
            )
            top_cand["specialist_check_points"] = llm_meta.get("specialist_check_points") or []

    primary = candidates[0] if candidates else None
    return {
        "success": bool(primary),
        "error": None if primary else (
            "Không tìm thấy mã HS 8 chữ số khớp trong kho tri thức biểu thuế (Phần XIV/XVI/XVII). "
            "Chuyên viên vui lòng nhập bổ sung mô tả kỹ thuật (chất liệu, công dụng) hoặc chọn mã thủ công."
        ),
        "query": query_info["raw_query"],
        "retrieval_engine": engine,
        "snapshot": (retrieval or {}).get("snapshot"),
        "requires_human_approval": True,
        "automatic_hs_decision": False,
        "primary_recommendation": primary,
        "candidates": candidates,
        "legal_notes": legal_notes,
        "gir_rules": gir_rules,
        "llm_reasoning": llm_meta,
    }


__all__ = [
    "extract_query_terms",
    "recommend_hs_codes",
    "strip_accents",
]
