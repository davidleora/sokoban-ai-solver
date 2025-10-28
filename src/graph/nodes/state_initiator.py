from src.graph.nodes.state import SokobanState
from src.sokoban import game_environment

def initiate_state(initial_map: game_environment.SokobanGame, model_name: str) -> SokobanState:

    return {
        "map": initial_map,                    
        "status": "continue",                         
        "moves": "",                       
        "solution": "",
        "max_iterations": 2,
        "max_further_prompts": 3,
        "current_further_prompt": 0,
        "visited_map_state": [],
        "current_iteration": 0,
        "records": {},
        "model_name": model_name,
        "next_step": "",
        "llm_client": None
    }


