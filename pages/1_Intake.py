# # import uuid
# # import streamlit as st
# # from core import intake, splitter, router_baseline, ownership
# # from core.db import init_db, insert_complaint, insert_suggestion
# # from core.ledger import log_event
# # from core.config import SIM_LABEL

# # init_db()
# # st.title("1. Intake")
# # st.warning(SIM_LABEL)

# # text = st.text_area("Complaint (Hindi / English / Hinglish)", height=120)
# # channel = st.selectbox("Channel", ["portal", "phone", "social", "in-person"])
# # loc_hint = st.text_input("Location (optional, staff-assisted)")

# # if st.button("Process") and text.strip():
# #     rec = intake.process(text, channel, loc_hint)
# #     st.session_state["rec"] = rec
# #     st.session_state["split"] = splitter.propose_split(text)
# #     st.session_state["route"] = router_baseline.route(text)

# # if "rec" in st.session_state:
# #     rec, sp, rt = st.session_state["rec"], st.session_state["split"], st.session_state["route"]
# #     st.subheader("Extracted")
# #     st.json({k: v for k, v in rec.items() if k != "original_text"})
# #     q = intake.clarification_question(rec)
# #     if q:
# #         st.info(f"Clarification question: {q}")

# #     st.subheader("Suggestion (baseline)")
# #     if rt["abstained"]:
# #         st.error("Not sure -> manual review queue")
# #     for t in rt["top3"]:
# #         st.write(f"- {t['dept']} ({t['score']})  evidence: {rt['evidence'].get(t['dept'])}")
# #         for o in ownership.check(t["dept"]):
# #             st.warning(f"Possible overlap with {o['overlap_owner']} ({o['issue_type']}). "
# #                        f"Source: {o['source']} [{o['verification']}]")

# #     st.subheader("Split proposal")
# #     st.write(sp["note"])
# #     if sp["is_compound"]:
# #         for p in sp["parts"]:
# #             st.write(f"- {p['text']} -> {[x['dept'] for x in p['suggestion']['top3'][:1]]}")

# #     if st.button("Save to review queue"):
# #         rec["case_id"] = f"CASE-{uuid.uuid4().hex[:6].upper()}"
# #         cid = insert_complaint(rec)
# #         insert_suggestion(cid, "baseline", rt["top3"], rt["evidence"], rt["confidence"], rt["abstained"])
# #         top = rt["top3"][0]["dept"] if rt["top3"] else None
# #         log_event(cid, "suggested", "system", suggested_dept=top,
# #                   details={"abstained": rt["abstained"], "confidence": rt["confidence"]})
# #         st.success(f"Saved as {rec['case_id']}")
# #         # TODO: if sp["is_compound"] and a human confirms, insert sub-issues with parent_id=cid and the same case_id





# import uuid
# import streamlit as st
# from core import intake, splitter, router_baseline, router_ml, ownership
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
#     st.session_state["rec"] = intake.process(text, channel, loc_hint)
#     st.session_state["split"] = splitter.propose_split(text)
#     st.session_state["route"] = router_baseline.route(text)
#     try:
#         st.session_state["route_ml"] = router_ml.default_router().route(text)
#     except Exception:
#         st.session_state["route_ml"] = None
#     st.session_state.pop("saved", None)

# if "rec" in st.session_state:
#     rec, sp = st.session_state["rec"], st.session_state["split"]
#     rt, rm = st.session_state["route"], st.session_state.get("route_ml")
#     st.subheader("Extracted")
#     st.json({k: v for k, v in rec.items() if k != "original_text"})
#     q = intake.clarification_question(rec)
#     if q:
#         st.info(f"Clarification question: {q}")

#     for name, r in [("Baseline (keywords)", rt), ("TF-IDF model", rm)]:
#         if r is None:
#             continue
#         st.subheader(f"Suggestion: {name}")
#         if r["abstained"]:
#             st.error("Not sure -> manual review queue")
#         for t in r["top3"]:
#             st.write(f"- {t['dept']} ({t['score']})  evidence: {r['evidence'].get(t['dept'], r['evidence'])}")
#         if r["top3"]:
#            for o in ownership.check_suggestions([x["dept"] for x in r["top3"]]):
#                 st.warning(f"Possible overlap with {o['overlap_owner']} ({o['issue_type']}). "
#                            f"Source: {o['source']} [{o['verification']}]")

#     st.subheader("Split proposal")
#     st.write(sp["note"])
#     if sp["is_compound"]:
#         for p in sp["parts"]:
#             st.write(f"- {p['text']} -> {[x['dept'] for x in p['suggestion']['top3'][:1]]}")
#         st.caption(f"Proposed lead department: {sp['lead'] or 'none (tie) - human decides'}")

#     if st.button("Save to review queue"):
#         case = f"CASE-{uuid.uuid4().hex[:6].upper()}"
#         rec["case_id"] = case
#         cid = insert_complaint(rec)
#         insert_suggestion(cid, "baseline", rt["top3"], rt["evidence"], rt["confidence"], rt["abstained"])
#         if rm:
#             insert_suggestion(cid, "tfidf", rm["top3"], rm["evidence"], rm["confidence"], rm["abstained"])
#         top = rt["top3"][0]["dept"] if rt["top3"] else None
#         log_event(cid, "suggested", "system", suggested_dept=top,
#                   details={"abstained": rt["abstained"], "confidence": rt["confidence"]})
#         st.session_state["saved"] = {"cid": cid, "case": case}
#         st.success(f"Saved as {case}")

#     saved = st.session_state.get("saved")
#     if saved and sp["is_compound"]:
#         st.subheader("Human decision on the split (nothing is applied automatically)")
#         c1, c2 = st.columns(2)
#         if c1.button("Confirm split into sub-issues"):
#             ids = splitter.confirm_split(saved["cid"], saved["case"], sp["parts"])
#             st.success(f"{len(ids)} sub-issues saved under {saved['case']}")
#         if c2.button("Keep as one complaint (merge back)"):
#             n = splitter.merge_back(saved["cid"])
#             st.info(f"Merge-back logged ({n} sub-issues affected).")




import uuid
import streamlit as st
from core import intake, splitter, router_baseline, router_ml, ownership
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
    st.session_state["rec"] = intake.process(text, channel, loc_hint)
    st.session_state["split"] = splitter.propose_split(text)
    st.session_state["route"] = router_baseline.route(text)
    try:
        st.session_state["route_ml"] = router_ml.default_router().route(text)
    except Exception:
        st.session_state["route_ml"] = None
    st.session_state.pop("saved", None)

if "rec" in st.session_state:
    rec, sp = st.session_state["rec"], st.session_state["split"]
    rt, rm = st.session_state["route"], st.session_state.get("route_ml")
    st.subheader("Extracted")
    st.json({k: v for k, v in rec.items() if k != "original_text"})
    q = intake.clarification_question(rec)
    if q:
        st.info(f"Clarification question: {q}")

    for name, r in [("Baseline (keywords)", rt), ("TF-IDF model", rm)]:
        if r is None:
            continue
        st.subheader(f"Suggestion: {name}")
        if r["abstained"]:
            st.error("Not sure -> manual review queue")
        for i, t in enumerate(r["top3"]):
            ev = r["evidence"].get(t["dept"], r["evidence"] if i == 0 else "")
            st.write(f"- {t['dept']} ({t['score']})  evidence: {ev}")

    # Ownership overlap: from the keyword baseline only (its top-3 holds departments with evidence).
    for o in ownership.check_suggestions([x["dept"] for x in rt["top3"]]):
        st.warning(f"Possible overlap: {o['owner']} / {o['overlap_owner']} ({o['issue_type']}). "
                   f"Source: {o['source']} [{o['verification']}]")

    st.subheader("Split proposal")
    st.write(sp["note"])
    if sp["is_compound"]:
        for p in sp["parts"]:
            st.write(f"- {p['text']} -> {[x['dept'] for x in p['suggestion']['top3'][:1]]}")
        st.caption(f"Proposed lead department: {sp['lead'] or 'none (tie) - human decides'}")

    if st.button("Save to review queue"):
        case = f"CASE-{uuid.uuid4().hex[:6].upper()}"
        rec["case_id"] = case
        cid = insert_complaint(rec)
        insert_suggestion(cid, "baseline", rt["top3"], rt["evidence"], rt["confidence"], rt["abstained"])
        if rm:
            insert_suggestion(cid, "tfidf", rm["top3"], rm["evidence"], rm["confidence"], rm["abstained"])
        top = rt["top3"][0]["dept"] if rt["top3"] and not rt["abstained"] else None
        log_event(cid, "suggested", "system", suggested_dept=top,
                  details={"abstained": rt["abstained"], "confidence": rt["confidence"]})
        st.session_state["saved"] = {"cid": cid, "case": case}
        st.success(f"Saved as {case}")

    saved = st.session_state.get("saved")
    if saved and sp["is_compound"]:
        st.subheader("Human decision on the split (nothing is applied automatically)")
        c1, c2 = st.columns(2)
        if c1.button("Confirm split into sub-issues"):
            ids = splitter.confirm_split(saved["cid"], saved["case"], sp["parts"])
            st.success(f"{len(ids)} sub-issues saved under {saved['case']}")
        if c2.button("Keep as one complaint (merge back)"):
            n = splitter.merge_back(saved["cid"])
            st.info(f"Merge-back logged ({n} sub-issues affected).")