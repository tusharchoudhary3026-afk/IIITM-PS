import streamlit as st
from core.db import init_db, fetch_all
from core.config import SIM_LABEL

st.set_page_config(page_title="NyayaFlow", layout="wide")
init_db()

st.title("NyayaFlow")
st.caption("Explainable grievance routing and accountability assistant")
st.warning(SIM_LABEL)

n = fetch_all("SELECT COUNT(*) AS n FROM complaints")[0]["n"]
open_ch = fetch_all("SELECT COUNT(*) AS n FROM challenges WHERE status='open'")[0]["n"]
c1, c2 = st.columns(2)
c1.metric("Complaints (synthetic)", n)
c2.metric("Open challenges", open_ch)

st.markdown("""
**Pages (left sidebar)**
1. **Intake** - enter a complaint, extract fields, propose a split, get suggestions
2. **Review** - accept / edit / clarify / escalate, with the append-only ledger
3. **Challenge** - staff challenge and citizen request-review
4. **Evaluation** - baseline results with sample sizes

**Ground rules:** nothing is auto-closed, auto-rejected or auto-merged. A human decides.
""")
