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

    def search(self, query_embedding, k=5):
        # If index is empty, return nothing
        if self.index.ntotal == 0:
            return []

        query_vector = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_vector, k)

        results = []
        for i, idx in enumerate(indices[0]):
            # FAISS returns -1 for empty slots — skip those
            if idx == -1:
                continue
            if idx < len(self.metadata):
                results.append({
                    "text": self.metadata[idx]["text"],
                    "score": float(distances[0][i])
                })

        return results