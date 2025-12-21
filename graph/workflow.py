import os
from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END
from graph.state import NewsroomState
from agents.editor import get_editor_agent
from agents.researcher import get_researcher_agent
from agents.analyst import get_analyst_agent
from agents.writer import get_writer_agent
from agents.critic import get_critic_agent
from agents.publisher import get_publisher_agent

def build_workflow():
    # 1. Initialize the Graph with our State
    workflow = StateGraph(NewsroomState)

    # 2. Define the Node Functions
    # Each function takes 'state', performs a task, and returns an update to the state.
    
    def editor_node(state: NewsroomState):
        agent = get_editor_agent()
        result = agent.invoke({"topic": state["topic"]})
        return {"plan": result.dict(), "revision_count": 0}

    def researcher_node(state: NewsroomState):
        # We extract questions from the plan created by the editor
        questions = state["plan"]["research_questions"]
        run_research = get_researcher_agent()
        data = run_research(questions)
        return {"research_data": data}

    def analyst_node(state: NewsroomState):
        agent = get_analyst_agent()
        result = agent.invoke({"research_data": str(state["research_data"])})
        return {"analysis": result.dict()}

    def writer_node(state: NewsroomState):
        agent = get_writer_agent()
        result = agent.invoke({
            "outline": state["plan"]["outline"],
            "facts": state["analysis"]["key_points"]
        })
        return {"draft": result.content}

    def critic_node(state: NewsroomState):
        agent = get_critic_agent()
        result = agent.invoke({
            "facts": state["analysis"]["key_points"],
            "draft": state["draft"]
        })
        return {"critique": result.dict()}

    def publisher_node(state: NewsroomState):
        agent = get_publisher_agent()
        result = agent.invoke({"draft": state["draft"]})
        return {"final_article": result.content}

    # 3. Add Nodes to Graph
    workflow.add_node("editor", editor_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("critic", critic_node)
    workflow.add_node("publisher", publisher_node)

    # 4. Define Linear Edges
    workflow.set_entry_point("editor")
    workflow.add_edge("editor", "researcher")
    workflow.add_edge("researcher", "analyst")
    workflow.add_edge("analyst", "writer")
    workflow.add_edge("writer", "critic")

    # 5. Define Conditional Logic (The Loop)
    def should_continue(state: NewsroomState):
        critique = state["critique"]
        # If approved OR we've tried too many times (safety valve)
        if critique["decision"] == "approve" or state["revision_count"] >= 2:
            return "publish"
        else:
            print(f"--- REJECTED BY CRITIC: {critique['feedback']} ---")
            return "rewrite"

    workflow.add_conditional_edges(
        "critic",
        should_continue,
        {
            "publish": "publisher",
            "rewrite": "writer"
        }
    )

    workflow.add_edge("publisher", END)

    return workflow.compile()