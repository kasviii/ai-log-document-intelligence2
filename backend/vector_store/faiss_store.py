import faiss
import numpy as np
import os
import pickle

INDEX_FILE = "faiss.index"
METADATA_FILE = "metadata.pkl"


class FAISSStore:
    def __init__(self, dimension: int):
        self.dimension = dimension

        if os.path.exists(INDEX_FILE) and os.path.exists(METADATA_FILE):
            self.index = faiss.read_index(INDEX_FILE)
            with open(METADATA_FILE, "rb") as f:
                self.metadata = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(dimension)
            self.metadata = []

    def add_embeddings(self, embeddings, metadatas):
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.metadata.extend(metadatas)

    def save(self):
        faiss.write_index(self.index, INDEX_FILE)
        with open(METADATA_FILE, "wb") as f:
            pickle.dump(self.metadata, f)

    def search(self, query_embedding, k=5, source_filter: str = None):
        if self.index.ntotal == 0:
            return []

        # Search more candidates if filtering by source, to ensure enough results
        search_k = k * 5 if source_filter else k
        query_vector = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_vector, search_k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx == -1:
                continue
            if idx >= len(self.metadata):
                continue

            meta = self.metadata[idx]

            # Filter by source filename if provided
            if source_filter and source_filter not in meta.get("source", ""):
                continue

            results.append({
                "text": meta["text"],
                "source": meta.get("source", "unknown"),
                "chunk_id": meta.get("chunk_id", idx),
                "score": float(distances[0][i])
            })

            if len(results) >= k:
                break

        return results