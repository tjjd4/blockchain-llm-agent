# Blockchain LLM Agent

A blockchain-focused LLM agent system built with AutoGen framework.

## Project Structure

```
src/
├── agent/         # Agent implementations
├── utils/         # Utility functions
├── mcp/           # Multi-agent communication protocol
├── schemas/       # Data schemas and models
└── contracts/     # Smart contract interfaces
```

## Overview

This project implements an LLM-powered agent system for blockchain interactions. It uses the AutoGen framework to create conversational agents that can interact with blockchain networks and smart contracts.

## Prerequisites

### Python Version
- Python >= 3.12 and < 4.0

### Package Managers (Choose one)
- [pip](https://pip.pypa.io/) - Python's default package manager
- [poetry](https://python-poetry.org/) - Modern dependency management and packaging
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver (recommended)

### Required Modules
- [Ollama](https://ollama.ai/) - Local LLM server for running models

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/tjjd4/blockchain-llm-agent.git
```
### 2. Install dependencies (requirements to be added)
```bash
cd path/to/blockchain-llm-agent/

pip install . # This command will build package itself
uv pip install -r pyproject.toml  # using uv
poetry install                    # using poetry
```
### 3. Configure your environment variables
```bash
cp .env.sample .env
```
Fill the enviroment variables!

### 4. Start ollama server
Open a new terminal and activate ollama
```bash
ollama serve
```
If you want to use any model haven't been downloaded before,
Open a new terminal and download the model by typing:
```bash
ollama pull <MODEL_NAME>
```
replace <MODEL_NAME> with the model you want to use, search on [Ollama](https://ollama.ai/)


### 4. Run the application
```bash
python main.py         # using python/pip
uv run python main.py  # using uv
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
