# import sqlite3
# from core.config import DB_PATH

# c = sqlite3.connect(DB_PATH)
# try:
#     c.execute("UPDATE ledger SET reason='tampered' WHERE id=(SELECT MIN(id) FROM ledger)")
#     print("NOT BLOCKED - the ledger can be edited!")
# except Exception as e:
#     print("BLOCKED:", e)
# c.rollback()


"""AT-07: can a ledger row be changed or deleted? Uses a temporary row inside a transaction
and rolls everything back, so your data is never changed."""
import sqlite3
from core.config import DB_PATH

c = sqlite3.connect(DB_PATH)
trg = c.execute("SELECT name FROM sqlite_master WHERE type='trigger' AND tbl_name='ledger'").fetchall()
print("Triggers on ledger:", [t[0] for t in trg] or "NONE")
c.execute("INSERT INTO ledger (complaint_id, event_type, actor, reason) VALUES (0, 'lock_test', 'test', 'original')")
for label, sql in [("UPDATE", "UPDATE ledger SET reason='tampered' WHERE event_type='lock_test'"),
                   ("DELETE", "DELETE FROM ledger WHERE event_type='lock_test'")]:
    try:
        n = c.execute(sql).rowcount
        print(f"{label}: NOT BLOCKED ({n} row changed) -> ledger is NOT append-only")
    except sqlite3.Error as e:
        print(f"{label}: BLOCKED ({e})")
c.rollback()
c.close()