import os
from typing import List
from langchain_community.tools.tavily_search import TavilySearchResults

def get_researcher_agent():
    # max_results=3 per question to keep it concise but deep
    search = TavilySearchResults(max_results=3)
    
    def run_research(questions: list[str]):
        all_results = []
        for query in questions:
            results = search.invoke({"query": query})
            all_results.append({"question": query, "results": results})
        return all_results
    
    return run_research