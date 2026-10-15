# """Engine 2: compound complaint splitter. Proposes only. A human confirms or merges back."""
# import re
# from . import router_baseline

# CONNECTORS = r"\band\b|\baur\b|(?<!\S)और(?!\S)|\bplus\b|;|\.\s+(?=[A-Z\u0900-\u097F])"


# def propose_split(text: str):
#     parts = [p.strip() for p in re.split(CONNECTORS, text, flags=re.I) if p and len(p.strip()) > 8]
#     if len(parts) < 2:
#         return {"is_compound": False, "parts": [], "note": "single issue"}
#     kw = router_baseline.load_keywords()
#     routed = [(p, router_baseline.route(p, kw)) for p in parts]
#     depts = {r["top3"][0]["dept"] for _, r in routed if r["top3"]}
#     # Parts that map to one department, or have no signal, are NOT split.
#     if len(depts) < 2:
#         return {"is_compound": False, "parts": [],
#                 "note": "possible multi-clause text but one owner or unclear; kept intact"}
#     return {"is_compound": True,
#             "parts": [{"text": p, "suggestion": r} for p, r in routed],
#             "note": "proposed split; needs human confirmation"}




"""Engine 2: compound complaint splitter. Proposes only. A human confirms or merges back."""
import re
import json
from collections import Counter
from . import router_baseline, intake
from .db import get_conn

CONNECTORS = r"\band\b|\baur\b|(?<!\S)और(?!\S)|\bplus\b|;|\.\s+(?=[A-Z\u0900-\u097F])"


def lead_department(parts):
    """Thin proposal: most common top department. Tie -> None (human decides)."""
    top = [p["suggestion"]["top3"][0]["dept"] for p in parts
           if p["suggestion"]["top3"] and not p["suggestion"]["abstained"]]
    c = Counter(top).most_common()
    if not c or (len(c) > 1 and c[0][1] == c[1][1]):
        return None
    return c[0][0]


def propose_split(text: str):
    parts = [p.strip() for p in re.split(CONNECTORS, text, flags=re.I) if p and len(p.strip()) > 8]
    if len(parts) < 2:
        return {"is_compound": False, "parts": [], "lead": None, "note": "single issue"}
    kw = router_baseline.load_keywords()
    routed = [(p, router_baseline.route(p, kw)) for p in parts]
    depts = {r["top3"][0]["dept"] for _, r in routed
             if r["top3"] and not r["abstained"]}
    if len(depts) < 2:
        return {"is_compound": False, "parts": [], "lead": None,
                "note": "possible multi-clause text but one owner or unclear; kept intact"}
    out = [{"text": p, "suggestion": r} for p, r in routed]
    return {"is_compound": True, "parts": out, "lead": lead_department(out),
            "note": "proposed split; needs human confirmation"}


def confirm_split(parent_id: int, case_id: str, parts: list, actor: str = "reviewer"):
    """Human-confirmed split. Children link via parent_id; case ids share the parent's prefix."""
    if not parts:
        raise ValueError("A split must contain at least one sub-issue.")
    ids = []
    conn = get_conn()
    try:
        with conn:
            parent = conn.execute(
                "SELECT channel, location FROM complaints WHERE id=?", (parent_id,)
            ).fetchone()
            if parent is None:
                raise ValueError(f"Parent complaint {parent_id} does not exist.")
            existing = conn.execute(
                "SELECT 1 FROM complaints WHERE parent_id=? LIMIT 1", (parent_id,)
            ).fetchone()
            if existing:
                raise ValueError("This complaint already has sub-issues; refusing to create duplicates.")

            for i, p in enumerate(parts, 1):
                rec = intake.process(
                    p["text"], channel=parent["channel"] or "portal",
                    location_hint=parent["location"] if parent["location"] != "unknown" else None,
                )
                rec["case_id"], rec["parent_id"] = f"{case_id}-{i}", parent_id
                cols = ["case_id", "parent_id", "original_text", "language", "normalized_text",
                        "channel", "location", "issue", "requested_action", "missing_fields", "is_synthetic"]
                vals = [rec.get(k) for k in cols]
                cur = conn.execute(
                    f"INSERT INTO complaints ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
                    vals,
                )
                cid = cur.lastrowid
                s = p["suggestion"]
                conn.execute(
                    "INSERT INTO suggestions (complaint_id, method, top3, evidence, confidence, abstained) "
                    "VALUES (?,?,?,?,?,?)",
                    (cid, "baseline", json.dumps(s["top3"]), json.dumps(s["evidence"]),
                     s["confidence"], int(s["abstained"])),
                )
                top = s["top3"][0]["dept"] if s["top3"] and not s["abstained"] else None
                conn.execute(
                    "INSERT INTO ledger (complaint_id, event_type, actor, suggested_dept, details) "
                    "VALUES (?,?,?,?,?)",
                    (cid, "suggested", "system", top, json.dumps({"parent_id": parent_id})),
                )
                ids.append(cid)
            conn.execute(
                "INSERT INTO ledger (complaint_id, event_type, actor, details) VALUES (?,?,?,?)",
                (parent_id, "split_confirmed", actor, json.dumps({"children": ids})),
            )
    finally:
        conn.close()
    return ids


def merge_back(parent_id: int, actor: str = "reviewer"):
    """Append-only: children stay in the table; the ledger records the merge-back."""
    conn = get_conn()
    try:
        with conn:
            kids = [r[0] for r in conn.execute(
                "SELECT id FROM complaints WHERE parent_id=? ORDER BY id", (parent_id,)
            ).fetchall()]
            last_split_action = conn.execute(
                "SELECT event_type FROM ledger WHERE complaint_id=? "
                "AND event_type IN ('split_confirmed', 'split_merged_back') ORDER BY id DESC LIMIT 1",
                (parent_id,),
            ).fetchone()
            if last_split_action and last_split_action[0] == "split_merged_back":
                raise ValueError("This split has already been merged back.")
            conn.executemany(
                "INSERT INTO ledger (complaint_id, event_type, actor) VALUES (?, 'split_merged_back', ?)",
                [(kid, actor) for kid in kids],
            )
            conn.execute(
                "INSERT INTO ledger (complaint_id, event_type, actor, details) VALUES (?, 'split_merged_back', ?, ?)",
                (parent_id, actor, json.dumps({"children": kids})),
            )
    finally:
        conn.close()
    return len(kids)
