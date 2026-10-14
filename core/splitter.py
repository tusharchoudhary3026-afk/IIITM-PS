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
from collections import Counter
from . import router_baseline, intake
from .db import insert_complaint, insert_suggestion, fetch_all
from .ledger import log_event

CONNECTORS = r"\band\b|\baur\b|(?<!\S)और(?!\S)|\bplus\b|;|\.\s+(?=[A-Z\u0900-\u097F])"


def lead_department(parts):
    """Thin proposal: most common top department. Tie -> None (human decides)."""
    top = [p["suggestion"]["top3"][0]["dept"] for p in parts if p["suggestion"]["top3"]]
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
    depts = {r["top3"][0]["dept"] for _, r in routed if r["top3"]}
    if len(depts) < 2:
        return {"is_compound": False, "parts": [], "lead": None,
                "note": "possible multi-clause text but one owner or unclear; kept intact"}
    out = [{"text": p, "suggestion": r} for p, r in routed]
    return {"is_compound": True, "parts": out, "lead": lead_department(out),
            "note": "proposed split; needs human confirmation"}


def confirm_split(parent_id: int, case_id: str, parts: list, actor: str = "reviewer"):
    """Human-confirmed split. Children link via parent_id; case ids share the parent's prefix."""
    ids = []
    for i, p in enumerate(parts, 1):
        rec = intake.process(p["text"])
        rec["case_id"], rec["parent_id"] = f"{case_id}-{i}", parent_id
        cid = insert_complaint(rec)
        s = p["suggestion"]
        insert_suggestion(cid, "baseline", s["top3"], s["evidence"], s["confidence"], s["abstained"])
        top = s["top3"][0]["dept"] if s["top3"] and not s["abstained"] else None
        log_event(cid, "suggested", "system", suggested_dept=top, details={"parent_id": parent_id})
        ids.append(cid)
    log_event(parent_id, "split_confirmed", actor, details={"children": ids})
    return ids


def merge_back(parent_id: int, actor: str = "reviewer"):
    """Append-only: children stay in the table; the ledger records the merge-back."""
    kids = fetch_all("SELECT id FROM complaints WHERE parent_id=?", (parent_id,))
    for k in kids:
        log_event(k["id"], "split_merged_back", actor)
    log_event(parent_id, "split_merged_back", actor, details={"children": [k["id"] for k in kids]})
    return len(kids)