from src.graph.nodes.state import SokobanState
import copy

def execute_moves(state: SokobanState) -> SokobanState:
    """
    Executes the moves issued by plan.
    """

    tmp_map = copy.deepcopy(state['map'])
    total_moves = ""
    
    # Check if LLM provided any moves
    if state['moves'] == "":
        state['status'] = "empty"
        return state
    
    # Execute each move from the LLM's plan
    for move_idx, move in enumerate(state['moves'], 1):

        # Try to execute the move
        if tmp_map.makeMove(move):
            total_moves += move
            cur_map_state = tmp_map.serialize_map()
            
            # Check if puzzle is solved
            if tmp_map.isLevelFinished():
                state['status'] = "success"
                state['visited_map_state'].append(cur_map_state)
                state['solution'] = total_moves
                return state 

            # Check for repeated/cyclic states (LLM got stuck in a loop)
            if cur_map_state in state['visited_map_state']:
                print(f"⚠️  Move #{move_idx} ({move}): Detected repeated state - LLM created a cycle")
            
            state['visited_map_state'].append(cur_map_state)

        else:
            print(f"❌ Move #{move_idx} ({move}): Failed - continuing...")
            continue

    # All moves processed but puzzle not solved
    # Update map to current position so further prompt sees the updated state
    state['map'] = tmp_map
    state['status'] = "need_further_prompt"
    state["moves"] = "" # Clear moves for next iteration
    return state
