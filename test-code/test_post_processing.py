#!/usr/bin/env python3
"""
Simple test script for post_processing_moves function.
Usage: python test_post_processing.py <input_file.txt>
"""

import sys


def post_processing_moves(response):
    """Exact copy from src/graph/llm/client.py lines 173-188"""
    steps = ""
    plan = response.strip().split('\n')

    for i, step in enumerate(plan):

        if "<U>" in step or "**U**" in step:
            steps += "U"
        elif "<D>" in step or "**D**" in step:
            steps += "D"
        elif "<L>" in step or "**L**" in step:
            steps += "L"
        elif "<R>" in step or "**R**" in step:
            steps += "R"

    return steps


def post_processing_moves_verbose(response):
    """Extended version that shows which line each move is detected from"""
    steps = ""
    detections = []
    plan = response.strip().split('\n')

    for line_num, step in enumerate(plan, start=1):
        found = None
        
        if "<U>" in step or "**U**" in step:
            steps += "U"
            found = "U"
        elif "<D>" in step or "**D**" in step:
            steps += "D"
            found = "D"
        elif "<L>" in step or "**L**" in step:
            steps += "L"
            found = "L"
        elif "<R>" in step or "**R**" in step:
            steps += "R"
            found = "R"
        
        if found:
            # Truncate long lines for display
            display_line = step if len(step) <= 100 else step[:97] + "..."
            detections.append((line_num, found, display_line))

    return steps, detections


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_post_processing.py <input_file.txt>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    with open(input_file, 'r') as f:
        response = f.read()
    
    moves, detections = post_processing_moves_verbose(response)
    
    print(f"Total moves extracted: {len(moves)}")
    print(f"Move sequence: {moves}\n")
    
    print("="*80)
    print("Detection details (line number → move → line content):")
    print("="*80)
    
    for line_num, direction, content in detections:
        print(f"Line {line_num:4d}: <{direction}> | {content}")
    
    print("="*80)
