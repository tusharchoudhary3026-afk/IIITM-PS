"""Shared visual styling for the NyayaFlow Streamlit demo."""
import streamlit as st


def apply_demo_style():
    st.markdown(
        """
        <style>
        :root {
            --nf-ink: #13243a;
            --nf-muted: #62748b;
            --nf-blue: #1c5d91;
            --nf-teal: #24a89a;
            --nf-line: #dfe8f0;
            --nf-paper: #ffffff;
        }
        .stApp {
            background:
                radial-gradient(ellipse at 6% 0%, rgba(36,168,154,.09), transparent 36rem),
                linear-gradient(180deg, #f4f8fb 0%, #f7f9fc 48%, #f1f6f9 100%);
            color: var(--nf-ink);
        }
        .stApp [data-testid="stWidgetLabel"] p,
        .stApp [data-testid="stWidgetLabel"] label,
        .stApp label {
            color: #233c55 !important;
            opacity: 1 !important;
        }
        .stApp [data-testid="stMarkdownContainer"] p,
        .stApp [data-testid="stMarkdownContainer"] li {
            color: #233c55;
        }
        .stApp [data-testid="stTextAreaRootElement"] {
            background: #ffffff !important;
            border: 1px solid #cbd9e5 !important;
            border-radius: 12px !important;
        }
        .stApp [data-testid="stTextAreaRootElement"] textarea,
        .stApp [data-testid="stTextInputRootElement"] input,
        .stApp [data-testid="stSelectbox"] [role="combobox"] {
            color: #172d43 !important;
            -webkit-text-fill-color: #172d43 !important;
        }
        .stApp [data-testid="stTextAreaRootElement"] textarea {
            background: #ffffff !important;
        }
        .stApp [data-testid="stTextInputRootElement"],
        .stApp [data-testid="stSelectbox"] div:has(> [role="combobox"]) {
            background: #ffffff !important;
            border: 1px solid #cbd9e5 !important;
            border-radius: 12px !important;
        }
        .stApp [data-testid="stTextAreaRootElement"] textarea::placeholder,
        .stApp [data-testid="stTextInputRootElement"] input::placeholder {
            color: #728398 !important;
            -webkit-text-fill-color: #728398 !important;
            opacity: 1;
        }
        .stApp section[data-testid="stSidebar"] {
            background: #f8fbfd !important;
            border-right: 1px solid #dce7ef !important;
        }
        .stApp [data-testid="stSidebarNav"] {
            width: 100% !important;
            background: linear-gradient(105deg, #ffffff 0%, #f6fbfd 58%, #eff8f7 100%) !important;
            border-bottom: 1px solid #cfdee8 !important;
            box-shadow: 0 8px 24px rgba(19, 48, 72, .10) !important;
            padding: 10px 22px !important;
            animation: nf-nav-enter .28s ease-out both;
        }
        .stApp [data-testid="stSidebarNavItems"] {
            display: flex !important; align-items: center; flex-direction: row !important;
            flex-wrap: wrap; gap: 7px;
        }
        .stApp [data-testid="stSidebarNavLinkContainer"] { padding: 0 !important; }
        .stApp a[data-testid="stSidebarNavLink"] {
            display: flex !important; align-items: center; gap: 8px;
            min-height: 44px; padding: 8px 15px !important; margin: 0 3px !important;
            border: 1px solid #dce7ef !important; border-radius: 13px !important;
            background: rgba(255,255,255,.82) !important; color: #173a56 !important;
            font-weight: 700 !important; text-decoration: none !important;
            box-shadow: 0 2px 6px rgba(19,48,72,.04);
            transition: background .18s ease, transform .18s ease, box-shadow .18s ease,
                        border-color .18s ease;
        }
        .stApp a[data-testid="stSidebarNavLink"] *,
        .stApp a[data-testid="stSidebarNavLink"] [data-testid="stMarkdownContainer"] p,
        .stApp a[data-testid="stSidebarNavLink"] [label] p {
            color: #173a56 !important; -webkit-text-fill-color: #173a56 !important;
            opacity: 1 !important; font-size: .92rem; font-weight: 700;
        }
        .stApp a[data-testid="stSidebarNavLink"]:hover {
            background: #e7f4f6 !important; border-color: #afd3dd !important;
            transform: translateY(-2px); box-shadow: 0 7px 16px rgba(22, 70, 99, .12);
        }
        .stApp a[data-testid="stSidebarNavLink"][aria-current="page"] {
            background: linear-gradient(115deg, #d9f1ec, #e5f4f5) !important;
            border-color: #9bcfc8 !important; color: #075f63 !important;
            box-shadow: inset 0 -3px 0 #168b83, 0 4px 12px rgba(8,127,120,.09);
        }
        .stApp a[data-testid="stSidebarNavLink"][aria-current="page"] *,
        .stApp a[data-testid="stSidebarNavLink"][aria-current="page"] [data-testid="stMarkdownContainer"] p,
        .stApp a[data-testid="stSidebarNavLink"][aria-current="page"] [label] p {
            color: #075f63 !important; -webkit-text-fill-color: #075f63 !important;
            opacity: 1 !important;
        }
        .stApp [data-testid="stRadio"] input { accent-color: #087f78 !important; }
        .stApp [data-testid="stAlert"] {
            color: #263b50 !important;
            border-radius: 14px;
        }
        .stApp [data-testid="stAlert"] p,
        .stApp [data-testid="stAlert"] span { color: #263b50 !important; }
        .stApp [data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {
            color: #263b50 !important;
        }
        .stApp [data-testid="stFormSubmitButton"] button,
        .stApp [data-testid="baseButton-primary"] {
            background: linear-gradient(110deg, #155b83, #087f78) !important;
            border: 0 !important; color: #ffffff !important;
        }
        .stApp [data-testid="baseButton-primary"] p,
        .stApp [data-testid="baseButton-primary"] span {
            color: #ffffff !important;
        }
        .block-container { max-width: 1180px; padding-top: 2rem; padding-bottom: 3rem; }
        h1, h2, h3 { color: var(--nf-ink); letter-spacing: -.025em; }
        [data-testid="stCaptionContainer"] { color: var(--nf-muted); }
        [data-testid="stMetric"] {
            background: rgba(255,255,255,.86); border: 1px solid var(--nf-line);
            border-radius: 16px; padding: 15px 18px; box-shadow: 0 5px 18px rgba(20,48,76,.04);
        }
        [data-testid="stMetricLabel"] { color: var(--nf-muted); }
        [data-testid="stMetricValue"] { color: var(--nf-ink); }
        [data-testid="stVerticalBlockBorderWrapper"] > div {
            border-color: var(--nf-line) !important; border-radius: 18px !important;
            background: rgba(255,255,255,.82);
        }
        .stButton > button, .stPageLink > a {
            border-radius: 11px; border: 1px solid #bfd1df !important; font-weight: 650;
            background: #ffffff !important; color: #173a56 !important;
            transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
        }
        .stButton > button:hover, .stPageLink > a:hover {
            transform: translateY(-1px); border-color: #77a9c8;
            box-shadow: 0 6px 16px rgba(28,93,145,.12);
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(110deg, #155b83, #087f78) !important;
            border: 0 !important; color: #ffffff !important;
        }
        .stButton > button[kind="primary"] p,
        .stButton > button[kind="primary"] span {
            color: #ffffff !important;
        }
        .stButton > button:disabled {
            color: #718196 !important; background: #e7edf2 !important; opacity: 1 !important;
        }
        [data-testid="stTabs"] button,
        .stApp [role="tablist"] [role="tab"] {
            font-weight: 650; color: #35516a !important;
            border-radius: 11px !important;
        }
        .stApp [role="tablist"] [role="tab"][aria-selected="true"] {
            color: #075f63 !important; background: #e4f3f1 !important;
        }
        @keyframes nf-nav-enter {
            from { opacity: 0; transform: translateY(-5px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @media (prefers-reduced-motion: reduce) {
            .stApp [data-testid="stSidebarNav"],
            .stApp a[data-testid="stSidebarNavLink"] {
                animation: none !important; transition: none !important;
            }
        }
        .nf-hero {
            position: relative; overflow: hidden; border-radius: 24px; padding: 30px 34px;
            color: #f7fbff; background: linear-gradient(118deg, #112b46 0%, #1c5d81 62%, #168b8a 100%);
            box-shadow: 0 18px 40px rgba(18,54,80,.16); margin: 4px 0 22px;
        }
        .nf-hero:after {
            content: ''; position: absolute; width: 240px; height: 240px; right: -55px; top: -115px;
            border: 1px solid rgba(255,255,255,.18); border-radius: 50%;
            box-shadow: 0 0 0 28px rgba(255,255,255,.045), 0 0 0 58px rgba(255,255,255,.035);
        }
        .nf-eyebrow { color: #a6dfd9; text-transform: uppercase; letter-spacing: .16em;
            font-size: .72rem; font-weight: 750; margin-bottom: 10px; }
        .nf-hero h1 { color: white; font-size: clamp(2rem, 4vw, 3.1rem); line-height: 1.05;
            margin: 0 0 10px; }
        .nf-hero p { color: #d8e9f1; max-width: 680px; margin: 0; font-size: 1.02rem; }
        .nf-hero p, .nf-hero h1, .nf-hero h1 [data-heading-text], .nf-hero strong {
            color: #ffffff !important; -webkit-text-fill-color: #ffffff !important;
            opacity: 1 !important;
        }
        .nf-hero .nf-eyebrow { color: #b9eee7 !important; }
        .nf-hero .nf-pill { color: #f3fbff !important; }
        .nf-pill { display: inline-block; padding: 5px 10px; border-radius: 999px;
            background: rgba(255,255,255,.13); color: #e8f7f7; font-size: .75rem;
            font-weight: 700; letter-spacing: .04em; margin-bottom: 18px; }
        .nf-section-kicker { color: var(--nf-blue); text-transform: uppercase; letter-spacing: .13em;
            font-size: .72rem; font-weight: 800; margin-bottom: 6px; }
        .nf-result-title { font-weight: 750; color: var(--nf-ink); font-size: 1.08rem; }
        .nf-result-sub { color: var(--nf-muted); font-size: .84rem; margin-top: 2px; }
        .nf-score { font-size: 1.65rem; font-weight: 800; color: var(--nf-blue); line-height: 1.1; }
        .nf-muted { color: var(--nf-muted); }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(eyebrow: str, title: str, description: str, badge: str = "ROUND 1 DEMO"):
    st.markdown(
        f"""
        <section class="nf-hero">
          <div class="nf-pill">{badge}</div>
          <div class="nf-eyebrow">{eyebrow}</div>
          <h1>{title}</h1>
          <p>{description}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
