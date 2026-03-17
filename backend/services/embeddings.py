from sentence_transformers import SentenceTransformer
from backend.vector_store.faiss_store import FAISSStore

# Load once globally (important for performance)
_model = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def generate_embeddings(chunks: list[str]) -> list[list[float]]:
    """
    Generate embeddings locally using SentenceTransformers
    and persist them into FAISS.
    """
    model = get_model()
    embeddings = model.encode(chunks, convert_to_numpy=True)

    embeddings_list = embeddings.tolist()

    # Store embeddings in FAISS
    if embeddings_list:
        store = FAISSStore(dimension=len(embeddings_list[0]))
        metadata = [{"text": chunk} for chunk in chunks]
        store.add_embeddings(embeddings_list, metadata)
        store.save()

    return embeddings_list