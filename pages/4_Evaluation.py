import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import streamlit as st
from scripts.evaluate import run, summary
from core.config import SIM_LABEL

st.title("4. Evaluation")
st.error(SIM_LABEL)
st.caption("Baseline on the frozen test split. Numerator/denominator reported; small n means preliminary.")

split = st.selectbox("Split", ["test", "val", "train"])
if st.button("Run baseline"):
    out = run(split)
    st.code(summary(out))
    st.subheader("Failures and abstentions")
    st.dataframe(out[out.outcome != "correct"])
# TODO: TF-IDF vs baseline table, coverage-vs-accuracy curve, language gap with confidence intervals
