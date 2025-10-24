# Project Introduction

This project uses LLM to generate solution for sokoban puzzle game. It also use LangGraph to manage the workflow.

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

### 3. Configure API Keys

1. Set API_Key at [www.deepinfra.com](https://deepinfra.com/), and copy the API key to `config.py`
2. Set API_key at [www.comet.com](https://comet.com/), and copy the API key to `config.py`

### 4. Run the Project

Run `python3 main.py`

Waiting for the LLM generate solution for the chosen sokoban puzzle. <br>
You could take a look at the running records at `/result/running_record.csv` <br>
Each running step could be found in the file `/result/result_map_<data_file_name>.txt`. <br><br>
One example is: <br>
<img src="result/running_result.png" width = 250>
<br><br>
You could also check the LLM query input/output logging in Opik: <br><br>
<img src="result/opik_logging.png" width = 800>

<br><br>
Check the generated GIF under the folder `/result`.<br><br>
<img src="result/result_map_4_1.gif" width = 250>

## TODO:

. Use Javascript Game Engine Phaser to render the game UI.
