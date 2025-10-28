from src.graph import sokoban_graph
from src.sokoban import game_environment
from pathlib import Path
from src.graph.nodes import state_initiator


def main():
    print("Hello from sokoban-llm-agent!")
    parent_dir = Path.cwd()

    data_file = parent_dir / "dataset/human_demos/1_0.txt"   
    model_name = "Qwen/Qwen3-14B"

    initial_map = game_environment.SokobanGame(data_file)

    print("Initial Map:")
    print(str(initial_map.serialize_map()))

    agent_state = state_initiator.initiate_state(initial_map, model_name)
    graph = sokoban_graph.build_sokoban_graph()
    app = graph.compile()
    app.invoke(agent_state, config={"recursion_limit": 50})


if __name__ == "__main__":
    main()
