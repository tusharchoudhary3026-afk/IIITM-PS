"""Engine 8 - Component 1: Frozen Held-Out Split Leakage Guard Verification."""
import pandas as pd
from core.config import COMPLAINTS

def verify_split_leakage():
    df = pd.read_csv(COMPLAINTS, encoding="utf-8-sig")
    
    # Check if 'family' and 'split' columns exist
    if "family" not in df.columns or "split" not in df.columns:
        print("Dataset missing 'family' or 'split' columns.")
        return
    
    # Group by family and check unique splits assigned
    leakage_check = df.groupby("family")["split"].nunique()
    leaked_families = leakage_check[leakage_check > 1]
    
    print(f"Total complaint rows: {len(df)}")
    print(f"Total unique complaint families: {df['family'].nunique()}")
    
    if len(leaked_families) == 0:
        print("SUCCESS: Zero data leakage. Each complaint family resides entirely within a single split (train, val, or test).")
    else:
        print(f"WARNING: Leakage detected! Families appearing in multiple splits: {list(leaked_families.index)}")

if __name__ == "__main__":
    verify_split_leakage()