import streamlit as st
import google.generativeai as genai
import os

from dotenv import load_dotenv

from pdf_reader import extract_text
from vector_store import create_vector_store
from chatbot import get_answer


# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# LOAD ENV
# -----------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API Key Not Found")
    st.stop()

genai.configure(api_key=api_key)

llm = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# -----------------------------
# SESSION STATE
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "topics" not in st.session_state:
    st.session_state.topics = ""

# -----------------------------
# HEADER
# -----------------------------

st.title("🤖 AI Research Assistant")

st.markdown(
    """
Upload any PDF and ask questions.

The assistant answers ONLY from the uploaded document.
"""
)

# -----------------------------
# FILE UPLOADER
# -----------------------------

uploaded_file = st.file_uploader(
    "📄 Upload PDF",
    type=["pdf"]
)

# -----------------------------
# MAIN LOGIC
# -----------------------------

if uploaded_file:

    with st.spinner("Reading PDF..."):
        text = extract_text(uploaded_file)

    if not text.strip():
        st.error(
            "Could not extract text from PDF."
        )
        st.stop()

    with st.spinner(
        "Creating Vector Store..."
    ):
        index, chunks, embedding_model = (
            create_vector_store(text)
        )

    # -------------------------
    # DOCUMENT SUMMARY
    # -------------------------

    if st.session_state.summary == "":

        summary_prompt = f"""
Summarize the document
in 5 short bullet points.

{text[:5000]}
"""

        try:

            summary_response = (
                llm.generate_content(
                    summary_prompt
                )
            )

            st.session_state.summary = (
                summary_response.text
            )

        except Exception:

            st.session_state.summary = (
                "Summary unavailable."
            )

    # -------------------------
    # TOPICS EXTRACTION
    # -------------------------

    if st.session_state.topics == "":

        topics_prompt = f"""
Extract top 5 important topics
from this document.

{text[:5000]}
"""

        try:

            topics_response = (
                llm.generate_content(
                    topics_prompt
                )
            )

            st.session_state.topics = (
                topics_response.text
            )

        except Exception:

            st.session_state.topics = (
                "Topics unavailable."
            )

    # -------------------------
    # SIDEBAR
    # -------------------------

    with st.sidebar:

        st.header("📊 Document Details")

        st.metric(
            "Total Chunks",
            len(chunks)
        )

        st.divider()

        st.subheader("📄 Summary")

        st.write(
            st.session_state.summary
        )

        st.divider()

        st.subheader("🔑 Key Topics")

        st.write(
            st.session_state.topics
        )

    # -------------------------
    # CHAT HISTORY
    # -------------------------

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):
            st.write(
                message["content"]
            )

    # -------------------------
    # CHAT INPUT
    # -------------------------

    question = st.chat_input(
        "Ask anything about the document..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.write(question)

        with st.spinner(
            "Searching document..."
        ):

            result = get_answer(
                question,
                index,
                chunks,
                embedding_model,
                llm
            )

        answer = result["answer"]

        with st.chat_message(
            "assistant"
        ):

            st.write(answer)

            st.progress(
                result["confidence"] / 100
            )

            st.caption(
                f"Confidence: {result['confidence']}%"
            )

            st.info(
                result["source"]
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )