# Project Introduction

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

Run `python3 main.py`

Waiting for the LLM generate solution for the chosen sokoban puzzle. <br>
You could take a look at the running records at `/result/running_record.csv` <br>
Each running step could be found in the file `/result/result_map_<data_file_name>.txt`. <br><br>
