from app.services.llm_service import LLMService
from app.rag.retriever import Retriever
from app.tools.tool_selector import ToolSelector
from app.tools.web_search import WebSearchTool
from app.core.logger import logger


class TaskExecutorAgent:

    @staticmethod
    async def execute(task: str, session_id: str):
        try:
            logger.info(f"[Executor] Task: {task}")

            # -----------------------------
            # STEP 1: TOOL SELECTION
            # -----------------------------
            tool = await ToolSelector.select_tool(task)

            reasoning_steps = []
            reasoning_steps.append(f"Selected tool: {tool}")

            # -----------------------------
            # WEB SEARCH
            # -----------------------------
            if "web_search" in tool:
                reasoning_steps.append("Using web search for real-time information")

                results = WebSearchTool.search(task)

                return {
                    "answer": results[:4],
                    "sources": ["Web Search"],
                    "tool_used": "web_search",
                    "reason": "Query requires real-time or external information",
                    "steps": reasoning_steps
                }

            # -----------------------------
            # RAG
            # -----------------------------
            elif "rag" in tool:
                reasoning_steps.append("Retrieving document context")

                retrieved_chunks = Retriever.retrieve(task, session_id)

                if not retrieved_chunks:
                    return {
                        "answer": ["No relevant information found in document"],
                        "sources": [],
                        "tool_used": "rag",
                        "reason": "User asked about uploaded document",
                        "steps": reasoning_steps
                    }

                context = "\n".join(retrieved_chunks)
                reasoning_steps.append("Retrieved relevant chunks")

                prompt = f"""
                Answer ONLY using the document.

                DOCUMENT:
                {context}

                QUESTION:
                {task}

                RULES:
                - No external knowledge
                - Return 4 bullet points
                """

                response = await LLMService.generate_response(prompt)

                reasoning_steps.append("Generated answer from document")

                points = [
                    line.strip("-• ").strip()
                    for line in response.split("\n")
                    if line.strip()
                ]

                return {
                    "answer": points[:4],
                    "sources": retrieved_chunks,
                    "tool_used": "rag",
                    "reason": "Query refers to uploaded document",
                    "steps": reasoning_steps
                }

            # -----------------------------
            # NORMAL LLM
            # -----------------------------
            else:
                reasoning_steps.append("Using LLM for general reasoning")

                prompt = f"""
                Answer clearly:

                {task}

                Give 4 bullet points
                """

                response = await LLMService.generate_response(prompt)

                reasoning_steps.append("Generated answer using LLM knowledge")

                points = [
                    line.strip("-• ").strip()
                    for line in response.split("\n")
                    if line.strip()
                ]

                return {
                    "answer": points[:4],
                    "sources": ["LLM Knowledge"],
                    "tool_used": "llm",
                    "reason": "General knowledge query",
                    "steps": reasoning_steps
                }

        except Exception as e:
            logger.error(f"[Executor Error]: {str(e)}")

            return {
                "answer": ["Error processing request"],
                "sources": [],
                "tool_used": "error",
                "reason": "Execution failure",
                "steps": ["Exception occurred"]
            }