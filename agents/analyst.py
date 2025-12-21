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
        ("system", "You are a Fact-Analyst. Review the raw research and extract only verified, non-redundant facts."),
        ("human", "Raw Research: {research_data}")
    ])
    
    return prompt | llm.with_structured_output(AnalysisOutput)