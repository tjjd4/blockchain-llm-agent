import os
from autogen import LLMConfig

from .base_agent import BaseAgent
from src.utils.prompt import LLM_PROMPTS
from src.utils.config import Config
ollama_llm_config = LLMConfig(
    model= "mistral-nemo:12b-instruct-2407-q2_K",
    api_type= "ollama",
)

openai_llm_config = LLMConfig(
    model= "gpt-4o-mini",
    api_type= "openai",
    api_key= Config.OPENAI_API_KEY,
)

class IntentAgent(BaseAgent):
    def __init__(self, **kwargs):
        system_message = LLM_PROMPTS["INTENT_AGENT_PROMPT"]
        super().__init__(name="IntentAgent", system_message=system_message, llm_config=ollama_llm_config, **kwargs)
