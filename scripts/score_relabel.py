# """Compares the teammate's labels with the AI labels. Run after data/relabel_sheet.csv is filled in."""
# import pandas as pd
# from sklearn.metrics import cohen_kappa_score
# from core.config import COMPLAINTS, ROOT

# SHEET = ROOT / "data" / "relabel_sheet.csv"
# KEY = ROOT / "data" / "relabel_key.csv"
# REPORT = ROOT / "data" / "relabel_report.txt"

# CANON = [("road", "Roads Dept"), ("drain", "Drainage Dept"), ("sanit", "Sanitation Dept"),
#          ("electric", "Electricity Dept"), ("water", "Water Supply Dept"),
#          ("multi", "MULTI"), ("both", "MULTI"), ("unclear", "UNCLEAR"), ("unsure", "UNCLEAR")]


# def canon(x):
#     s = str(x).strip().lower()
#     if not s or s == "nan":
#         return None
#     for key, name in CANON:
#         if s.startswith(key):
#             return name
#     return "UNRECOGNISED:" + s


# sheet = pd.read_csv(SHEET, encoding="utf-8-sig")
# key = pd.read_csv(KEY)
# ai = pd.read_csv(COMPLAINTS, encoding="utf-8-sig")[["id", "owner_label", "language", "text"]]
# d = sheet.merge(key, on="row_no").merge(ai, on="id", suffixes=("", "_ai"))
# d["human"] = d["your_label"].map(canon)
# blank = int(d["human"].isna().sum())
# bad = d[d["human"].fillna("").str.startswith("UNRECOGNISED")]
# d = d[d["human"].notna() & ~d["human"].fillna("").str.startswith("UNRECOGNISED")]

# who = sorted(set(sheet["labeller"].dropna().astype(str)) - {""}) if "labeller" in sheet.columns else []
# n = len(d)
# agree = int((d["human"] == d["owner_label"]).sum())
# lines = [f"Independent relabelling check (human vs AI labels), n = {n} complaints",
#          f"Agreement: {agree} of {n} ({agree / n:.0%})" if n else "No usable labels found"]
# lines.append("Labelled by: " + (", ".join(who) if who else "not recorded"))
# if n and d["human"].nunique() > 1 or n and d["owner_label"].nunique() > 1:
#     lines.append(f"Cohen's kappa: {cohen_kappa_score(d['human'], d['owner_label']):.2f}")
# for lang, g in d.groupby("language"):
#     lines.append(f"  {lang}: {int((g['human'] == g['owner_label']).sum())} of {len(g)} agree")
# for lab, g in d.groupby("owner_label"):
#     lines.append(f"  AI label {lab}: {int((g['human'] == g['owner_label']).sum())} of {len(g)} agree")
# if blank or len(bad):
#     lines.append(f"Skipped: {blank} blank, {len(bad)} unrecognised labels")
# lines.append("\nDisagreements (read these; each is either an AI label error or a genuinely ambiguous complaint):")
# for _, r in d[d["human"] != d["owner_label"]].iterrows():
#     lines.append(f"  row {r['row_no']}: AI={r['owner_label']} | human={r['human']} | {r['text']}"
#                  + (f" | note: {r['notes']}" if isinstance(r.get('notes'), str) else ""))
# lines.append("\nThis is one teammate's labels on a sample. It checks the AI labels; it does not make the dataset human-verified.")
# out = "\n".join(lines)
# REPORT.write_text(out, encoding="utf-8")
# print(out)

"""Compares the teammate's labels with the AI labels. Run after data/relabel_sheet.csv is filled in."""
import pandas as pd
from sklearn.metrics import cohen_kappa_score
from core.config import COMPLAINTS, ROOT

SHEET = ROOT / "data" / "relabel_sheet.csv"
KEY = ROOT / "data" / "relabel_key.csv"
REPORT = ROOT / "data" / "relabel_report.txt"

CANON = [("road", "Roads Dept"), ("drain", "Drainage Dept"), ("sanit", "Sanitation Dept"),
         ("electric", "Electricity Dept"), ("water", "Water Supply Dept"),
         ("multi", "MULTI"), ("both", "MULTI"), ("unclear", "UNCLEAR"), ("unsure", "UNCLEAR")]


def canon(x):
    s = str(x).strip().lower()
    if not s or s == "nan":
        return None
    for key, name in CANON:
        if s.startswith(key):
            return name
    return "UNRECOGNISED:" + s


sheet = pd.read_csv(SHEET, encoding="utf-8-sig")
key = pd.read_csv(KEY)
ai = pd.read_csv(COMPLAINTS, encoding="utf-8-sig")[["id", "owner_label", "language", "text"]]
d = sheet.merge(key, on="row_no").merge(ai, on="id", suffixes=("", "_ai"))
d["human"] = d["your_label"].map(canon)
blank = int(d["human"].isna().sum())
bad = d[d["human"].fillna("").str.startswith("UNRECOGNISED")]
d = d[d["human"].notna() & ~d["human"].fillna("").str.startswith("UNRECOGNISED")]

who = sorted(set(sheet["labeller"].dropna().astype(str)) - {""}) if "labeller" in sheet.columns else []
n = len(d)
agree = int((d["human"] == d["owner_label"]).sum())
lines = [f"Independent relabelling check (human vs AI labels), n = {n} complaints",
         f"Agreement: {agree} of {n} ({agree / n:.0%})" if n else "No usable labels found",
         f"Labelled by {len(who)} person(s): " + (", ".join(who) if who else "not recorded")]
if n:
    counts = d["human"].value_counts()
    lines.append("Human label counts: " + ", ".join(f"{k} {v}" for k, v in counts.items()))
    if counts.iloc[0] / n > 0.8 or len(who) > 5:
        lines.append(f"WARNING: SUSPICIOUS SHEET. '{counts.iloc[0] and counts.index[0]}' is {counts.iloc[0]} of {n} labels "
                     f"and/or there are {len(who)} different labellers. This usually means a click or instruction "
                     "problem, not real disagreement. Do NOT report this agreement figure; redo the labelling "
                     "with one or two named people.")
if n and (d["human"].nunique() > 1 or d["owner_label"].nunique() > 1):
    lines.append(f"Cohen's kappa: {cohen_kappa_score(d['human'], d['owner_label']):.2f}")
for lang, g in d.groupby("language"):
    lines.append(f"  {lang}: {int((g['human'] == g['owner_label']).sum())} of {len(g)} agree")
for lab, g in d.groupby("owner_label"):
    lines.append(f"  AI label {lab}: {int((g['human'] == g['owner_label']).sum())} of {len(g)} agree")
if blank or len(bad):
    lines.append(f"Skipped: {blank} blank, {len(bad)} unrecognised labels")
lines.append("\nDisagreements (read these; each is either an AI label error or a genuinely ambiguous complaint):")
for _, r in d[d["human"] != d["owner_label"]].iterrows():
    lines.append(f"  row {r['row_no']}: AI={r['owner_label']} | human={r['human']} | {r['text']}"
                 + (f" | note: {r['notes']}" if isinstance(r.get('notes'), str) else ""))
lines.append("\nThis is a sample labelled by the named person(s) above. It checks the AI labels; it does not make the dataset human-verified.")
out = "\n".join(lines)
REPORT.write_text(out, encoding="utf-8")
print(out)