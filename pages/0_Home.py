import streamlit as st
from core.db import init_db, fetch_all
from core.ui import apply_demo_style, render_hero

init_db()
apply_demo_style()

render_hero(
    "Civic grievance routing",
    "<strong>NagrikSetu</strong>",
    "NagrikSetu helps surface the issue, show routing suggestions, and keep possible multi-issue complaints visible for a person to review.",
)

counts = fetch_all(
    "SELECT COUNT(*) AS cases, "
    "SUM(CASE WHEN parent_id IS NOT NULL THEN 1 ELSE 0 END) AS sub_issues "
    "FROM complaints"
)[0]
languages = fetch_all("SELECT COUNT(DISTINCT language) AS n FROM complaints")[0]["n"]

st.markdown('<div class="nf-section-kicker">Prototype at a glance</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c1.metric("Saved complaints", counts["cases"] or 0)
c2.metric("Linked sub-issues", counts["sub_issues"] or 0)
c3.metric("Input languages seen", languages or 0, help="Language labels from saved demo complaints.")

st.write("")
left, right = st.columns([1.35, 1], gap="large")
with left:
    with st.container(border=True):
        st.markdown('<div class="nf-section-kicker">Guided demo</div>', unsafe_allow_html=True)
        st.subheader("Follow one complaint through the prototype")
        steps = [
            ("01", "Capture", "Preserve the original text and extract the fields the rules can identify."),
            ("02", "Inspect", "Compare keyword and TF-IDF suggestions with their supporting evidence."),
            ("03", "Consider a split", "Review proposed sub-issues and confirm only when they make sense."),
        ]
        for number, title, detail in steps:
            a, b = st.columns([0.16, 1])
            a.markdown(f"<div class='nf-score'>{number}</div>", unsafe_allow_html=True)
            b.markdown(f"**{title}**  <span class='nf-muted'>{detail}</span>", unsafe_allow_html=True)
            st.write("")
        st.page_link("pages/1_Intake.py", label="Open Complain here", icon="📝", use_container_width=True)

with right:
    with st.container(border=True):
        st.markdown('<div class="nf-section-kicker">Demo guardrails</div>', unsafe_allow_html=True)
        st.subheader("Human judgement stays central")
        st.markdown(
            """
            - Suggestions are prompts for review, not final assignments.
            - Uncertain routes remain visible for a person to assess.
            - A proposed split is not saved until someone confirms it.
            """
        )
        st.caption("Prototype data and outputs are synthetic; the ownership table contains assumptions.")

st.divider()
st.caption("NagrikSetu · Round 1 prototype · Built for explainable first-touch grievance handling")
