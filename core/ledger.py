# """Append-only decision ledger. Corrections ADD rows; old rows are never changed."""
# import json
# from .config import REASON_REQUIRED
# from .db import execute, fetch_all


# def log_event(complaint_id, event_type, actor, suggested_dept=None, final_dept=None,
#               reason=None, reason_code=None, details=None):
#     if event_type in REASON_REQUIRED and not (reason or "").strip():
#         raise ValueError(f"A reason is mandatory for '{event_type}'.")
#     execute(
#         "INSERT INTO ledger (complaint_id, event_type, actor, suggested_dept, final_dept, "
#         "reason, reason_code, details) VALUES (?,?,?,?,?,?,?,?)",
#         (complaint_id, event_type, actor, suggested_dept, final_dept, reason, reason_code,
#          json.dumps(details) if details else None))


# def history(complaint_id):
#     return fetch_all("SELECT * FROM ledger WHERE complaint_id=? ORDER BY id", (complaint_id,))


# def save_correction(complaint_id, text, wrong_dept, correct_dept):
#     """Stored as a labelled example only. No automatic retraining."""
#     execute("INSERT INTO corrections (complaint_id, text, wrong_dept, correct_dept) VALUES (?,?,?,?)",
#             (complaint_id, text, wrong_dept, correct_dept))




"""Append-only decision ledger. Corrections ADD rows; old rows are never changed."""
import json
from .config import REASON_REQUIRED, CODE_REQUIRED, REASON_CODES
from .db import execute, fetch_all


def log_event(complaint_id, event_type, actor, suggested_dept=None, final_dept=None,
              reason=None, reason_code=None, details=None):
    if event_type in REASON_REQUIRED and not (reason or "").strip():
        raise ValueError(f"A reason is mandatory for '{event_type}'.")
    if event_type in CODE_REQUIRED:
        if reason_code not in REASON_CODES:
            raise ValueError("A transfer-reason code is mandatory for edit / escalate.")
        if reason_code == "other" and not (reason or "").strip():
            raise ValueError("Code 'other' needs a free-text reason.")
    execute(
        "INSERT INTO ledger (complaint_id, event_type, actor, suggested_dept, final_dept, "
        "reason, reason_code, details) VALUES (?,?,?,?,?,?,?,?)",
        (complaint_id, event_type, actor, suggested_dept, final_dept, reason, reason_code,
         json.dumps(details) if details else None))


def history(complaint_id):
    return fetch_all("SELECT * FROM ledger WHERE complaint_id=? ORDER BY id", (complaint_id,))


def save_correction(complaint_id, text, wrong_dept, correct_dept):
    """Stored as a labelled example only. No automatic retraining."""
    execute("INSERT INTO corrections (complaint_id, text, wrong_dept, correct_dept) VALUES (?,?,?,?)",
            (complaint_id, text, wrong_dept, correct_dept))