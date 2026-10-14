"""Writes a BLIND relabelling sheet: complaint text only, no AI labels, shuffled, row numbers instead of ids.
Give data/relabel_sheet.csv to a teammate who did NOT write the complaints. Keep data/relabel_key.csv to yourself."""
import pandas as pd
from core.config import COMPLAINTS, ROOT

SHEET = ROOT / "data" / "relabel_sheet.csv"
KEY = ROOT / "data" / "relabel_key.csv"

df = pd.read_csv(COMPLAINTS, encoding="utf-8-sig")
one_per_family = df.sample(frac=1, random_state=7).groupby("family").head(1)      # one language version per family
picked = one_per_family.groupby("owner_label").head(4)                            # up to 4 per department / MULTI / UNCLEAR
picked = picked.sample(frac=1, random_state=11).reset_index(drop=True)            # shuffled: order gives nothing away
picked["row_no"] = picked.index + 1

picked[["row_no", "id"]].to_csv(KEY, index=False)
sheet = picked[["row_no", "text"]].copy()
sheet["your_label"] = ""
sheet["notes"] = ""
sheet.to_csv(SHEET, index=False, encoding="utf-8-sig")                            # utf-8-sig so Excel shows Devanagari
print(f"Wrote {len(sheet)} complaints to {SHEET}\nKey (do NOT share) saved to {KEY}")