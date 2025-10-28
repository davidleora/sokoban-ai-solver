
from src.graph.nodes.state import SokobanState

def validate_state(state: SokobanState) -> SokobanState:
    """
    Validate the running status and decide next node.
    Two-level retry system:
    1. Inner loop: Further prompt LLM up to max_further_prompts times with current state
    2. Outer loop: Restart from scratch up to max_iterations times
    
    Sets 'next_step' in state to indicate routing decision.
    """
    
    if state['status'] == "need_further_prompt":
        # Try to continue from current state with further prompt
        if state['current_further_prompt'] < state['max_further_prompts']:
            state['current_further_prompt'] += 1
            print(f"💬 Further prompting LLM (attempt {state['current_further_prompt']}/{state['max_further_prompts']}) - continuing from current state...")
            state['next_step'] = "go_further_prompt"
            return state
        else:
            # All further prompts exhausted, mark iteration as failed
            print(f"❌ Max further prompts ({state['max_further_prompts']}) reached for iteration {state['current_iteration']}.")
            state['status'] = "unsolved"  # Mark this iteration as failed
            # Fall through to check outer iterations
    
    if state['status'] in ["unsolved", "empty"]:
        # Check if we can retry from scratch
        if state['current_iteration'] >= state['max_iterations']:
            print(f"❌ Could not find solution after {state['max_iterations']} iteration(s).")
            state['next_step'] = "end"
            return state
        else:
            print(f"🔄 Iteration {state['current_iteration']} failed. Restarting from scratch...")
            state['current_further_prompt'] = 0  # Reset further prompt counter for new iteration
            state['next_step'] = "go_moves"
            return state
    
    elif state['status'] == "success":
        print(f"✅ Puzzle solved!")
        state['next_step'] = "success"
        return state
