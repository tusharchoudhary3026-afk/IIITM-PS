-- NyayaFlow schema. All demo data is SYNTHETIC.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS complaints (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id         TEXT NOT NULL,              -- shared by parent + sub-issues
    parent_id       INTEGER REFERENCES complaints(id),  -- NULL for the original complaint
    original_text   TEXT NOT NULL,              -- NEVER modified
    language        TEXT NOT NULL,              -- english | hindi | hinglish | uncertain
    normalized_text TEXT,                       -- separate field, Hinglish normalisation
    channel         TEXT DEFAULT 'portal',      -- portal | phone | social | in-person
    location        TEXT DEFAULT 'unknown',     -- never invented
    issue           TEXT,
    requested_action TEXT,
    missing_fields  TEXT,                       -- comma-separated
    is_synthetic    INTEGER NOT NULL DEFAULT 1,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS suggestions (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    complaint_id  INTEGER NOT NULL REFERENCES complaints(id),
    method        TEXT NOT NULL,                -- baseline | tfidf_lr
    top3          TEXT NOT NULL,                -- JSON: [{dept, score}]
    evidence      TEXT,                         -- JSON: matched words / rules
    confidence    REAL,
    abstained     INTEGER NOT NULL DEFAULT 0,   -- 1 = manual queue
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Append-only decision ledger (see triggers below)
CREATE TABLE IF NOT EXISTS ledger (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    complaint_id    INTEGER NOT NULL REFERENCES complaints(id),
    event_type      TEXT NOT NULL,   -- suggested | accept | edit | clarify | escalate | challenge | challenge_resolved | transfer
    actor           TEXT NOT NULL,   -- system | operator | reviewer | citizen
    suggested_dept  TEXT,
    final_dept      TEXT,
    reason          TEXT,            -- mandatory on edit / escalate / transfer
    reason_code     TEXT,            -- wrong_category | missing_info | overlapping_ownership | duplicate_report | other
    details         TEXT,            -- JSON
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TRIGGER IF NOT EXISTS ledger_no_update
BEFORE UPDATE ON ledger
BEGIN SELECT RAISE(ABORT, 'ledger is append-only'); END;

CREATE TRIGGER IF NOT EXISTS ledger_no_delete
BEFORE DELETE ON ledger
BEGIN SELECT RAISE(ABORT, 'ledger is append-only'); END;

CREATE TABLE IF NOT EXISTS challenges (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    complaint_id  INTEGER NOT NULL REFERENCES complaints(id),
    raised_by     TEXT NOT NULL,             -- staff | citizen
    reason        TEXT NOT NULL,
    status        TEXT NOT NULL DEFAULT 'open',   -- open | resolved
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Corrections saved as labelled examples (NO automatic retraining)
CREATE TABLE IF NOT EXISTS corrections (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    complaint_id INTEGER NOT NULL REFERENCES complaints(id),
    text         TEXT NOT NULL,
    wrong_dept   TEXT,
    correct_dept TEXT NOT NULL,
    created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);
