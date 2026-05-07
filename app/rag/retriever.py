from app.rag.embeddings import get_embedding
from app.rag.vector_store import vector_store


class Retriever:

    @staticmethod
    def retrieve(query: str, session_id: str, document_id=None):
        query_embedding = get_embedding(query)

        results = vector_store.search(
            query_embedding,
            session_id,
            document_id
        )

        return results[:3]