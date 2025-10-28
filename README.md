# Project Introduction [RESEARCH IN PROGRESS]

This project uses LLM to generate solution for sokoban puzzle game. It also use LangGraph to manage the workflow.

## System Requirements

⚠️ **This project is Linux-only** and requires a CUDA-enabled environment.

### Hardware Requirements
- **GPU:** NVIDIA GPU with Turing architecture or newer (RTX 20 series, T4, or better)

### Software Requirements
- **Operating System:** Linux
- **CUDA Toolkit:** Version 11.7 to 12.6
  - Recommended: CUDA 11.7 - 12.3 (most tested versions)
  - Download from [NVIDIA CUDA Downloads](https://developer.nvidia.com/cuda-downloads)
- **Python:** 3.11 or higher
- **GPU Drivers:** Compatible NVIDIA drivers for your CUDA version

### Key Dependencies
- **bitsandbytes** (>=0.48.1): For model quantization and optimization
- **torch**: Will be installed automatically with CUDA support

## Setup Instructions

### 1. Clone the Repository

Clone the repository with submodules (to include the `boxoban-levels` dataset):

```bash
git clone --recursive https://github.com/davidleora/sokoban-ai-solver.git
cd sokoban-ai-solver
```

Or if you already cloned without `--recursive`, initialize the submodules:

```bash
git submodule update --init --recursive
```

### 2. Set Up Python Environment

1. Ensure that your computer installs "uv" package
2. At the project root path, type `uv sync` (this will create the `.venv` folder automatically)
3. Activate the virtual environment: `source .venv/bin/activate`

### 3. Run the Project

#### Single Puzzle Mode
```bash
python main.py dataset/human_demos/1_0.txt
```

#### Batch Processing (All 107 Puzzles)
```bash
python batch_run.py
```
**Note:** The model is loaded once and reused across all files for optimal performance.

## Results

- **GIF animations**: `result/<model_name>/result_map_*.gif`
- **CSV logs**: `result/running_record.csv`

## Configuration

Edit model settings in `main.py` or `batch_run.py`:
- `model_name`: LLM model to use (default: `openai/gpt-oss-20b`)
- `max_iterations`: Fresh restart attempts (default: 2)
- `max_further_prompts`: Continuation attempts per iteration (default: 5)
