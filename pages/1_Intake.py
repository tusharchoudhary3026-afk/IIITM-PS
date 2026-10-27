import uuid
import streamlit as st
from core import intake, splitter, router_baseline, router_ml, ownership
from core.db import init_db, insert_complaint, insert_suggestion
from core.ledger import log_event
from core.config import SIM_LABEL
from core.ui import apply_demo_style, render_hero
from core.db import init_db, insert_complaint, insert_suggestion, fetch_all

init_db()
apply_demo_style()

render_hero(
    "01 / Capture and understand",
    "<strong>Complain here</strong>",
    "See what the system can extract, where its routing suggestions come from, and when a complaint may contain more than one issue.",
    badge="INTERACTIVE PROTOTYPE",
)

st.warning(SIM_LABEL)

phase1, phase2, phase3 = st.columns(3)
phase1.markdown("**①  Tell us what happened**")
phase2.markdown("**②  Inspect the evidence**")
phase3.markdown("**③  Review a possible split**")

examples = {
    "Compound example": "Waterlogging is building up on the road near Morar and the streetlight is not working.",
    "Clear single issue": "The streetlight is not working near City Centre.",
    "Missing details": "There is a problem but nobody has said what or where.",
}
st.markdown('<div class="nf-section-kicker">Try a synthetic example</div>', unsafe_allow_html=True)
example_cols = st.columns(len(examples))
for col, (label, sample) in zip(example_cols, examples.items()):
    if col.button(label, use_container_width=True, key=f"example_{label}"):
        st.session_state["intake_text"] = sample
        st.session_state.pop("rec", None)
        st.session_state.pop("saved", None)

with st.container(border=True):
    st.markdown('<div class="nf-section-kicker">Complaint details</div>', unsafe_allow_html=True)
    with st.form("intake_form", clear_on_submit=False):
        text = st.text_area(
            "Complaint (Hindi / English / Hinglish)",
            height=135,
            key="intake_text",
            placeholder="For example: The drain is blocked near Ward 12 and water is collecting on the road.",
        )
        c1, c2 = st.columns([1, 1.4])
        channel = c1.selectbox("Channel", ["portal", "phone", "social", "in-person"])
        loc_hint = c2.text_input("Location (optional, staff-assisted)", placeholder="e.g. Ward 12")
        submitted = st.form_submit_button("Analyze complaint", type="primary", use_container_width=True)

if submitted:
    st.session_state.pop("rec", None)
    st.session_state.pop("split", None)
    st.session_state.pop("route", None)
    st.session_state.pop("route_ml", None)
    st.session_state.pop("saved", None)
    if not text.strip():
        st.error("Enter a complaint or choose one of the synthetic examples to continue.")
    else:
        st.session_state["rec"] = intake.process(text, channel, loc_hint)
        st.session_state["split"] = splitter.propose_split(text)
        st.session_state["route"] = router_baseline.route(text)
        try:
            st.session_state["route_ml"] = router_ml.default_router().route(text)
            st.session_state.pop("route_ml_error", None)
        except Exception as exc:
            st.session_state["route_ml"] = None
            st.session_state["route_ml_error"] = str(exc)
        st.session_state.pop("saved", None)


def render_route_card(name, result, method):
    with st.container(border=True):
        col, stat = st.columns([3, 1])
        col.markdown(f'<div class="nf-result-title">{name}</div>', unsafe_allow_html=True)
        col.markdown(f'<div class="nf-result-sub">{method}</div>', unsafe_allow_html=True)
        stat.metric("Confidence", f"{result['confidence']:.0%}")
        if result["abstained"]:
            st.warning("The route is uncertain. Keep it for manual review.")
        if not result["top3"]:
            st.info("No department had a keyword match; no route is suggested.")
            return
        for rank, item in enumerate(result["top3"], 1):
            left, right = st.columns([1, 3])
            left.markdown(f"**{rank}. {item['dept']}**")
            left.progress(float(item["score"]), text=f"{item['score']:.0%}")
            if method == "Keyword evidence":
                evidence = result["evidence"].get(item["dept"], [])
                right.caption("Matched terms")
                right.write(", ".join(evidence) if evidence else "No direct keyword evidence")
            else:
                terms = result["evidence"].get("matched_terms", [])
                right.caption("Terms supporting the leading model suggestion")
                right.write(", ".join(terms) if rank == 1 and terms else "Model terms are shown for the leading suggestion.")


if "rec" in st.session_state:
    rec = st.session_state["rec"]
    sp = st.session_state["split"]
    rt = st.session_state["route"]
    rm = st.session_state.get("route_ml")
    st.divider()
    st.markdown('<div class="nf-section-kicker">Analysis workspace</div>', unsafe_allow_html=True)
    st.subheader("Complaint signal and routing")

    tab_details, tab_routes, tab_split = st.tabs(["Extracted details", "Routing evidence", "Issue split"])
    with tab_details:
        a, b, c = st.columns(3)
        a.metric("Detected language", rec["language"].title())
        b.metric("Location", rec["location"] if rec["location"] != "unknown" else "Not found")
        c.metric("Detected issue labels", len(rec["issue"].split(" | ")) if rec["issue"] != "unknown" else 0)
        with st.container(border=True):
            st.markdown("**Original complaint**")
            st.write(rec["original_text"])
        with st.container(border=True):
            st.markdown("**Extracted fields**")
            st.write({
                "Issue": rec["issue"],
                "Requested action": rec["requested_action"],
                "Channel": rec["channel"],
                "Missing fields": rec["missing_fields"] or "None detected",
            })
            with st.expander("View normalized text"):
                st.write(rec["normalized_text"])
        question = intake.clarification_question(rec)
        if question:
            st.info(f"Clarification prompt: {question}")

    with tab_routes:
        st.caption("Scores are prototype signals, not calibrated probabilities or final assignments.")
        left, right = st.columns(2, gap="medium")
        with left:
            render_route_card("Keyword baseline", rt, "Keyword evidence")
        with right:
            if rm:
                render_route_card("TF-IDF model", rm, "Model evidence")
            else:
                with st.container(border=True):
                    st.markdown('<div class="nf-result-title">TF-IDF model</div>', unsafe_allow_html=True)
                    st.info("The model could not load for this session.")
                    if st.session_state.get("route_ml_error"):
                        st.caption(st.session_state["route_ml_error"])

        overlaps = ownership.check_suggestions([x["dept"] for x in rt["top3"]], rec["original_text"])
        if overlaps:
            st.markdown("**Possible ownership overlap**")
            for overlap in overlaps:
                st.warning(
                    f"{overlap['owner']} / {overlap['overlap_owner']} · {overlap['issue_type']}\n\n"
                    f"Rule status: {overlap['verification']} · {overlap['source']}"
                )
        else:
            st.caption("No overlap rule matched both the suggested departments and the complaint wording.")

    with tab_split:
        with st.container(border=True):
            st.markdown('<div class="nf-result-title">Split assessment</div>', unsafe_allow_html=True)
            st.write(sp["note"])
            if sp["is_compound"]:
                st.caption(f"Proposed lead department: {sp['lead'] or 'No clear lead; human judgement needed'}")
                for index, part in enumerate(sp["parts"], 1):
                    with st.container(border=True):
                        st.markdown(f"**Issue {index}**")
                        st.write(part["text"])
                        suggestion = part["suggestion"]
                        if suggestion["top3"]:
                            lead = suggestion["top3"][0]
                            st.caption(
                                f"Top suggestion: {lead['dept']} · {lead['score']:.0%}"
                                + (" · uncertain" if suggestion["abstained"] else "")
                            )
                        else:
                            st.caption("No department suggestion; leave this issue for a person to assess.")
                st.info("The system only proposes. Sub-issues are saved after a human confirms the split.")
            else:
                st.caption("The complaint remains intact as one case.")

    saved = st.session_state.get("saved")
    if saved and saved.get("text") == rec["original_text"]:
        st.success(f"Saved to the review queue as {saved['case']}.")
    elif st.button("Save complaint to review queue", type="primary", use_container_width=True):
        case = f"CASE-{uuid.uuid4().hex[:6].upper()}"
        rec["case_id"] = case
        cid = insert_complaint(rec)
        insert_suggestion(cid, "baseline", rt["top3"], rt["evidence"], rt["confidence"], rt["abstained"])
        if rm:
            insert_suggestion(cid, "tfidf", rm["top3"], rm["evidence"], rm["confidence"], rm["abstained"])
        top = rt["top3"][0]["dept"] if rt["top3"] and not rt["abstained"] else None
        log_event(cid, "suggested", "system", suggested_dept=top,
                  details={"abstained": rt["abstained"], "confidence": rt["confidence"]})
        st.session_state["saved"] = {"cid": cid, "case": case, "text": rec["original_text"]}
        st.success(f"Saved to the review queue as {case}.")

    saved = st.session_state.get("saved")
    if saved and saved.get("text") == rec["original_text"] and sp["is_compound"]:
        st.write("")
        with st.container(border=True):
            st.markdown("**Human decision on the split**")
            c1, c2 = st.columns(2)
            if c1.button("Confirm proposed split", use_container_width=True):
                try:
                    ids = splitter.confirm_split(saved["cid"], saved["case"], sp["parts"])
                    st.success(f"{len(ids)} linked sub-issues saved under {saved['case']}.")
                except ValueError as exc:
                    st.error(str(exc))
            if c2.button("Keep as one complaint", use_container_width=True):
                try:
                    if not fetch_all("SELECT 1 FROM complaints WHERE parent_id=? LIMIT 1", (saved["cid"],)):
                        st.info("Kept as one complaint. No split was saved, so nothing changed.")
                    else:
                        st.info(f"Merged back. {splitter.merge_back(saved['cid'])} linked sub-issues affected.")
                except ValueError as exc:
                    st.error(str(exc))
            