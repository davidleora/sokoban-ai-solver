from src.graph.nodes.state import SokobanState
# from src.graph.llm.client_openai import LLM_client as LLM_client_openai
# from src.graph.llm.client_claude import LLM_client as LLM_client_claude
from src.graph.llm.client import LLM_client as LLM_client_local
import time

def llm_moves(state: SokobanState) -> SokobanState:
    """
    Generates moves (sequence of primitive moves)
    based on the current map.
    """
    state['current_iteration'] = state['current_iteration'] + 1
    state['moves'] = ""
    state['status'] = "continue"
    state['visited_map_state'] = []
    print("Start the trial:", state['current_iteration'])
    llm_client = LLM_client_local(state['model_name'])
    
    # Call the model and record the execution time, and model name
    start_time = time.perf_counter()
    plan_chunk = llm_client.query_llm_for_moves(state["map"].convert_current_state_to_map()) 
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    state['records']['model'] = llm_client.model_name
    state['records']['time'] = execution_time
    
    print(f"plan_chunk:\n\n{plan_chunk}")
    print()
    plan_result = llm_client.post_processing_moves(plan_chunk)
    
    if plan_result:
        state['moves'] = plan_result
    return state
