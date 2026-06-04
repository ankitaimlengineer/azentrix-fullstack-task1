# 🤖 AI Research Assistant

A Context-Aware Document Question Answering System built using Streamlit, FAISS, Sentence Transformers, and Google Gemini.

The application allows users to upload PDF documents and ask questions based strictly on the uploaded document.

---

# Features

✅ PDF Upload

✅ RAG Based Retrieval

✅ Gemini 2.5 Flash Integration

✅ Hallucination Protection

✅ Confidence Score

✅ Source Tracking

✅ Document Summary

✅ Key Topic Extraction

✅ Download Chat

✅ Professional Dark UI

---

# Problem Statement

People spend significant time searching lengthy documents for specific information.

This project solves that problem by enabling users to upload a PDF and interact with it using natural language questions.

The assistant answers only from the provided document and avoids generating unsupported information.

---

# Architecture

PDF Upload
↓
PDF Extraction
↓
Chunking
↓
Sentence Embeddings
↓
FAISS Vector Store
↓
Similarity Search
↓
Context Retrieval
↓
Gemini 2.5 Flash
↓
Answer Generation

---

# Tech Stack

* Python
* Streamlit
* Google Gemini 2.5 Flash
* Sentence Transformers
* FAISS
* NumPy
* PyPDF
* Python Dotenv

---

# Project Structure

azentrix-fullstack-task1/

├── app.py

├── chatbot.py

├── vector_store.py

├── pdf_reader.py

├── requirements.txt

├── README.md

├── DESIGN.md

├── .env

└── .streamlit/config.toml

---

# Installation

Clone Repository

git clone YOUR_REPOSITORY_URL

Move to Project Folder

cd azentrix-fullstack-task1

Create Virtual Environment

python -m venv venv

Activate Environment

Windows:

venv\Scripts\activate

Install Dependencies

pip install -r requirements.txt

---

# Environment Variable

Create .env file

GEMINI_API_KEY=YOUR_API_KEY

---

# Run Project

streamlit run app.py

---

# Screenshots

Add screenshots in screenshots folder.

Suggested screenshots:

* Home Screen
* PDF Upload
* Document Summary
* Question Answering
* Confidence Score
* Source Display

---

# Demo Video

Add Loom Video Link Here

---

# Future Improvements

* Multi PDF Support
* Citation Based Answers
* OCR Support
* ChromaDB Integration
* Agentic AI Workflows
* Cloud Deployment

---

# Author

Ankit Thummar

BCA Graduate

Python Developer

AI & Machine Learning Enthusiast

---

# License

This project is submitted as part of the Azentrix Generative AI Internship Assessment.
