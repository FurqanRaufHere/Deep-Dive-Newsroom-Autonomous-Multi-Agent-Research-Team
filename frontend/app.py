import streamlit as st
import asyncio
import sys
import os
import time
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from graph.workflow import build_workflow

# 1. Page Configuration
st.set_page_config(
    page_title="Deep Dive Newsroom",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Enhanced Custom CSS with animations and modern design
st.markdown("""
    <style>
    /* Main background and typography */
    .main { 
        background-color: #0e1117;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Animated gradient header */
    .hero-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        animation: fadeInDown 0.8s ease-out;
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Compact agent status line */
    .agent-status-line {
        background: linear-gradient(145deg, #1a1f2e, #252b3b);
        padding: 0.75rem 1.25rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #667eea;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    
    .agent-status-line:hover {
        border-left-width: 5px;
        padding-left: 1.5rem;
    }
    
    /* Pulsing dot for active status */
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
    }
    
    .status-working {
        background: #667eea;
        animation: pulse 1.5s infinite;
    }
    
    .status-complete {
        background: #10b981;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7); }
        50% { opacity: 0.8; box-shadow: 0 0 0 4px rgba(102, 126, 234, 0); }
    }
    
    /* Progress bar styling */
    .progress-container {
        background: #1a1f2e;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 24px;
        background: #1a1f2e;
        padding: 1rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] { 
        height: 50px;
        white-space: pre-wrap;
        font-weight: bold;
        background: transparent;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.1);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(145deg, #1a1f2e, #252b3b);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .metric-label {
        color: #8b92a7;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Article content styling */
    .article-content {
        background: #1a1f2e;
        padding: 2rem;
        border-radius: 12px;
        line-height: 1.8;
        font-size: 1.1rem;
    }
    
    /* Success animation */
    .success-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        animation: bounceIn 0.6s ease-out;
    }
    
    @keyframes bounceIn {
        0% { transform: scale(0); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    /* Sidebar enhancements */
    .css-1d391kg { background-color: #1a1f2e; }
    
    /* Example topics styling */
    .example-topic {
        background: rgba(102, 126, 234, 0.1);
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        border-left: 3px solid #667eea;
    }
    
    .example-topic:hover {
        background: rgba(102, 126, 234, 0.2);
        transform: translateX(5px);
    }
    
    /* Timeline styling */
    .timeline-item {
        padding-left: 2rem;
        border-left: 2px solid #667eea;
        margin-bottom: 1.5rem;
        position: relative;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -6px;
        top: 0;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #667eea;
        box-shadow: 0 0 0 4px #1a1f2e;
    }
    
    /* Compact info box */
    .info-box {
        background: rgba(102, 126, 234, 0.1);
        border-left: 3px solid #667eea;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        font-size: 0.85rem;
        color: #8b92a7;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Agent emoji mapping for visual appeal
AGENT_EMOJIS = {
    "Editor": "",
    "Researcher": "",
    "Analyst": "",
    "Writer": "",
    "Critic": "",
    "Publisher": ""
}

def show_compact_agent_status(agent_name, status):
    """Display compact agent status as a single line"""
    emoji = AGENT_EMOJIS.get(agent_name, "")
    status_class = "status-working" if status == "working" else "status-complete"
    status_text = "Working..." if status == "working" else "Complete"
    
    st.markdown(f"""
        <div class="agent-status-line">
            <span class="status-dot {status_class}"></span>
            <span>{emoji}</span>
            <strong style="color: #fff;">{agent_name}</strong>
            <span style="color: #8b92a7; margin-left: auto;">{status_text}</span>
        </div>
    """, unsafe_allow_html=True)

def show_metrics(final_state, elapsed_time):
    """Display research metrics in cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value"></div>
                <div class="metric-label">Status: Complete</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        word_count = len(final_state.get("final_article", "").split())
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{word_count:,}</div>
                <div class="metric-label">Words Generated</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        reading_time = max(1, word_count // 200)
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{reading_time}</div>
                <div class="metric-label">Min Read Time</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{elapsed_time:.1f}s</div>
                <div class="metric-label">Research Time</div>
            </div>
        """, unsafe_allow_html=True)

def show_example_topics():
    """Display clickable example topics"""
    st.markdown("### Example Topics")
    examples = [
        "The impact of Quantum Computing on Cybersecurity in 2025",
        "AI-powered drug discovery and its ethical implications",
        "The future of renewable energy storage solutions",
        "Blockchain technology in supply chain management",
        "Neuromorphic computing and brain-inspired AI"
    ]
    
    for example in examples:
        if st.button(f" {example}", key=example, use_container_width=True):
            st.session_state.selected_topic = example
            st.rerun()

def show_process_timeline(final_state):
    """Display research process as a timeline"""
    st.markdown("### Research Timeline")
    
    timeline_steps = [
        ("Editor", "Research plan created", final_state.get("plan")),
        ("Researcher", "Data collection completed", final_state.get("research_data")),
        ("Analyst", "Analysis performed", final_state.get("analysis")),
        ("Writer", "Article drafted", final_state.get("final_article")),
        ("Critic", "Quality review done", final_state.get("critique")),
        ("Publisher", "Article finalized", final_state.get("final_article"))
    ]
    
    for agent, description, data in timeline_steps:
        if data:
            emoji = AGENT_EMOJIS.get(agent, "")
            st.markdown(f"""
                <div class="timeline-item">
                    <strong>{emoji} {agent}</strong><br>
                    <span style="color: #8b92a7;">{description}</span>
                </div>
            """, unsafe_allow_html=True)

def main():
    # Initialize session state
    if 'selected_topic' not in st.session_state:
        st.session_state.selected_topic = ""
    
    # Hero Header
    st.markdown("""
        <div class="hero-header">
            <h1 style="margin: 0; color: white;"> Deep Dive Newsroom</h1>
            <p style="margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.9); font-size: 1.2rem;">
                Autonomous Multi-Agent Research Team
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 2. Sidebar for Controls
    with st.sidebar:
        st.markdown("## Control Panel")
        
        # Use session state for topic
        if st.session_state.selected_topic:
            topic = st.text_area(
                "Enter Research Topic:", 
                value=st.session_state.selected_topic,
                placeholder="e.g., The impact of Quantum Computing on Cybersecurity in 2025",
                height=120
            )
            st.session_state.selected_topic = ""  # Reset after using
        else:
            topic = st.text_area(
                "Enter Research Topic:", 
                placeholder="e.g., The impact of Quantum Computing on Cybersecurity in 2025",
                height=120
            )
        
        # Start button right after input
        run_button = st.button("Start Research", use_container_width=True, type="primary")
        
        st.divider()
        
        # Compact agent info
        st.markdown('<div class="info-box"> <strong>Active Agents:</strong> Editor, Researcher, Analyst, Writer, Critic, Publisher</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Show example topics when no research is running
        if 'research_running' not in st.session_state or not st.session_state.research_running:
            show_example_topics()

    # 3. Main Display Area
    if run_button and topic:
        st.session_state.research_running = True
        start_time = time.time()
        
        # Compact progress section
        st.markdown("## Research Progress")
        
        # Single progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Compact agent status area
        agent_status_container = st.container()
        
        with agent_status_container:
            agents = ["Editor", "Researcher", "Analyst", "Writer", "Critic", "Publisher"]
            agent_status_placeholders = {}
            
            # Create placeholders for each agent in a compact way
            for agent in agents:
                agent_status_placeholders[agent] = st.empty()
            
            # Simulate agent progress
            for idx, agent in enumerate(agents):
                progress = (idx + 1) / len(agents)
                progress_bar.progress(progress)
                status_text.markdown(f"**{AGENT_EMOJIS.get(agent, '')} {agent} is working...**")
                
                # Update current agent to working
                with agent_status_placeholders[agent]:
                    show_compact_agent_status(agent, "working")
                
                # Small delay for visual effect
                time.sleep(0.3)
            
            # Build and run graph
            status_text.markdown("**Finalizing research...**")
            app = build_workflow()
            initial_state = {"topic": topic, "revision_count": 0}
            
            # Execute Graph
            final_state = app.invoke(initial_state)
            
            elapsed_time = time.time() - start_time
            
            # Update all agents to complete
            for agent in agents:
                with agent_status_placeholders[agent]:
                    show_compact_agent_status(agent, "complete")
            
            progress_bar.progress(1.0)
            status_text.markdown("### <span class='success-badge'>Research Complete!</span>", unsafe_allow_html=True)

        st.divider()
        
        # Show metrics
        show_metrics(final_state, elapsed_time)
        
        st.divider()

        # 4. Result Organization with enhanced tabs
        tab_final, tab_process, tab_timeline, tab_raw = st.tabs([
            "Final Article", 
            "Process Insights",
            "Timeline",
            "Raw Research"
        ])

        with tab_final:
            st.markdown("## Executive Summary")
            
            # Extract executive summary if available
            article = final_state.get("final_article", "No article generated.")
            if article and "Executive Summary" in article:
                summary_start = article.find("Executive Summary")
                summary_end = article.find("\n\n", summary_start)
                if summary_end == -1:
                    summary_end = summary_start + 500
                summary = article[summary_start:summary_end]
                st.info(summary)
            
            st.divider()
            
            # Display full article
            st.markdown('<div class="article-content">', unsafe_allow_html=True)
            st.markdown(article)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Export options
            st.divider()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button(
                    label="Download as Markdown",
                    data=article,
                    file_name=f"research_{topic[:30]}.md",
                    mime="text/markdown"
                )
            with col2:
                st.download_button(
                    label="Download as Text",
                    data=article,
                    file_name=f"research_{topic[:30]}.txt",
                    mime="text/plain"
                )
            with col3:
                if st.button("Share Article"):
                    st.success("Share link copied! (Feature coming soon)")

        with tab_process:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Editor's Plan")
                with st.expander("View Full Plan", expanded=True):
                    plan = final_state.get("plan", {})
                    if isinstance(plan, dict):
                        st.json(plan)
                    else:
                        st.write(plan)
                
                st.markdown("### Critic's Feedback")
                with st.expander("View Critique"):
                    critique = final_state.get("critique", {})
                    if isinstance(critique, dict):
                        st.json(critique)
                    else:
                        st.write(critique)
            
            with col2:
                st.markdown("### Analyst's Insights")
                with st.expander("View Analysis", expanded=True):
                    analysis = final_state.get("analysis", {})
                    if isinstance(analysis, dict):
                        key_points = analysis.get("key_points", [])
                        if key_points:
                            for point in key_points:
                                st.markdown(f"• {point}")
                        else:
                            st.json(analysis)
                    else:
                        st.write(analysis)
                
                st.markdown("### Writer's Notes")
                with st.expander("View Writing Process"):
                    st.write("Article structure, tone, and approach details")
                    st.info("Writer successfully completed the article based on research and analysis.")

        with tab_timeline:
            show_process_timeline(final_state)

        with tab_raw:
            st.markdown("### Raw Research Data")
            st.caption("Data collected by the Researcher agent")
            
            research_data = final_state.get("research_data", {})
            if research_data:
                st.json(research_data)
            else:
                st.warning("No raw research data available")
            
            # Show full state for debugging
            with st.expander("Complete State (Debug)"):
                st.json(final_state)

        st.session_state.research_running = False

    elif run_button and not topic:
        st.warning("Please enter a research topic first!")
        st.info("Try one of the example topics from the sidebar!")
    
    # Show welcome message when no research has been done
    elif 'research_running' not in st.session_state or not st.session_state.research_running:
        st.markdown("""
            <div style="text-align: center; padding: 4rem 2rem;">
                <h2 style="color: #667eea;">Welcome to Deep Dive Newsroom</h2>
                <p style="color: #8b92a7; font-size: 1.2rem; margin: 1rem 0;">
                    Your AI-powered research team is ready to dive deep into any topic.
                </p>
                <p style="color: #8b92a7;">
                    Enter a research topic in the sidebar and click "Start Research" to begin!
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Show feature highlights
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div class="metric-card">
                    <div style="font-size: 3rem;"></div>
                    <h3>Deep Research</h3>
                    <p style="color: #8b92a7;">Multi-source analysis and fact-checking</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="metric-card">
                    <div style="font-size: 3rem;"></div>
                    <h3>6 AI Agents</h3>
                    <p style="color: #8b92a7;">Specialized team for quality output</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="metric-card">
                    <div style="font-size: 3rem;"></div>
                    <h3>Publication Ready</h3>
                    <p style="color: #8b92a7;">Professional articles in minutes</p>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

# import streamlit as st
# import asyncio
# import sys
# import os
# sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
# from graph.workflow import build_workflow

# # 1. Page Configuration (The "Professional" Look)
# st.set_page_config(
#     page_title="Deep Dive Newsroom",
#     page_icon="📰",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # Custom CSS for a sleek, modern look
# st.markdown("""
#     <style>
#     .main { background-color: #0e1117; }
#     .stTabs [data-baseweb="tab-list"] { gap: 24px; }
#     .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; font-weight: bold; }
#     .agent-status { padding: 10px; border-radius: 5px; margin-bottom: 10px; border-left: 5px solid #ff4b4b; }
#     </style>
#     """, unsafe_allow_html=True)

# def main():
#     st.title("📰 Deep Dive Newsroom")
#     st.subheader("Autonomous Multi-Agent Research Team")
#     st.divider()

#     # 2. Sidebar for Controls
#     with st.sidebar:
#         st.header("Control Panel")
#         topic = st.text_area("Enter Research Topic:", placeholder="e.g., The impact of Quantum Computing on Cybersecurity in 2025")
        
#         # Optional: Sliders for model behavior if you want to pass these to the graph
#         st.info("Agents: Editor, Researcher, Analyst, Writer, Critic, Publisher")
        
#         run_button = st.button("Start Research", use_container_width=True)

#     # 3. Main Display Area
#     if run_button and topic:
#         # We use a container to show real-time progress
#         progress_container = st.container()
        
#         with progress_container:
#             st.write("### 🤖 Agent Workspace")
            
#             # Using st.status for a professional "thinking" feel
#             with st.status("Initializing Autonomous Team...", expanded=True) as status:
#                 # Build and run graph
#                 app = build_workflow()
#                 initial_state = {"topic": topic, "revision_count": 0}
                
#                 # Execute Graph
#                 # Note: For production-speed UI, we use invoke(). 
#                 # If you want streaming per token, that's Phase 7.
#                 final_state = app.invoke(initial_state)
                
#                 status.update(label="Research Complete!", state="complete", expanded=False)

#         # 4. Result Organization (Tabs for Cleanliness)
#         tab_final, tab_process, tab_raw = st.tabs(["Final Article", "Process Insights", "Raw Research"])

#         with tab_final:
#             st.markdown(final_state.get("final_article", "No article generated."))

#         with tab_process:
#             col1, col2 = st.columns(2)
#             with col1:
#                 with st.expander("📝 Editor's Plan", expanded=True):
#                     st.json(final_state.get("plan"))
#                 with st.expander("⚖️ Critic's Feedback"):
#                     st.json(final_state.get("critique"))
            
#             with col2:
#                 with st.expander("📊 Analyst's Fact Sheet", expanded=True):
#                     st.write(final_state.get("analysis", {}).get("key_points", []))

#         with tab_raw:
#             st.write("Raw data pulled by the Researcher agent:")
#             st.json(final_state.get("research_data"))

#     elif run_button and not topic:
#         st.warning("Please enter a topic first!")

# if __name__ == "__main__":
#     main()