import streamlit as st
from core.db import init_db, fetch_all, execute
from core.ledger import log_event
from core.config import SIM_LABEL
from core.ui import apply_demo_style, render_hero

init_db()
apply_demo_style()
render_hero("Case feedback", "Challenge a route", "Flag a routing concern and provide context for the reviewer.", badge="CHALLENGE")
st.warning(SIM_LABEL)

rows = fetch_all("SELECT id, case_id, original_text FROM complaints ORDER BY id DESC")
if not rows:
    st.info("No complaints yet.")
    st.stop()

st.subheader("Raise a challenge")
pick = st.selectbox("Case", rows, format_func=lambda r: f"{r['case_id']} | {r['original_text'][:50]}")
who = st.radio("Raised by", ["staff", "citizen"], horizontal=True)
why = st.text_area("Why is this routing wrong?")
if st.button("Submit challenge"):
    if not why.strip():
        st.error("Add a short reason before submitting the challenge.")
    else:
        execute("INSERT INTO challenges (complaint_id, raised_by, reason) VALUES (?,?,?)",
                (pick["id"], who, why.strip()))
        log_event(pick["id"], "challenge", who, reason=why.strip())
        st.success("Sent to the review queue.")

st.subheader("Open challenges")
for ch in fetch_all("SELECT * FROM challenges WHERE status='open'"):
    st.write(f"#{ch['id']} (case {ch['complaint_id']}, by {ch['raised_by']}): {ch['reason']}")
    note = st.text_input("Resolution note", key=f"n{ch['id']}")
    if st.button("Resolve", key=f"r{ch['id']}"):
        if not note.strip():
            st.error("Add a resolution note before closing this challenge.")
        else:
            execute("UPDATE challenges SET status='resolved' WHERE id=?", (ch["id"],))
            log_event(ch["complaint_id"], "challenge_resolved", "reviewer", reason=note.strip())
            st.rerun()
