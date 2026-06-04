from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


# ----------------------------------
# TEXT CHUNKING
# ----------------------------------

def split_text(
    text,
    chunk_size=500,
    overlap=100
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():

            chunks.append(chunk)

        start += (
            chunk_size - overlap
        )

    return chunks


# ----------------------------------
# VECTOR STORE CREATION
# ----------------------------------

def create_vector_store(text):

    # Create Chunks
    chunks = split_text(
        text=text,
        chunk_size=500,
        overlap=100
    )

    # Load Embedding Model
    embedding_model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    # Create Embeddings
    embeddings = embedding_model.encode(
        chunks,
        convert_to_numpy=True
    )

    embeddings = embeddings.astype(
        "float32"
    )

    # Create FAISS Index
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        embeddings
    )

    return (
        index,
        chunks,
        embedding_model
    )