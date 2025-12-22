import os
from typing import List
from langchain_community.tools.tavily_search import TavilySearchResults

def get_researcher_agent():
    # max_results=3 per question to keep it concise but deep
    search = TavilySearchResults(max_results=3)

    def run_research(questions: list[str]):
        all_results = []
        for query in questions:
            # Refine query by adding context for more relevant, recent results
            refined_query = f"latest research on {query}"
            results = search.invoke({"query": refined_query})
            all_results.append({"question": query, "results": results})
        return all_results

    return run_research
