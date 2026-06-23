import streamlit as st

# =====================================
# THEME SETTINGS
# =====================================

APP_BG = "#030712"      # <-- ફક્ત આ બદલીશ તો આખું theme બદલાશે

CARD_BG = "#111827"
SIDEBAR_BG = "#0f172a"

PRIMARY = "#2563eb"
SECONDARY = "#7c3aed"

TEXT = "#ffffff"
MUTED = "#94a3b8"

BORDER = "#334155"


# =====================================
# LOAD UI
# =====================================

def load_ui():

    st.set_page_config(
        page_title="AI Research Assistant",
        page_icon="🤖",
        layout="wide"
    )

    st.markdown(
        f"""
<style>

/* ---------------------------
IMPORT FONT
---------------------------- */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

/* ---------------------------
FULL APP BACKGROUND
---------------------------- */

.stApp {{

    background:
    radial-gradient(circle at top left,
    rgba(37,99,235,0.15),
    transparent 35%),

    radial-gradient(circle at top right,
    rgba(124,58,237,0.15),
    transparent 35%),

    {APP_BG};

    color:{TEXT};
}}

/* ---------------------------
MAIN AREA
---------------------------- */

[data-testid="stAppViewContainer"],
[data-testid="stMain"] {{
    background: transparent !important;
}}

.block-container {{
    padding-top: 1rem;
    max-width: 1400px;
}}

/* ---------------------------
HEADER REMOVE
---------------------------- */

[data-testid="stHeader"] {{
    background: transparent !important;
}}

[data-testid="stToolbar"] {{
    background: transparent !important;
}}

/* ---------------------------
SIDEBAR
---------------------------- */

[data-testid="stSidebar"] {{

    background:
    linear-gradient(
    180deg,
    {SIDEBAR_BG},
    #020617);

    border-right:
    1px solid {BORDER};
}}

/* ---------------------------
TEXT
---------------------------- */

h1,h2,h3,h4,h5,h6,p,label,span {{
    color:{TEXT} !important;
}}

/* ---------------------------
TITLE
---------------------------- */

.main-title {{

    text-align:center;

    font-size:52px;

    font-weight:800;

    color:white;

    margin-bottom:10px;
}}

.sub-title {{

    text-align:center;

    color:{MUTED};

    font-size:18px;

    margin-bottom:40px;
}}

/* ---------------------------
UPLOAD BOX
---------------------------- */

[data-testid="stFileUploader"] {{

    background:{CARD_BG};

    border:1px solid {BORDER};

    border-radius:18px;

    padding:20px;
}}

/* ---------------------------
TEXT AREA
---------------------------- */

textarea {{

    background:{CARD_BG} !important;

    color:white !important;

    border-radius:14px !important;

    border:1px solid {BORDER} !important;
}}

/* ---------------------------
BUTTON
---------------------------- */

.stButton > button {{

    width:100%;

    height:52px;

    border:none;

    border-radius:14px;

    color:white;

    font-weight:700;

    background:
    linear-gradient(
    135deg,
    {PRIMARY},
    {SECONDARY}
    );

    transition:0.3s;
}}

.stButton > button:hover {{

    transform:translateY(-2px);

    box-shadow:
    0 0 30px rgba(124,58,237,.5);
}}

/* ---------------------------
CHAT MESSAGE
---------------------------- */

[data-testid="stChatMessage"] {{

    background:{CARD_BG};

    border:1px solid {BORDER};

    border-radius:18px;

    padding:10px;
}}

/* ---------------------------
SUCCESS / INFO / WARNING
---------------------------- */

.stSuccess,
.stInfo,
.stWarning,
.stError {{

    border-radius:15px !important;
}}

/* ---------------------------
METRIC CARDS
---------------------------- */

[data-testid="metric-container"] {{

    background:{CARD_BG};

    border:1px solid {BORDER};

    border-radius:18px;

    padding:15px;
}}

/* ---------------------------
CODE BLOCK
---------------------------- */

pre {{

    border-radius:15px !important;

    border:1px solid {BORDER};

    background:#020617 !important;
}}

/* ---------------------------
SCROLLBAR
---------------------------- */

::-webkit-scrollbar {{
    width:10px;
}}

::-webkit-scrollbar-thumb {{
    background:{PRIMARY};
    border-radius:10px;
}}

</style>
        """,
        unsafe_allow_html=True
    )


# =====================================
# HEADER
# =====================================

def show_header():

    st.markdown(
        """
        <div class="main-title">
        🤖 AI Research Assistant
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sub-title">
        Context-Aware PDF Question Answering using RAG + FAISS + Gemini 2.5 Flash
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================
# SIDEBAR
# =====================================

def sidebar():

    with st.sidebar:

        st.markdown("## 🤖 AI Assistant")

        st.success("✅ PDF Analysis")
        st.success("✅ FAISS Retrieval")
        st.success("✅ Gemini 2.5 Flash")
        st.success("✅ Hallucination Guard")
        st.success("✅ Topic Extraction")
        st.success("✅ Summary Generator")

        st.divider()

        st.info("🚀 Version 1.0")

        st.caption(
            "Professional RAG Document Assistant"
        )