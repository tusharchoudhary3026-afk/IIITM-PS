import streamlit as st

st.set_page_config(page_title="NagrikSetu | Civic grievance demo", page_icon="🧭", layout="wide")

pages = [
    st.Page("pages/0_Home.py", title="Home", icon="🏠", default=True),
    st.Page("pages/1_Intake.py", title="Complain here", icon="📝"),
    st.Page("pages/2_Review.py", title="Review", icon="🔎"),
    st.Page("pages/3_Challenge.py", title="Challenge", icon="⚖️"),
    st.Page("pages/4_Evaluation.py", title="Evaluation", icon="📊"),
    st.Page("pages/5_Relabel.py", title="Relabel", icon="🏷️"),
]

st.navigation(pages, position="top").run()
