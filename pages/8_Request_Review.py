import json
import streamlit as st
from core.db import init_db, fetch_all, execute
from core.ledger import log_event
from core.config import SIM_LABEL
from core.ui import apply_demo_style, render_hero

init_db()
apply_demo_style()
render_hero("For residents", "Request a review", "Ask a person to look again at how your complaint was routed.", badge="CITIZEN")
st.warning(SIM_LABEL)

case_id = st.text_input("Your case ID (for example CASE-1A2B3C)").strip().upper()
why = st.text_area("What looks wrong or missing?")
if case_id:
    found = fetch_all("SELECT id, case_id FROM complaints WHERE case_id=?", (case_id,))
    if not found:
        st.error("No case with that ID.")
    else:
        cid = found[0]["id"]
        sug = fetch_all("SELECT * FROM suggestions WHERE complaint_id=? ORDER BY id LIMIT 1", (cid,))
        with st.container(border=True):
            st.markdown("**Why this department?** (facts from the record, not a final decision)")
            if sug and not sug[0]["abstained"]:
                top = json.loads(sug[0]["top3"])[0]["dept"]
                terms = json.loads(sug[0]["evidence"]).get(top, [])
                st.write(f"The system suggested **{top}**" + (f" because the complaint contains: {', '.join(terms)}." if terms else "."))
            else:
                st.write("The system was not sure, so this case waits for a person to decide.")
            st.caption("A staff member makes the final decision.")
        if st.button("Send review request", type="primary"):
            if not why.strip():
                st.error("Add a short reason first.")
            else:
                execute("INSERT INTO challenges (complaint_id, raised_by, reason) VALUES (?,?,?)",
                        (cid, "citizen", why.strip()))
                log_event(cid, "challenge", "citizen", reason=why.strip())
                st.success("Sent to the review queue.")