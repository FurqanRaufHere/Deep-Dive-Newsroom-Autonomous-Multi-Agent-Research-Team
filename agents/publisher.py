from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Define the publisher agent
def get_publisher_agent():
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Layout Editor. Take the approved article and add a 'Executive Summary' at the top and 'References' at the bottom."),
        ("human", "Final Article: {draft}")
    ])
    
    return prompt | llm