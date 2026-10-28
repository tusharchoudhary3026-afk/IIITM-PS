"""Engine 2: compound complaint splitter. Proposes only. A human confirms or merges back."""
import re
from . import router_baseline

CONNECTORS = r"\band\b|\baur\b|(?<!\S)और(?!\S)|\bplus\b|;|\.\s+(?=[A-Z\u0900-\u097F])"


def propose_split(text: str):
    parts = [p.strip() for p in re.split(CONNECTORS, text, flags=re.I) if p and len(p.strip()) > 8]
    if len(parts) < 2:
        return {"is_compound": False, "parts": [], "note": "single issue"}
    kw = router_baseline.load_keywords()
    routed = [(p, router_baseline.route(p, kw)) for p in parts]
    depts = {r["top3"][0]["dept"] for _, r in routed if r["top3"]}
    # Parts that map to one department, or have no signal, are NOT split.
    if len(depts) < 2:
        return {"is_compound": False, "parts": [],
                "note": "possible multi-clause text but one owner or unclear; kept intact"}
    return {"is_compound": True,
            "parts": [{"text": p, "suggestion": r} for p, r in routed],
            "note": "proposed split; needs human confirmation"}
