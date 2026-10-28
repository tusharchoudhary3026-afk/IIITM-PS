"""Engine 10: Reassignment Analytics & Hotspot Detection (Thin analytics based on decision ledger)."""
import pandas as pd
from core.db import fetch_all
from core.config import SIM_LABEL, REASON_CODES

def get_reassignment_breakdown():
    """Aggregates transfer counts and denominators grouped by official reason codes from the ledger."""
    rows = fetch_all("SELECT reason_code, COUNT(*) as count FROM ledger WHERE reason_code IS NOT NULL GROUP BY reason_code")
    if not rows:
        return {code: 0 for code in REASON_CODES}
    
    breakdown = {row["reason_code"]: row["count"] for row in rows}
    # Ensure all official reason codes are represented
    for code in REASON_CODES:
        if code not in breakdown:
            breakdown[code] = 0
    return breakdown


def detect_emerging_hotspots(min_count: int = 3):
    """Aggregates complaints by location and issue category to flag potential emerging hotspots (No map required)."""
    rows = fetch_all("SELECT location, issue FROM complaints WHERE location != 'unknown' AND location IS NOT NULL")
    if not rows:
        return []
    
    df = pd.DataFrame(rows)
    grouped = df.groupby(["location", "issue"]).size().reset_index(name="observed_count")
    hotspots = grouped[grouped["observed_count"] >= min_count].sort_values(by="observed_count", ascending=False)
    
    results = []
    for _, row in hotspots.iterrows():
        results.append({
            "location": row["location"],
            "category": row["issue"],
            "observed_count": int(row["observed_count"]),
            "baseline_average": 1.0,
            "status_label": SIM_LABEL  # Mandatory simulation label governance rule
        })
    return results


def get_case_reassignment_timeline(complaint_id: int):
    """Retrieves the per-case chronological reassignment timeline from logged events."""
    return fetch_all(
        "SELECT event_type, actor, suggested_dept, final_dept, reason, reason_code, timestamp "
        "FROM ledger WHERE complaint_id = ? ORDER BY id ASC",
        (complaint_id,)
    )