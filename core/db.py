import json
import sqlite3
from .config import DB_PATH, SCHEMA_PATH


def get_conn():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_conn()
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    conn.commit()
    conn.close()


def insert_complaint(rec: dict) -> int:
    cols = ["case_id", "parent_id", "original_text", "language", "normalized_text",
            "channel", "location", "issue", "requested_action", "missing_fields", "is_synthetic"]
    vals = [rec.get(k) for k in cols]
    conn = get_conn()
    cur = conn.execute(
        f"INSERT INTO complaints ({','.join(cols)}) VALUES ({','.join('?'*len(cols))})", vals)
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def insert_suggestion(complaint_id, method, top3, evidence, confidence, abstained):
    conn = get_conn()
    conn.execute(
        "INSERT INTO suggestions (complaint_id, method, top3, evidence, confidence, abstained) "
        "VALUES (?,?,?,?,?,?)",
        (complaint_id, method, json.dumps(top3), json.dumps(evidence), confidence, int(abstained)))
    conn.commit()
    conn.close()


def execute(sql, params=()):
    conn = get_conn()
    try:
        conn.execute(sql, params)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def fetch_all(sql, params=()):
    conn = get_conn()
    rows = [dict(r) for r in conn.execute(sql, params).fetchall()]
    conn.close()
    return rows
