from typing import List
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

class AnalysisOutput(BaseModel):
    key_points: List[str] = Field(description="The most important facts extracted from research.")
    verified_sources: List[str] = Field(description="URLs of the most credible sources found.")

def get_analyst_agent():
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Fact-Analyst specializing in extracting high-quality, verified information from raw research data. Your task is to review the provided raw research and extract only the most important, verified, and non-redundant facts.

Key Guidelines:
- **Verification**: Prioritize facts from credible sources such as academic journals, reputable news outlets (e.g., BBC, Reuters), government websites, or peer-reviewed studies. Avoid unverified claims, rumors, or biased sources.
- **Non-Redundancy**: Eliminate duplicates or very similar facts; merge them into a single, concise statement if possible.
- **Key Points**: Focus on 5-10 of the most impactful facts that directly relate to the topic. Prioritize facts that are recent, data-driven, or have significant implications.
- **Output Format**: Provide facts as concise bullet points, each including a brief source citation (e.g., URL or source name) for verification. Ensure facts are neutral, accurate, and directly supported by the research data.

Example:
- Fact: CRISPR technology has reduced crop losses due to pests by up to 30% in field trials (Source: Nature Biotechnology, 2022).
- Fact: Ethical concerns include off-target gene edits in human applications (Source: WHO Report on Gene Editing).

Do not add opinions, speculations, or external knowledge—stick strictly to the provided research data."""),
        ("human", "Raw Research: {research_data}")
    ])
    
    return prompt | llm.with_structured_output(AnalysisOutput)