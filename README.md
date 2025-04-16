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


## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/tjjd4/blockchain-llm-agent.git
```
### 2. Install dependencies (requirements to be added)
```bash
cd path/to/blockchain-llm-agent/

pip install .     # using python/pip
uv pip install .  # using uv
poetry install    #using poetry
```
### 3. Configure your environment variables
```bash
cp .env.sample .env
```
Fill the enviroment variables!

### 4. Run the application
```bash
python main.py         # using python/pip
uv run python main.py  # using uv
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
