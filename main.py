from src.graph import sokoban_graph
from src.sokoban import game_environment
from pathlib import Path
from src.graph.nodes import state_initiator


def main():
    print("Hello from sokoban-llm-agent!")
    parent_dir = Path.cwd()

    data_file = parent_dir / "dataset/human_demos/4_1.txt"
    # model_name = "meta-llama/Llama-3.2-3B-Instruct"    
    # model_name = "Qwen/Qwen2.5-7B-Instruct"
    # model_name = "Qwen/Qwen2.5-7B"
    # model_name = "Qwen/Qwen3-32B"
    # model_name = "meta-llama/Llama-3.2-3B"
    # model_name = "google/gemma-3-27b-it"
    # model_name = "openai/gpt-oss-20b"
    # model_name = "openai/gpt-oss-120b"

    # model_name = "gpt-4o-mini" 
    # model_name = "google/gemini-2.5-flash"
    # model_name = "deepseek-ai/DeepSeek-R1-0528-Turbo"
    # model_name = "claude-sonnet-4-5"

    initial_map = game_environment.SokobanGame(data_file)

    print("Initial Map:")
    print(str(initial_map.serialize_map()))

    agent_state = state_initiator.initiate_state(initial_map, model_name)
    graph = sokoban_graph.build_sokoban_graph()
    app = graph.compile()
    app.invoke(agent_state, config={"recursion_limit": 50})


if __name__ == "__main__":
    main()
