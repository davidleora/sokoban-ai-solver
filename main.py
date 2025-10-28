from src.graph import sokoban_graph
from src.sokoban import game_environment
from pathlib import Path
from src.graph.nodes import state_initiator
from src.graph.llm.client import LLM_client as LLM_client_local
import sys

def main():
    print("Hello from sokoban-llm-agent!")
    parent_dir = Path.cwd()

    if len(sys.argv) > 1:
        data_file = parent_dir / sys.argv[1]
    else:
        data_file = parent_dir / "dataset/human_demos/1_0.txt"

    model_name = "openai/gpt-oss-20b"

    if not data_file.exists():
        print(f"Error: Data file {data_file} does not exist")
        sys.exit(1)

    initial_map = game_environment.SokobanGame(data_file)

    print("Initial Map:")
    print(str(initial_map.serialize_map()))

    # Load model once
    print(f"\n🔄 Loading model {model_name}...")
    llm_client = LLM_client_local(model_name)
    print(f"✅ Model loaded!\n")

    agent_state = state_initiator.initiate_state(initial_map, model_name)
    agent_state['llm_client'] = llm_client  # Pass pre-loaded client
    graph = sokoban_graph.build_sokoban_graph()
    app = graph.compile()
    app.invoke(agent_state, config={"recursion_limit": 50})

if __name__ == "__main__":
    main()
