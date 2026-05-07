import os
from tavily import TavilyClient

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


class WebSearchTool:

    @staticmethod
    def search(query: str):
        try:
            response = client.search(
                query=query,
                search_depth="basic",
                max_results=5
            )

            results = []

            for r in response.get("results", []):
                results.append(r.get("content", ""))

            # Return top 4 cleaned results
            return results[:4] if results else ["No results found"]

        except Exception as e:
            return [f"Web search error: {str(e)}"]