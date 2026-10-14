# # from pathlib import Path

# # ROOT = Path(__file__).resolve().parent.parent
# # DB_PATH = ROOT / "db" / "nyayaflow.db"
# # SCHEMA_PATH = ROOT / "db" / "schema.sql"
# # RESP_TABLE = ROOT / "data" / "responsibility_table.csv"
# # KEYWORDS = ROOT / "data" / "keywords.csv"
# # COMPLAINTS = ROOT / "data" / "complaints.csv"

# # REASON_CODES = ["wrong_category", "missing_info", "overlapping_ownership", "duplicate_report", "other"]
# # REVIEW_ACTIONS = ["accept", "edit", "clarify", "escalate"]
# # REASON_REQUIRED = {"edit", "escalate"}

# # # Team sets this on a validation split (see scripts/evaluate.py). Placeholder only.
# # CONFIDENCE_THRESHOLD = 0.40

# # SIM_LABEL = "SIMULATED / SYNTHETIC DATA - not real municipal data"



# import json
# from pathlib import Path

# ROOT = Path(__file__).resolve().parent.parent
# DB_PATH = ROOT / "db" / "nyayaflow.db"
# SCHEMA_PATH = ROOT / "db" / "schema.sql"
# RESP_TABLE = ROOT / "data" / "responsibility_table.csv"
# KEYWORDS = ROOT / "data" / "keywords.csv"
# COMPLAINTS = ROOT / "data" / "complaints.csv"
# THRESHOLD_FILE = ROOT / "data" / "threshold.json"

# REASON_CODES = ["wrong_category", "missing_info", "overlapping_ownership", "duplicate_report", "other"]
# REVIEW_ACTIONS = ["accept", "edit", "clarify", "escalate"]
# REASON_REQUIRED = {"edit", "escalate"}
# CODE_REQUIRED = {"edit", "escalate"}          # transfer-reason code mandatory on reassignment

# CONFIDENCE_THRESHOLD = 0.40   # keyword baseline: share of keyword hits (placeholder, own scale)


# def _load_tfidf_threshold():
#     try:
#         return float(json.loads(THRESHOLD_FILE.read_text())["tfidf"])
#     except Exception:
#         return 0.40            # until scripts/evaluate_full.py picks one on the validation split


# TFIDF_THRESHOLD = _load_tfidf_threshold()

# SIM_LABEL = "SIMULATED / SYNTHETIC DATA - not real municipal data"



import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "db" / "nyayaflow.db"
SCHEMA_PATH = ROOT / "db" / "schema.sql"
RESP_TABLE = ROOT / "data" / "responsibility_table.csv"
KEYWORDS = ROOT / "data" / "keywords.csv"
COMPLAINTS = ROOT / "data" / "complaints.csv"
THRESHOLD_FILE = ROOT / "data" / "threshold.json"

REASON_CODES = ["wrong_category", "missing_info", "overlapping_ownership", "duplicate_report", "other"]
REVIEW_ACTIONS = ["accept", "edit", "clarify", "escalate"]
REASON_REQUIRED = {"edit", "escalate"}
CODE_REQUIRED = {"edit", "escalate"}          # transfer-reason code mandatory on reassignment

CONFIDENCE_THRESHOLD = 0.40   # keyword baseline: share of keyword hits (placeholder, own scale)


def _load_tfidf_threshold():
    try:
        return float(json.loads(THRESHOLD_FILE.read_text())["tfidf"])
    except Exception:
        return 0.40            # until scripts/evaluate_full.py picks one on the validation split


TFIDF_THRESHOLD = _load_tfidf_threshold()

SIM_LABEL = "SIMULATED / SYNTHETIC DATA - not real municipal data"