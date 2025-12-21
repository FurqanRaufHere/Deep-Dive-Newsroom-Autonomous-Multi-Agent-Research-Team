# 📰 Deep Dive Newsroom: Autonomous Multi-Agent Research Team

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange)](https://github.com/langchain-ai/langgraph)
[![Groq](https://img.shields.io/badge/LLM-Groq-green)](https://groq.com/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)](https://streamlit.io/)

**Deep Dive Newsroom** is an autonomous, multi-agent AI system designed to conduct deep-dive research and write high-quality technical articles. Unlike simple RAG systems, this project uses a specialized team of **6 autonomous agents** that collaborate, critique, and self-correct to ensure factual accuracy and depth.

---

## 🧠 System Architecture

The project is built on **LangGraph**, treating the research process as a state machine with a feedback loop.

### The Agent Team:
1.  **Editor (Planner):** Breaks down the user's topic into specific research questions and a structured outline.
2.  **Researcher:** Uses the **Tavily API** to perform real-time web searches for each specific question.
3.  **Analyst:** Filters raw search data, extracts hard facts, and resolves contradictions (KRR).
4.  **Writer:** Drafts a comprehensive Markdown article based on the facts and the Editor's outline.
5.  **Critic (Quality Control):** Compares the draft against the facts. If it finds hallucinations or missing data, it triggers a **Rewrite Loop**.
6.  **Publisher:** Polishes the final approved draft, adding an executive summary and professional formatting.



---

## 🚀 Key Features

* **Autonomous Logic:** Agents pass state and instructions without human intervention.
* **Self-Correction:** The Critic agent can "reject" work, sending it back to the Writer for improvement.
* **Real-time Research:** Integrated with Tavily for up-to-the-minute web data.
* **Lightning Fast Inference:** Powered by **Groq** (Llama-3.3-70b) for near-instant agent coordination.
* **Interactive Dashboard:** A professional Streamlit UI to monitor agent thoughts and progress.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/deep-dive-newsroom.git](https://github.com/YOUR_USERNAME/deep-dive-newsroom.git)
cd deep-dive-newsroom

pip install -r requirements.txt

# Create a .env file in the root directory:
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here

streamlit run frontend/app.py
```

