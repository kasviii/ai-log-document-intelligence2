from fastapi import APIRouter, HTTPException
from backend.services.text_extraction import extract_text_from_file
from backend.services.chunking import chunk_text
from backend.services.embeddings import generate_embeddings, get_model
from backend.vector_store.faiss_store import FAISSStore

router = APIRouter()


@router.get("/embed")
def embed_document(file_path: str):
    try:
        text = extract_text_from_file(file_path)
        chunks = chunk_text(text)
        embeddings = generate_embeddings(chunks)

        return {
            "file_path": file_path,
            "total_chunks": len(chunks),
            "embedding_dimension": len(embeddings[0]) if embeddings else 0
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/query")
def query_documents(question: str, k: int = 5):
    try:
        model = get_model()
        query_embedding = model.encode(question).tolist()

        store = FAISSStore(dimension=len(query_embedding))

        results = store.search(query_embedding, k)

        if not results:
            return {
                "question": question,
                "answer": "No relevant context found. Please upload and embed a document first.",
                "retrieved_chunks": [],
                "chunks_returned": 0
            }

        context = " ".join([r["text"] for r in results])

        answer = f"Based on the document context: {context[:300]}..."

        return {
            "question": question,
            "answer": answer,
            "retrieved_chunks": results,
            "chunks_returned": len(results)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))