import faiss
import numpy as np

VECTOR_DIM = 64


class VectorStore:

    def __init__(self):
        self.index = faiss.IndexFlatL2(VECTOR_DIM)
        self.texts = []
        self.metadata = []  # store session_id + document_id

    def add(self, embeddings, texts, session_id, document_id):
        embeddings = np.array(embeddings).astype("float32")

        self.index.add(embeddings)
        self.texts.extend(texts)

        for _ in texts:
            self.metadata.append({
                "session_id": session_id,
                "document_id": document_id
            })

    def search(self, query_embedding, session_id, document_id=None, k=5):
        if len(self.texts) == 0:
            return []

        query_embedding = np.array([query_embedding]).astype("float32")

        D, I = self.index.search(query_embedding, k)

        results = []

        for i in I[0]:
            if i < len(self.texts):
                meta = self.metadata[i]

                if meta["session_id"] == session_id:
                    if document_id is None or meta["document_id"] == document_id:
                        results.append(self.texts[i])

        return results


vector_store = VectorStore()