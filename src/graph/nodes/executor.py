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
    for move in state['moves']:

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
                idx = state['visited_map_state'].index(cur_map_state)
                total_moves = total_moves[: idx+1]
                state['visited_map_state'] = state['visited_map_state'][: idx+1]
                print(f"⚠️  Detected repeated state - LLM created a cycle")
                continue  # Skip to next move
            else:
                state['visited_map_state'].append(cur_map_state)

        else:
            print(f"Move '{move}' failed, continuing...")
            continue

    state['status'] = "unsolved"
    state["moves"] = "" # Clear moves for next iteration
    return state
