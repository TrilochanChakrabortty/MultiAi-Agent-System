from app.services.llm_service import LLMService


class ToolSelector:

    @staticmethod
    async def select_tool(query: str):
        prompt = f"""
        Decide how to answer this query.

        Options:
        - rag → if query depends on uploaded document
        - web_search → if real-time or external info needed
        - none → general knowledge

        Query: {query}

        Rules:
        - If user refers to "my file", "pdf", "resume", "document" → rag
        - If query needs latest info → web_search
        - Otherwise → none

        Return ONLY: rag / web_search / none
        """

        response = await LLMService.generate_response(prompt)
        return response.strip().lower()