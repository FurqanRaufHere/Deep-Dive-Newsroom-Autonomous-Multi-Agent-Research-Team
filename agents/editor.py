import os
from typing import List
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Define the structured output format
class ResearchPlan(BaseModel):
    research_questions: List[str] = Field(description="4-6 specific questions to research.")
    outline: List[str] = Field(description="A logical structure for the final article.")

def get_editor_agent(model_name="llama-3.3-70b-versatile"):
    llm = ChatGroq(model=model_name, temperature=0.2)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Senior News Editor. Your job is to take a broad topic and 
        create a focused research plan. Break the topic down into specific, analytical 
        questions that a researcher can answer. Create a clear outline for the final report."""),
        ("human", "Topic: {topic}")
    ])
    
    # Use structured output to ensure the graph can read the result
    return prompt | llm.with_structured_output(ResearchPlan)

# Test logic
if __name__ == "__main__":
    # Ensure GROQ_API_KEY is in your .env
    editor = get_editor_agent()
    result = editor.invoke({"topic": "The impact of CRSPR on agricultural sustainability"})
    print("Research Questions:", result.research_questions)
    print("Outline:", result.outline)