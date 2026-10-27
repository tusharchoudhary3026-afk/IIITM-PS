import json
import streamlit as st
from core.db import init_db, fetch_all
from core.ledger import history
from core import ownership
from core.config import SIM_LABEL
from core.privacy import mask_text
from core.ui import apply_demo_style, render_hero

init_db()
apply_demo_style()
render_hero("Audit", "Case replay", "One case from first suggestion to latest decision, in order.", badge="AUDIT")
st.warning(SIM_LABEL)

rows = fetch_all("SELECT id, case_id, parent_id, original_text FROM complaints ORDER BY id DESC")
if not rows:
    st.info("No complaints yet.")
    st.stop()
pick = st.selectbox("Case", rows, format_func=lambda r: f"{r['case_id']} | {mask_text(r['original_text'])[:50]}")
st.write("**Original text:**", mask_text(pick["original_text"]))

ICON = {"suggested": "🤖", "accept": "✅", "edit": "✏️", "clarify": "❓", "escalate": "⬆️",
        "challenge": "⚖️", "challenge_resolved": "🔒", "split_confirmed": "✂️", "split_merged_back": "🔗"}
h = history(pick["id"])
st.subheader("Timeline (append-only ledger)")
if not h:
    st.caption("No ledger events for this case yet.")
for e in h:
    stamp = next((str(e[k]) for k in e if any(s in k.lower() for s in ("time", "created", "_at", "ts"))), "")
    with st.container(border=True):
        st.markdown(f"{ICON.get(e['event_type'], '•')} **{e['event_type']}** · {e['actor']} · {stamp}")
        bits = []
        if e.get("suggested_dept"): bits.append(f"suggested: {e['suggested_dept']}")
        if e.get("final_dept"): bits.append(f"final: {e['final_dept']}")
        if e.get("reason_code"): bits.append(f"code: {e['reason_code']}")
        if bits: st.caption(" · ".join(bits))
        if e.get("reason"): st.write(f"Reason: {e['reason']}")
        if e.get("details"):
            try: st.caption(json.dumps(json.loads(e["details"])))
            except Exception: st.caption(str(e["details"]))

st.subheader("Pattern flags (no blame)")
b, r = ownership.detect_bounce(h), ownership.repeat_reassignment(h)
if b: st.warning(f"A → B → A pattern: {b['pattern']}")
if r: st.warning(f"Repeat reassignment: {r['moves']} owner changes ({r['path']})")
if not (b or r): st.caption("No transfer pattern detected for this case.")

ch = fetch_all("SELECT * FROM challenges WHERE complaint_id=? ORDER BY id", (pick["id"],))
if ch:
    st.subheader("Challenges")
    for c in ch:
        st.write(f"#{c['id']} · {c['raised_by']} · {c['status']}: {c['reason']}")