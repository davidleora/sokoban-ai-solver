from src.graph.nodes.state import SokobanState
from src.graph.llm.client_openai import LLM_client as LLM_client_openai
from src.graph.llm.client_claude import LLM_client as LLM_client_claude
from src.graph.llm.client import LLM_client as LLM_client_local
import time

def llm_moves(state: SokobanState) -> SokobanState:
    """
    Generates moves based on current map.
    Called for:
    1. Fresh iteration start (current_further_prompt == 0)
    2. Further prompt/continuation (current_further_prompt > 0)
    """
    
    # Determine if this is a fresh start or further prompt
    is_fresh_start = state.get('current_further_prompt', 0) == 0
    
    if is_fresh_start:
        # New iteration - reset everything
        state['current_iteration'] = state['current_iteration'] + 1
        state['visited_map_state'] = []
        state['current_further_prompt'] = 0
        print(f"\n{'='*70}")
        print(f"🆕 ITERATION {state['current_iteration']}/{state['max_iterations']} - Starting fresh")
        print(f"{'='*70}")
    else:
        # Further prompt - continue from current state
        print(f"\n{'~'*70}")
        print(f"💬 FURTHER PROMPT {state['current_further_prompt']}/{state['max_further_prompts']} (Iteration {state['current_iteration']}) - Continuing")
        print(f"{'~'*70}")
    
    state['moves'] = ""
    state['status'] = "continue"
    
    # Select appropriate client based on model name
    model_name = state['model_name']
    if "gpt" in model_name.lower() or "openai" in model_name.lower():
        llm_client = LLM_client_openai(model_name)
    elif "claude" in model_name.lower() or "anthropic" in model_name.lower():
        llm_client = LLM_client_claude(model_name)
    else:
        llm_client = LLM_client_local(model_name)
    
    # Build prompt based on context
    current_map_list = state["map"].convert_current_state_to_map()
    current_map_str = state["map"].serialize_map()
    
    # Display the current map being sent to LLM
    print(f"\n📍 Current map state being sent to LLM:", flush=True)
    print(current_map_str, flush=True)
    print(flush=True)
    
    if is_fresh_start:
        # Fresh start - just give the initial map
        user_prompt = current_map_list
    else:
        # Further prompt - give context that we're continuing
        print(f"ℹ️  Context: {len(state['visited_map_state'])} moves have been executed so far.", flush=True)
        print(flush=True)
        user_prompt = f"""You've made {len(state['visited_map_state'])} moves so far but haven't solved it yet.

Current map state:
{current_map_list}

Continue from this state to solve the puzzle. Provide the next moves."""
    
    # Call the model
    start_time = time.perf_counter()
    plan_chunk = llm_client.query_llm_for_moves(user_prompt)
    end_time = time.perf_counter()
    
    execution_time = end_time - start_time
    state['records']['model'] = llm_client.model_name
    # Accumulate time across further prompts within the same iteration
    if is_fresh_start:
        state['records']['time'] = execution_time
    else:
        state['records']['time'] = state['records'].get('time', 0) + execution_time
    
    print(f"\nPlan chunk:\n{plan_chunk}\n")
    plan_result = llm_client.post_processing_moves(plan_chunk)
    
    if plan_result:
        state['moves'] = plan_result
        print(f"Extracted moves: {plan_result[:50]}{'...' if len(plan_result) > 50 else ''}")
    
    return state
