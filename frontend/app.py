import streamlit as st
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from graph.workflow import build_workflow

# 1. Page Configuration (The "Professional" Look)
st.set_page_config(
    page_title="Deep Dive Newsroom",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for a sleek, modern look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; font-weight: bold; }
    .agent-status { padding: 10px; border-radius: 5px; margin-bottom: 10px; border-left: 5px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("📰 Deep Dive Newsroom")
    st.subheader("Autonomous Multi-Agent Research Team")
    st.divider()

    # 2. Sidebar for Controls
    with st.sidebar:
        st.header("Control Panel")
        topic = st.text_area("Enter Research Topic:", placeholder="e.g., The impact of Quantum Computing on Cybersecurity in 2025")
        
        # Optional: Sliders for model behavior if you want to pass these to the graph
        st.info("Agents: Editor, Researcher, Analyst, Writer, Critic, Publisher")
        
        run_button = st.button("Start Research", use_container_width=True)

    # 3. Main Display Area
    if run_button and topic:
        # We use a container to show real-time progress
        progress_container = st.container()
        
        with progress_container:
            st.write("### 🤖 Agent Workspace")
            
            # Using st.status for a professional "thinking" feel
            with st.status("Initializing Autonomous Team...", expanded=True) as status:
                # Build and run graph
                app = build_workflow()
                initial_state = {"topic": topic, "revision_count": 0}
                
                # Execute Graph
                # Note: For production-speed UI, we use invoke(). 
                # If you want streaming per token, that's Phase 7.
                final_state = app.invoke(initial_state)
                
                status.update(label="Research Complete!", state="complete", expanded=False)

        # 4. Result Organization (Tabs for Cleanliness)
        tab_final, tab_process, tab_raw = st.tabs(["Final Article", "Process Insights", "Raw Research"])

        with tab_final:
            st.markdown(final_state.get("final_article", "No article generated."))

        with tab_process:
            col1, col2 = st.columns(2)
            with col1:
                with st.expander("📝 Editor's Plan", expanded=True):
                    st.json(final_state.get("plan"))
                with st.expander("⚖️ Critic's Feedback"):
                    st.json(final_state.get("critique"))
            
            with col2:
                with st.expander("📊 Analyst's Fact Sheet", expanded=True):
                    st.write(final_state.get("analysis", {}).get("key_points", []))

        with tab_raw:
            st.write("Raw data pulled by the Researcher agent:")
            st.json(final_state.get("research_data"))

    elif run_button and not topic:
        st.warning("Please enter a topic first!")

if __name__ == "__main__":
    main()