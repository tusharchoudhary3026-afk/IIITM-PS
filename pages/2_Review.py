# import json
# import streamlit as st
# from core.db import init_db, fetch_all
# from core.ledger import log_event, history, save_correction
# from core.config import REASON_CODES, REVIEW_ACTIONS, SIM_LABEL
# from core import ownership

# init_db()
# st.title("2. Human Review")
# st.warning(SIM_LABEL)

# rows = fetch_all("SELECT id, case_id, language, original_text FROM complaints ORDER BY id DESC")
# if not rows:
#     st.info("No complaints yet. Use Intake first.")
#     st.stop()

# pick = st.selectbox("Complaint", rows,
#                     format_func=lambda r: f"{r['case_id']} | {r['language']} | {r['original_text'][:50]}")
# st.write("**Original text:**", pick["original_text"])

# sug = fetch_all("SELECT * FROM suggestions WHERE complaint_id=? ORDER BY id DESC LIMIT 1", (pick["id"],))
# suggested = None
# if sug:
#     top3 = json.loads(sug[0]["top3"])
#     suggested = top3[0]["dept"] if top3 else None
#     st.write("**Suggestion:**", top3, "| confidence:", sug[0]["confidence"],
#              "| abstained:", bool(sug[0]["abstained"]))

# action = st.radio("Action", REVIEW_ACTIONS, horizontal=True)
# final = st.text_input("Final department", value=suggested or "")
# reason = st.text_area("Reason (mandatory for edit / escalate)")
# code = st.selectbox("Transfer-reason code", REASON_CODES)

# if st.button("Submit decision"):
#     try:
#         log_event(pick["id"], action, "reviewer", suggested_dept=suggested, final_dept=final or None,
#                   reason=reason, reason_code=code if action in ("edit", "escalate") else None)
#         if action == "edit" and suggested and final != suggested:
#             save_correction(pick["id"], pick["original_text"], suggested, final)  # labelled example only
#         st.success("Logged. Previous entries are untouched.")
#     except ValueError as e:
#         st.error(str(e))

# st.subheader("Ledger (append-only)")
# h = history(pick["id"])
# st.dataframe(h)
# b = ownership.detect_bounce(h)
# if b:
#     st.warning(f"Transfer pattern flagged (no blame): {b['pattern']}")










import json
import streamlit as st
from core.db import init_db, fetch_all
from core.ledger import log_event, history, save_correction
from core.config import REASON_CODES, REVIEW_ACTIONS, SIM_LABEL
from core import ownership
from core.ui import apply_demo_style, render_hero

init_db()
apply_demo_style()
render_hero("Case handling", "Review complaint", "Inspect the original complaint and suggestions, then record the reviewer decision.", badge="REVIEW")
st.warning(SIM_LABEL)

rows = fetch_all("SELECT id, case_id, parent_id, language, original_text FROM complaints ORDER BY id DESC")
if not rows:
    st.info("No complaints yet. Use Intake first.")
    st.stop()

pick = st.selectbox("Complaint", rows,
                    format_func=lambda r: f"{r['case_id']} | {r['language']} | {r['original_text'][:50]}")
st.write("**Original text:**", pick["original_text"])

# --- Split view (Engine 2): parent and sub-issues ---
if pick.get("parent_id"):
    parent = fetch_all("SELECT case_id, original_text FROM complaints WHERE id=?", (pick["parent_id"],))
    if parent:
        st.info(f"This is a sub-issue of {parent[0]['case_id']}: {parent[0]['original_text'][:80]}")
kids = fetch_all("SELECT id, case_id, original_text FROM complaints WHERE parent_id=? ORDER BY id", (pick["id"],))
h = history(pick["id"])
if kids:
    merged = any(e["event_type"] == "split_merged_back" for e in h)
    st.subheader("Sub-issues (split by a human)")
    if merged:
        st.caption("A reviewer merged this split back. The sub-issues stay in the record; treat the parent as one complaint.")
    for k in kids:
        st.write(f"- {k['case_id']}: {k['original_text']}")

# --- Suggestions: baseline first (matches the ledger), others shown for comparison ---
sugs = fetch_all("SELECT * FROM suggestions WHERE complaint_id=? ORDER BY id", (pick["id"],))
suggested = None
for i, s in enumerate(sugs):
    top3 = json.loads(s["top3"])
    if i == 0:
        suggested = top3[0]["dept"] if top3 and not s["abstained"] else None
    st.write(f"**Suggestion ({s['method']}):**", top3, "| confidence:", s["confidence"],
             "| abstained:", bool(s["abstained"]))

action = st.radio("Action", REVIEW_ACTIONS, horizontal=True)
final = st.text_input("Final department", value=suggested or "")
reason = st.text_area("Reason (mandatory for edit / escalate)")
code = st.selectbox("Transfer-reason code (mandatory for edit / escalate)", REASON_CODES)

if st.button("Submit decision"):
    try:
        log_event(pick["id"], action, "reviewer", suggested_dept=suggested, final_dept=final or None,
                  reason=reason, reason_code=code if action in ("edit", "escalate") else None)
        if action == "edit" and suggested and final != suggested:
            save_correction(pick["id"], pick["original_text"], suggested, final)  # labelled example only
        st.success("Logged. Previous entries are untouched.")
    except ValueError as e:
        st.error(str(e))

st.subheader("Ledger (append-only)")
h = history(pick["id"])
st.dataframe(h)
b = ownership.detect_bounce(h)
if b:
    st.warning(f"Transfer pattern flagged (no blame): {b['pattern']}")
r = ownership.repeat_reassignment(h)
if r:
    st.warning(f"Repeat reassignment flagged (no blame): {r['moves']} owner changes: {r['path']}")
