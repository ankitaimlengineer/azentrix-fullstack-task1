from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


# -----------------------------------
# EMBEDDING MODEL LOADER
# -----------------------------------

def load_embedding_model():

    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )


# -----------------------------------
# SMART TEXT CHUNKING
# -----------------------------------

def split_text(
    text,
    chunk_size=700,
    overlap=150
):

    chunks = []

    start = 0

    text_length = len(text)

    while start < text_length:

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():

            chunks.append(
                chunk.strip()
            )

        start += (
            chunk_size - overlap
        )

    return chunks


# -----------------------------------
# VECTOR STORE CREATION
# -----------------------------------

def create_vector_store(text):

    chunks = split_text(
        text=text,
        chunk_size=700,
        overlap=150
    )

    embedding_model = (
        load_embedding_model()
    )

    embeddings = (
        embedding_model.encode(
            chunks,
            convert_to_numpy=True,
            show_progress_bar=False
        )
    )

    embeddings = embeddings.astype(
        "float32"
    )

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


# -----------------------------------
# RETRIEVE CHUNKS
# -----------------------------------

def retrieve_chunks(
    question,
    index,
    chunks,
    embedding_model,
    top_k=5
):

    query_embedding = (
        embedding_model.encode(
            [question],
            convert_to_numpy=True
        )
    )

    query_embedding = (
        query_embedding.astype(
            "float32"
        )
    )

    distances, indices = (
        index.search(
            query_embedding,
            top_k
        )
    )

    retrieved_chunks = []

    for idx in indices[0]:

        if idx < len(chunks):

            retrieved_chunks.append(
                chunks[idx]
            )

    return (
        retrieved_chunks,
        distances[0]
    )


# -----------------------------------
# GET VECTOR STORE STATS
# -----------------------------------

def get_vector_stats(
    index,
    chunks
):

    return {

        "total_chunks": len(chunks),

        "vector_dimension":
        index.d
    }