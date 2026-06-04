import numpy as np

SIMILARITY_THRESHOLD = 1.50


def get_answer(
    question,
    index,
    chunks,
    embedding_model,
    llm
):

    # ----------------------------------
    # QUESTION EMBEDDING
    # ----------------------------------

    query_embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True
    )

    query_embedding = query_embedding.astype(
        "float32"
    )

    # ----------------------------------
    # VECTOR SEARCH
    # ----------------------------------

    distances, indices = index.search(
        query_embedding,
        k=3
    )

    # ----------------------------------
    # HALLUCINATION GUARD
    # ----------------------------------

    best_distance = float(
        distances[0][0]
    )

    if best_distance > SIMILARITY_THRESHOLD:

        return {
            "answer":
            "This information is not available in the document.",

            "confidence": 0,

            "source":
            "No relevant source found."
        }

    # ----------------------------------
    # BUILD CONTEXT
    # ----------------------------------

    context = ""

    source_chunks = []

    for idx in indices[0]:

        if idx < len(chunks):

            context += (
                chunks[idx] + "\n\n"
            )

            source_chunks.append(
                idx + 1
            )

    # ----------------------------------
    # PROMPT
    # ----------------------------------

    prompt = f"""
You are a document assistant.

Rules:

1. Answer ONLY using the context.
2. Do not use outside knowledge.
3. If answer is not available,
   reply exactly:

This information is not available in the document.

Context:
{context}

Question:
{question}
"""

    # ----------------------------------
    # GEMINI RESPONSE
    # ----------------------------------

    try:

        response = llm.generate_content(
            prompt
        )

        answer = response.text

    except Exception:

        answer = (
            "Error generating answer."
        )

    # ----------------------------------
    # CONFIDENCE SCORE
    # ----------------------------------

    confidence = int(

        max(
            0,
            min(
                100,
                (1 - best_distance / 2)
                * 100
            )
        )

    )

    # ----------------------------------
    # RETURN RESULT
    # ----------------------------------

    return {

        "answer": answer,

        "confidence": confidence,

        "source":
        f"Retrieved Chunks: {source_chunks}"

    }