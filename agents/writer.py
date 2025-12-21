from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

def get_writer_agent():
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Professional Tech Writer. Use the provided facts and outline to write a comprehensive, engaging article in Markdown."),
        ("human", "Outline: {outline}\n\nFacts: {facts}")
    ])
    
    return prompt | llm # We want a raw string back, so no Pydantic here.