from app.services.llm_service import LLMService


class PlannerAgent:

    @staticmethod
    async def create_plan(query: str):
        """
        Smart planner:
        - Simple query → return as-is
        - Complex query → break into tasks
        """

        prompt = f"""
        Decide if the query is simple or complex.

        Query: {query}

        Rules:
        - If simple → return EXACT query only
        - If complex → return 2-3 short tasks
        - Return ONLY a Python list
        - No explanation

        Example:
        Simple → ["how to reuse plastic bottle"]
        Complex → ["analyze document", "extract key points"]
        """

        response = await LLMService.generate_response(prompt)

        try:
            tasks = eval(response)

            if not isinstance(tasks, list):
                return [query]

            return tasks

        except:
            return [query]