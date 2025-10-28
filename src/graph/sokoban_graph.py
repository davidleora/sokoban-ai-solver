from langgraph.graph import StateGraph, END, START
from src.graph.nodes import executor, llm_caller, result_displayer, validator, state
from functools import lru_cache

def route_based_on_status(state):
    return state.get('next_step', 'end')

@lru_cache(maxsize=1)
def build_sokoban_graph():
    g = StateGraph(state.SokobanState)

    g.add_node("moves", llm_caller.llm_moves)
    g.add_node("executor", executor.execute_moves)
    g.add_node("validator", validator.validate_state)
    g.add_node("generate_result", result_displayer.generate_result)

    g.add_edge(START, "moves")
    g.add_edge("moves", "executor")
    g.add_edge("executor", "validator")

    g.add_conditional_edges("validator", route_based_on_status,
        {
            "success": "generate_result",
            "go_moves": "moves",
            "go_further_prompt": "moves",
            "end": "generate_result",
        }
        )
    
    g.add_edge("generate_result", END)
    return g 

