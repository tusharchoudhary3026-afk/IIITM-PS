# import sys, pathlib
# sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
# import streamlit as st
# from scripts.evaluate import run, summary
# from core.config import SIM_LABEL

# st.title("4. Evaluation")
# st.error(SIM_LABEL)
# st.caption("Baseline on the frozen test split. Numerator/denominator reported; small n means preliminary.")

# split = st.selectbox("Split", ["test", "val", "train"])
# if st.button("Run baseline"):
#     out = run(split)
#     st.code(summary(out))
#     st.subheader("Failures and abstentions")
#     st.dataframe(out[out.outcome != "correct"])
# # TODO: TF-IDF vs baseline table, coverage-vs-accuracy curve, language gap with confidence intervals



import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import pandas as pd
import streamlit as st
from scripts.evaluate import run, summary
from scripts.evaluate_full import evaluate, report
from core.config import SIM_LABEL
from core.ui import apply_demo_style, render_hero

apply_demo_style()
render_hero("Prototype evidence", "Evaluation", "Compare the current routing approaches and inspect their measured limits.", badge="EVALUATION")
st.error(SIM_LABEL)
st.caption("Numerator/denominator reported. Small n means preliminary. Labels are AI-written, not independent human labels.")

split = st.selectbox("Split", ["test", "val", "train"])
tab1, tab2 = st.tabs(["Baseline vs TF-IDF", "Baseline only (original)"])
with tab1:
    if st.button("Run comparison"):
        r = evaluate(split)
        st.code(report(r))
        st.subheader("Coverage vs accuracy (TF-IDF, validation split)")
        st.dataframe(pd.DataFrame(r["curve"]))
        st.line_chart(pd.DataFrame(r["curve"]).set_index("coverage")["accuracy"])
        rows = []
        for m in ("baseline", "tfidf"):
            for lang, v in r[m]["by_language"].items():
                rows.append({"method": m, "language": lang, "correct": v["correct"], "n": v["n"],
                             "abstained": v["abstained"], "95% CI": str(v["ci"])})
        st.subheader("Language-wise results")
        st.dataframe(pd.DataFrame(rows))
with tab2:
    if st.button("Run baseline"):
        out = run(split)
        st.code(summary(out))
        st.dataframe(out[out.outcome != "correct"])
