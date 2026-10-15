# """Engine 6: ownership-conflict checker. Flags overlap; never decides."""
# import pandas as pd
# from .config import RESP_TABLE


# def load_table():
#     return pd.read_csv(RESP_TABLE, encoding='utf-8-sig')


# def check(dept: str, table=None):
#     t = table if table is not None else load_table()
#     out = []
#     for _, r in t[t["owner"] == dept].iterrows():
#         if isinstance(r["overlap_owner"], str) and r["overlap_owner"].strip():
#             out.append({"issue_type": r["issue_type"], "owner": r["owner"],
#                         "overlap_owner": r["overlap_owner"], "source": r["source"],
#                         "verification": r["verification"]})
#     return out


# def detect_bounce(history: list[dict]):
#     """Pattern flag only (A -> B -> A), no blame."""
#     seq = []
#     for h in history:
#         if not seq and h.get("suggested_dept"):
#             seq.append(h["suggested_dept"])            # starting owner
#         if h.get("final_dept") and (not seq or seq[-1] != h["final_dept"]):
#             seq.append(h["final_dept"])
#     for i in range(len(seq) - 2):
#         if seq[i] == seq[i + 2] and seq[i] != seq[i + 1]:
#             return {"pattern": f"{seq[i]} -> {seq[i+1]} -> {seq[i+2]}"}
#     return None





"""Engine 6: ownership-conflict checker. Flags overlap; never decides."""
import pandas as pd
from .config import RESP_TABLE


def load_table():
    return pd.read_csv(RESP_TABLE, encoding='utf-8-sig')


def check(dept: str, table=None):
    t = table if table is not None else load_table()
    out = []
    for _, r in t[t["owner"] == dept].iterrows():
        if isinstance(r["overlap_owner"], str) and r["overlap_owner"].strip():
            out.append({"issue_type": r["issue_type"], "owner": r["owner"],
                        "overlap_owner": r["overlap_owner"], "source": r["source"],
                        "verification": r["verification"]})
    return out


def unverified_rows(table=None):
    t = table if table is not None else load_table()
    return t[t["verification"].astype(str).str.upper() == "ASSUMPTION"]


def owner_sequence(history: list[dict]):
    seq = []
    for h in history:
        if not seq and h.get("suggested_dept"):
            seq.append(h["suggested_dept"])            # starting owner
        if h.get("final_dept") and (not seq or seq[-1] != h["final_dept"]):
            seq.append(h["final_dept"])
    return seq


def detect_bounce(history: list[dict]):
    """Pattern flag only (A -> B -> A), no blame."""
    seq = owner_sequence(history)
    for i in range(len(seq) - 2):
        if seq[i] == seq[i + 2] and seq[i] != seq[i + 1]:
            return {"pattern": f"{seq[i]} -> {seq[i+1]} -> {seq[i+2]}"}
    return None


def repeat_reassignment(history: list[dict], min_moves: int = 2):
    """Flag when owner changed at least `min_moves` times. Pattern only, no blame."""
    seq = owner_sequence(history)
    if len(seq) - 1 >= min_moves:
        return {"moves": len(seq) - 1, "path": " -> ".join(seq)}
    return None


OVERLAP_CUES = {
    "waterlogging on road": ("waterlogging", "waterlogged", "flood", "paani bhara", "पानी भर"),
    "open manhole / missing drain cover": ("manhole", "missing drain cover", "open drain cover", "मैनहोल"),
    "burst water pipe flooding road": ("burst pipe", "burst water pipe", "pipeline leak", "pipe burst"),
}


def check_suggestions(depts: list, complaint_text: str = "", table=None):
    """Flag only when both departments and a cue for that overlap are present."""
    t = table if table is not None else load_table()
    text = str(complaint_text).lower()
    out = []
    for _, r in t.iterrows():
        ov = r["overlap_owner"]
        cues = OVERLAP_CUES.get(str(r["issue_type"]).strip().lower(), ())
        issue_matches = any(cue.lower() in text for cue in cues)
        if (isinstance(ov, str) and ov.strip() and r["owner"] in depts and ov in depts
                and issue_matches):
            out.append({"issue_type": r["issue_type"], "owner": r["owner"], "overlap_owner": ov,
                        "source": r["source"], "verification": r["verification"]})
    return out
