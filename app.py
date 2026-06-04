import streamlit as st
import google.generativeai as genai
import os

from dotenv import load_dotenv

from pdf_reader import (
    extract_text,
    get_pdf_info
)

from vector_store import (
    create_vector_store,
    get_vector_stats
)

from chatbot import get_answer


# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------------
# LOAD ENVIRONMENT
# -----------------------------------

load_dotenv()

api_key = os.getenv(
    "GEMINI_API_KEY"
)

if not api_key:

    st.error(
        "Gemini API Key Not Found"
    )

    st.stop()

genai.configure(
    api_key=api_key
)

llm = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# -----------------------------------
# SESSION STATE
# -----------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []

if "summary" not in st.session_state:

    st.session_state.summary = ""

if "topics" not in st.session_state:

    st.session_state.topics = ""

if "index" not in st.session_state:

    st.session_state.index = None

if "chunks" not in st.session_state:

    st.session_state.chunks = None

if "embedding_model" not in st.session_state:

    st.session_state.embedding_model = None

# -----------------------------------
# HEADER
# -----------------------------------

st.title(
    "🤖 AI Research Assistant"
)

st.markdown(
    """
Upload a PDF document and ask questions.

The assistant answers ONLY from
the uploaded document.
"""
)

# -----------------------------------
# PDF UPLOAD
# -----------------------------------

uploaded_file = st.file_uploader(
    "📄 Upload PDF",
    type=["pdf"]
)

# -----------------------------------
# PROCESS PDF
# -----------------------------------

if uploaded_file:

    pdf_info = get_pdf_info(
        uploaded_file
    )

    with st.spinner(
        "Reading PDF..."
    ):

        text = extract_text(
            uploaded_file
        )

    if not text.strip():

        st.error(
            "Could not extract text."
        )

        st.stop()

    # -------------------------------
    # CREATE VECTOR STORE ONLY ONCE
    # -------------------------------

    if (
        st.session_state.index
        is None
    ):

        with st.spinner(
            "Creating Vector Store..."
        ):

            (
                index,
                chunks,
                embedding_model
            ) = create_vector_store(
                text
            )

            st.session_state.index = (
                index
            )

            st.session_state.chunks = (
                chunks
            )

            st.session_state.embedding_model = (
                embedding_model
            )

    # -------------------------------
    # SUMMARY
    # -------------------------------

    if (
        st.session_state.summary
        == ""
    ):

        try:

            response = (
                llm.generate_content(
                    f"""
Summarize this document
in 5 short bullet points.

{text[:5000]}
"""
                )
            )

            st.session_state.summary = (
                response.text
            )

        except Exception:

            st.session_state.summary = (
                "Summary unavailable."
            )

    # -------------------------------
    # TOPICS
    # -------------------------------

    if (
        st.session_state.topics
        == ""
    ):

        try:

            response = (
                llm.generate_content(
                    f"""
Extract top 5 important topics
from this document.

{text[:5000]}
"""
                )
            )

            st.session_state.topics = (
                response.text
            )

        except Exception:

            st.session_state.topics = (
                "Topics unavailable."
            )

    # -------------------------------
    # SIDEBAR
    # -------------------------------

    with st.sidebar:

        st.header(
            "📊 Document Details"
        )

        st.write(
            f"📄 File: {pdf_info['filename']}"
        )

        st.write(
            f"📑 Pages: {pdf_info['total_pages']}"
        )

        st.write(
            f"💾 Size: {pdf_info['size_kb']} KB"
        )

        stats = get_vector_stats(
            st.session_state.index,
            st.session_state.chunks
        )

        st.metric(
            "Chunks",
            stats["total_chunks"]
        )

        st.metric(
            "Vector Dimension",
            stats["vector_dimension"]
        )

        st.divider()

        st.subheader(
            "📄 Summary"
        )

        st.write(
            st.session_state.summary
        )

        st.divider()

        st.subheader(
            "🔑 Key Topics"
        )

        st.write(
            st.session_state.topics
        )

        st.divider()



            # -----------------------------------
    # CLEAR CHAT BUTTON
    # -----------------------------------

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🗑 Clear Chat"
        ):

            st.session_state.messages = []

            st.rerun()

    # -----------------------------------
    # DOWNLOAD CHAT
    # -----------------------------------

    with col2:

        if st.session_state.messages:

            chat_text = ""

            for msg in (
                st.session_state.messages
            ):

                role = (
                    msg["role"]
                    .upper()
                )

                content = (
                    msg["content"]
                )

                chat_text += (
                    f"{role}:\n"
                    f"{content}\n\n"
                )

            st.download_button(

                label=
                "⬇ Download Chat",

                data=chat_text,

                file_name=
                "chat_history.txt",

                mime="text/plain"
            )

    # -----------------------------------
    # CHAT HISTORY
    # -----------------------------------

    for message in (
        st.session_state.messages
    ):

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )

    # -----------------------------------
    # CHAT INPUT
    # -----------------------------------

    question = st.chat_input(
        "Ask anything about the document..."
    )

    if question:

        # -------------------------------
        # USER MESSAGE
        # -------------------------------

        st.session_state.messages.append(

            {
                "role": "user",
                "content": question
            }

        )

        with st.chat_message(
            "user"
        ):

            st.write(
                question
            )

        # -------------------------------
        # GET ANSWER
        # -------------------------------

        with st.spinner(
            "Searching document..."
        ):

            result = get_answer(

                question,

                st.session_state.index,

                st.session_state.chunks,

                st.session_state
                .embedding_model,

                llm

            )

        answer = result[
            "answer"
        ]

        confidence = result[
            "confidence"
        ]

        source = result[
            "source"
        ]

              # -------------------------------
        # ASSISTANT MESSAGE
        # -------------------------------

        with st.chat_message("assistant"):

            st.markdown("## 🤖 Answer")

            st.success(answer)

            st.divider()

            st.markdown(
                "## 📊 Confidence Score"
            )

            st.progress(
                confidence / 100
            )

            if confidence >= 80:

                st.success(
                    f"{confidence}% Confidence"
                )

            elif confidence >= 50:

                st.warning(
                    f"{confidence}% Confidence"
                )

            else:

                st.error(
                    f"{confidence}% Confidence"
                )

            st.divider()

            st.markdown(
                "## 📚 Supporting Evidence"
            )

            if isinstance(
                source,
                list
            ):

                for i, src in enumerate(
                    source,
                    start=1
                ):

                    with st.expander(
                        f"Evidence {i}"
                    ):

                        st.write(src)

            else:

                st.info(source)

        # -------------------------------
        # SAVE CHAT
        # -------------------------------

        st.session_state.messages.append(

            {
                "role": "assistant",
                "content": answer
            }

        )
#else:

    st.info(
        "Upload a PDF document to begin."
    )

    st.markdown(
        """
### Features

✅ PDF Upload

✅ RAG Based Retrieval

✅ Gemini 2.5 Flash

✅ Hallucination Protection

✅ Confidence Score

✅ Source Tracking

✅ Document Summary

✅ Topic Extraction

✅ Download Chat

✅ Modern UI
"""
    )