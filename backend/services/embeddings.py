from sentence_transformers import SentenceTransformer
from backend.vector_store.faiss_store import FAISSStore

_model = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def generate_embeddings(chunks: list[str], source: str = "unknown") -> list[list[float]]:
    """
    Generate embeddings and persist to FAISS with source metadata.
    """
    model = get_model()
    embeddings = model.encode(chunks, convert_to_numpy=True)
    embeddings_list = embeddings.tolist()

    if embeddings_list:
        store = FAISSStore(dimension=len(embeddings_list[0]))
        metadata = [{"text": chunk, "source": source, "chunk_id": i} for i, chunk in enumerate(chunks)]
        store.add_embeddings(embeddings_list, metadata)
        store.save()

    return embeddings_list