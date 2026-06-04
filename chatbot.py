import numpy as np

SIMILARITY_THRESHOLD = 3.0


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
        k=5
    )

    best_distance = float(
        distances[0][0]
    )

    # ----------------------------------
    # HALLUCINATION GUARD
    # ----------------------------------

    if best_distance > SIMILARITY_THRESHOLD:

        return {

            "answer":
            "This information is not available in the document.",

            "confidence": 0,

            "source": [
                "No relevant information found."
            ]
        }

    # ----------------------------------
    # BUILD CONTEXT
    # ----------------------------------

    context = ""

    source_preview = []

    for idx in indices[0]:

        if idx < len(chunks):

            chunk_text = chunks[idx]

            context += (
                chunk_text +
                "\n\n"
            )

            source_preview.append(
                chunk_text[:350]
            )

    # ----------------------------------
    # PROMPT
    # ----------------------------------

    prompt = f"""
You are an AI Research Assistant.

STRICT RULES:

1. Answer ONLY using the provided context.
2. Never use outside knowledge.
3. Never guess information.
4. If answer is missing, reply exactly:

This information is not available in the document.

5. Keep answers concise and factual.
6. Give answers in a professional interview-ready format.
7. Do not mention context, chunks, retrieval process, embeddings, vector database, or sources.
8. Give direct answers.

Context:
{context}

Question:
{question}
"""

    # ----------------------------------
    # GENERATE ANSWER
    # ----------------------------------

    try:

        response = llm.generate_content(
            prompt
        )

        answer = (
            response.text.strip()
        )

    except Exception:

        answer = (
            "Error generating answer."
        )

    # ----------------------------------
    # CONFIDENCE SCORE
    # ----------------------------------

    confidence = int(

        max(
            50,
            min(
                100,
                (
                    1 -
                    (
                        best_distance / 5
                    )
                ) * 100
            )
        )

    )

    # ----------------------------------
    # RETURN RESULT
    # ----------------------------------

    return {

        "answer": answer,

        "confidence": confidence,

        "source": source_preview

    }