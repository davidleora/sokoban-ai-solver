from src.graph import sokoban_graph
from src.sokoban import game_environment
from pathlib import Path
from src.graph.nodes import state_initiator
from src.graph.llm.client import LLM_client as LLM_client_local
import time


def run_single_file(data_file: Path, model_name: str, llm_client):
    """Run solver on a single file with pre-loaded model"""
    print(f"\n{'='*80}")
    print(f"📂 Processing: {data_file.name}")
    print(f"{'='*80}\n")
    
    try:
        initial_map = game_environment.SokobanGame(data_file)
        print("Initial Map:")
        print(str(initial_map.serialize_map()))

        agent_state = state_initiator.initiate_state(initial_map, model_name)
        agent_state['llm_client'] = llm_client  # Pass pre-loaded client
        graph = sokoban_graph.build_sokoban_graph()
        app = graph.compile()
        app.invoke(agent_state, config={"recursion_limit": 50})
        
        print(f"✅ Completed: {data_file.name}\n")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {data_file.name}: {e}\n")
        return False


def main():
    parent_dir = Path.cwd()
    dataset_dir = parent_dir / "dataset/human_demos"
    model_name = "openai/gpt-oss-20b"
    
    # Get all txt files and sort them
    txt_files = sorted(dataset_dir.glob("*.txt"))
    
    print(f"🎯 Found {len(txt_files)} files to process")
    print(f"🤖 Using model: {model_name}")
    
    # ⭐ LOAD MODEL ONCE HERE - HUGE PERFORMANCE BOOST! ⭐
    print(f"\n🔄 Loading model {model_name} into GPU (this takes ~5 seconds)...")
    llm_client = LLM_client_local(model_name)
    print(f"✅ Model loaded and ready! Now processing all {len(txt_files)} files...\n")
    
    start_time = time.time()
    success_count = 0
    fail_count = 0
    
    for idx, txt_file in enumerate(txt_files, 1):
        print(f"\n{'#'*80}")
        print(f"Progress: {idx}/{len(txt_files)}")
        print(f"{'#'*80}")
        
        result = run_single_file(txt_file, model_name, llm_client)
        if result:
            success_count += 1
        else:
            fail_count += 1
        
        # Small delay between runs
        time.sleep(1)
    
    total_time = time.time() - start_time
    
    print(f"\n{'='*80}")
    print(f"🏁 BATCH PROCESSING COMPLETE")
    print(f"{'='*80}")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {fail_count}")
    print(f"⏱️  Total time: {total_time/60:.2f} minutes")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()