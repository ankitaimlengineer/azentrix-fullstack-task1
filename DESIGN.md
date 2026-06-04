# DESIGN.md

## Project Title

AI Research Assistant – RAG Based PDF Question Answering System

---

## Objective

The goal of this project is to build a Context-Aware Document Question Answering Bot that answers questions only from the uploaded PDF document and prevents hallucinations.

---

## Architecture

PDF Upload
↓
PDF Text Extraction
↓
Text Chunking
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
Final Answer

---

## Architectural Decisions

### PDF Processing

PyPDF was selected because it is lightweight, easy to use, and supports text extraction from most PDF documents.

### Embedding Model

The all-MiniLM-L6-v2 Sentence Transformer model was chosen because it provides good semantic understanding while remaining fast and lightweight.

### Vector Database

FAISS was used as the vector store because it offers high-speed similarity search and is widely used in Retrieval Augmented Generation systems.

### LLM Selection

Gemini 2.5 Flash was selected due to:

* Fast response time
* Strong reasoning ability
* Free API availability
* Excellent document understanding

---

## Retrieval Process

1. User uploads PDF.
2. Text is extracted.
3. Text is split into chunks.
4. Chunks are converted into embeddings.
5. Embeddings are stored in FAISS.
6. User asks a question.
7. Question embedding is generated.
8. Top relevant chunks are retrieved.
9. Gemini receives only retrieved context.
10. Final answer is generated.

---

## Hallucination Prevention

The system uses a similarity threshold.

If retrieved chunks are not relevant enough, the assistant returns:

"This information is not available in the document."

This ensures answers are based only on document content.

---

## Challenges Faced

### Challenge 1

Large PDF processing can be slow.

Solution:

Chunking and vector search reduce processing overhead.

### Challenge 2

Preventing hallucinations.

Solution:

Strict prompting and similarity threshold checks.

### Challenge 3

Maintaining answer relevance.

Solution:

Top-K retrieval with semantic embeddings.

---

## Future Improvements

* Multi PDF Support
* Page Number Citations
* ChromaDB Integration
* Conversation Memory
* Agentic Workflows
* OCR Support
* Document Comparison
* Cloud Deployment

---

## Conclusion

The project successfully demonstrates a Retrieval Augmented Generation pipeline capable of answering document-specific questions while minimizing hallucinations.
