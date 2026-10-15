"""Engine 3: keyword/rule baseline. Build and evaluate this BEFORE any ML."""
import re
import pandas as pd
from .config import KEYWORDS, CONFIDENCE_THRESHOLD


def load_keywords():
    df = pd.read_csv(KEYWORDS, encoding='utf-8-sig')
    out = {}
    for _, r in df.iterrows():
        out.setdefault(r["department"], []).append(str(r["keyword"]).lower())
    return out


def route(text: str, kw=None):
    kw = load_keywords() if kw is None else kw
    t = text.lower()
    scores, evidence = {}, {}
    for dept, words in kw.items():
        hits = []
        for word in words:
            term = str(word).strip().lower()
            if not term:
                continue
            if re.search(r"[A-Za-z]", term):
                matched = re.search(rf"(?<!\w){re.escape(term)}(?!\w)", t) is not None
            else:
                # Python's \w boundaries split some Devanagari combining marks.
                matched = term in t
            if matched:
                hits.append(term)
        if hits:
            scores[dept] = len(hits)
            evidence[dept] = hits
    if not scores:
        return {"top3": [], "evidence": {}, "confidence": 0.0, "abstained": True}
    total = sum(scores.values())
    ranked = sorted(scores.items(), key=lambda x: -x[1])[:3]
    top3 = [{"dept": d, "score": round(s / total, 2)} for d, s in ranked]
    conf = top3[0]["score"]
    tie = len(ranked) > 1 and ranked[0][1] == ranked[1][1]
    abstained = conf < CONFIDENCE_THRESHOLD or tie
    return {"top3": top3, "evidence": {d: evidence[d] for d, _ in ranked},
            "confidence": conf, "abstained": abstained}
