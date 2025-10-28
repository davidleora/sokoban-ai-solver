# src/graph/state.py
from typing import TypedDict, List
from src.sokoban.game_environment import SokobanGame

class SokobanState(TypedDict, total=False):
    map: SokobanGame                    # Current board
    status: str                         # "success" | "unsolved" | "empty" | "need_further_prompt"
    moves: str                          # All executed primitive moves (L/R/U/D)
    solution: str                       # solution steps (exclude those repetitive cyclic steps)
    max_iterations: int                 # max allowed iteration times (outer retry - restart from scratch)
    max_further_prompts: int            # max allowed further prompts per iteration (inner retry - continue from current)
    current_further_prompt: int         # current further prompt count within iteration
    visited_map_state: List[str]        # visited maps (serialized)
    current_iteration: int              # current iteration index
    records: dict                       # running metadata recording
    model_name: str                     # the LLM model name
    next_step: str                      # routing decision set by validator
    
