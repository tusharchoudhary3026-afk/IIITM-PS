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


def detect_bounce(history: list[dict]):
    """Pattern flag only (A -> B -> A), no blame."""
    seq = []
    for h in history:
        if not seq and h.get("suggested_dept"):
            seq.append(h["suggested_dept"])            # starting owner
        if h.get("final_dept") and (not seq or seq[-1] != h["final_dept"]):
            seq.append(h["final_dept"])
    for i in range(len(seq) - 2):
        if seq[i] == seq[i + 2] and seq[i] != seq[i + 1]:
            return {"pattern": f"{seq[i]} -> {seq[i+1]} -> {seq[i+2]}"}
    return None
