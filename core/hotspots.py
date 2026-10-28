"""Engine 10 / Analytics: Hotspot Detection (Without a Map)."""
import pandas as pd
from datetime import datetime, timedelta
from .config import COMPLAINTS, SIM_LABEL
from .db import fetch_all


def detect_hotspots(min_count: int = 3):
    """Aggregates complaints by location and issue category to flag potential hotspots."""
    rows = fetch_all("SELECT location, issue, created_at FROM complaints WHERE location != 'unknown'")
    if not rows:
        return []
    
    df = pd.DataFrame(rows)
    # Group by location and issue category
    grouped = df.groupby(["location", "issue"]).size().reset_index(name="observed_count")
    
    # Filter by threshold rule (e.g., observed count >= min_count)
    hotspots = grouped[grouped["observed_count"] >= min_count].sort_values(by="observed_count", ascending=False)
    
    results = []
    for _, row in hotspots.iterrows():
        results.append({
            "location": row["location"],
            "category": row["issue"],
            "observed_count": int(row["observed_count"]),
            "baseline_average": 1.0,  # Simulated baseline for comparison
            "status_label": SIM_LABEL
        })
        
    return results