from dotenv import load_dotenv
from graph.workflow import build_workflow

load_dotenv()

def main():
    app = build_workflow()
    
    # Input the topic
    initial_state = {"topic": "The future of renewable energy in 2025"}
    
    # Run the graph
    print("🚀 Starting the Newsroom Research Team...")
    final_state = app.invoke(initial_state)
    
    print("\n--- FINAL ARTICLE ---")
    print(final_state["final_article"])

if __name__ == "__main__":
    main()