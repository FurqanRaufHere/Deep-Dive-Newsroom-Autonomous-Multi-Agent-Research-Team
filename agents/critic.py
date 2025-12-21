from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

class Critique(BaseModel):
    decision: str = Field(description="Either 'approve' or 'reject'")
    feedback: str = Field(description="If rejected, provide specific instructions for improvement.")

def get_critic_agent():
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Quality Control Expert. Check the article for: 1. Adherence to outline. 2. Fact accuracy. 3. Tone. Decide to 'approve' or 'reject'."),
        ("human", "Original Facts: {facts}\n\nDraft Article: {draft}")
    ])
    
    return prompt | llm.with_structured_output(Critique)