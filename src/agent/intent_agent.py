import json
from autogen import LLMConfig

from .base_agent import BaseAgent
from src.utils.prompt import LLM_PROMPTS

llm_config = LLMConfig(
    config_list=[
        {
            "model": "mistral-nemo:12b-instruct-2407-q2_K",
            "api_type": "ollama",
        }
    ]
)

class IntentAgent(BaseAgent):
    def __init__(self, **kwargs):
        system_message = LLM_PROMPTS["INTENT_AGENT_PROMPT"]
        super().__init__(name="IntentAgent", system_message=system_message, llm_config=llm_config, **kwargs)
