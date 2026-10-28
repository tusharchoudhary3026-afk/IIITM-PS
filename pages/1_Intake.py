# import uuid
# import streamlit as st
# from core import intake, splitter, router_baseline, ownership
# from core.db import init_db, insert_complaint, insert_suggestion
# from core.ledger import log_event
# from core.config import SIM_LABEL

# init_db()
# st.title("1. Intake")
# st.warning(SIM_LABEL)

# text = st.text_area("Complaint (Hindi / English / Hinglish)", height=120)
# channel = st.selectbox("Channel", ["portal", "phone", "social", "in-person"])
# loc_hint = st.text_input("Location (optional, staff-assisted)")

# if st.button("Process") and text.strip():
#     rec = intake.process(text, channel, loc_hint)
#     st.session_state["rec"] = rec
#     st.session_state["split"] = splitter.propose_split(text)
#     st.session_state["route"] = router_baseline.route(text)

# if "rec" in st.session_state:
#     rec, sp, rt = st.session_state["rec"], st.session_state["split"], st.session_state["route"]
#     st.subheader("Extracted")
#     st.json({k: v for k, v in rec.items() if k != "original_text"})
#     q = intake.clarification_question(rec)
#     if q:
#         st.info(f"Clarification question: {q}")

#     st.subheader("Suggestion (baseline)")
#     if rt["abstained"]:
#         st.error("Not sure -> manual review queue")
#     for t in rt["top3"]:
#         st.write(f"- {t['dept']} ({t['score']})  evidence: {rt['evidence'].get(t['dept'])}")
#         for o in ownership.check(t["dept"]):
#             st.warning(f"Possible overlap with {o['overlap_owner']} ({o['issue_type']}). "
#                        f"Source: {o['source']} [{o['verification']}]")

#     st.subheader("Split proposal")
#     st.write(sp["note"])
#     if sp["is_compound"]:
#         for p in sp["parts"]:
#             st.write(f"- {p['text']} -> {[x['dept'] for x in p['suggestion']['top3'][:1]]}")

#     if st.button("Save to review queue"):
#         rec["case_id"] = f"CASE-{uuid.uuid4().hex[:6].upper()}"
#         cid = insert_complaint(rec)
#         insert_suggestion(cid, "baseline", rt["top3"], rt["evidence"], rt["confidence"], rt["abstained"])
#         top = rt["top3"][0]["dept"] if rt["top3"] else None
#         log_event(cid, "suggested", "system", suggested_dept=top,
#                   details={"abstained": rt["abstained"], "confidence": rt["confidence"]})
#         st.success(f"Saved as {rec['case_id']}")
#         # TODO: if sp["is_compound"] and a human confirms, insert sub-issues with parent_id=cid and the same case_id


import uuid
import streamlit as st
from core import intake, splitter, router_baseline, ownership
from core.db import init_db, insert_complaint, insert_suggestion
from core.ledger import log_event
from core.config import SIM_LABEL

init_db()
st.title("1. Intake")
st.warning(SIM_LABEL)

text = st.text_area("Complaint (Hindi / English / Hinglish)", height=120)
channel = st.selectbox("Channel", ["portal", "phone", "social", "in-person"])
loc_hint = st.text_input("Location (optional, staff-assisted)")

if st.button("Process") and text.strip():
    # Processing happens in the background (backend)
    rec = intake.process(text, channel, loc_hint)
    st.session_state["rec"] = rec
    st.session_state["split"] = splitter.propose_split(text)
    st.session_state["route"] = router_baseline.route(text)

if "rec" in st.session_state:
    rec, sp, rt = st.session_state["rec"], st.session_state["split"], st.session_state["route"]
    
    # Raw JSON extraction is now completely hidden from the UI (handled in backend)
    
    q = intake.clarification_question(rec)
    if q:
        st.info(f"Clarification question: {q}")

    st.subheader("Suggestion (baseline)")
    if rt["abstained"]:
        st.error("Not sure -> manual review queue")
    for t in rt["top3"]:
        st.write(f"- {t['dept']} ({t['score']})  evidence: {rt['evidence'].get(t['dept'])}")
        for o in ownership.check(t["dept"]):
            st.warning(f"Possible overlap with {o['overlap_owner']} ({o['issue_type']}). "
                       f"Source: {o['source']} [{o['verification']}]")

    st.subheader("Split proposal")
    st.write(sp["note"])
    if sp["is_compound"]:
        for p in sp["parts"]:
            st.write(f"- {p['text']} -> {[x['dept'] for x in p['suggestion']['top3'][:1]]}")

    if st.button("Save to review queue"):
        rec["case_id"] = f"CASE-{uuid.uuid4().hex[:6].upper()}"
        cid = insert_complaint(rec)
        insert_suggestion(cid, "baseline", rt["top3"], rt["evidence"], rt["confidence"], rt["abstained"])
        top = rt["top3"][0]["dept"] if rt["top3"] else None
        log_event(cid, "suggested", "system", suggested_dept=top,
                  details={"abstained": rt["abstained"], "confidence": rt["confidence"]})
        st.success(f"Saved as {rec['case_id']}")