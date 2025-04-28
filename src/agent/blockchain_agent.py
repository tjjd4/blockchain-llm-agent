from autogen import LLMConfig, UserProxyAgent
import logging

from .base_ag2_agent import BaseAgent
from src.utils.prompt import LLM_PROMPTS
from src.utils.config import Config
from src.utils.pydantic_types import Intent

logger = logging.getLogger(__name__)

# ollama_llm_config = LLMConfig(
#     model= "mistral-nemo:12b-instruct-2407-q2_K",
#     api_type= "ollama",
# )

# openai_llm_config = LLMConfig(
#     model= "gpt-4o-mini",
#     api_type= "openai",
#     api_key= Config.OPENAI_API_KEY,
# )


class BlockchainAgent(BaseAgent):
    def __init__(self, **kwargs):
        system_message = LLM_PROMPTS["BLOCKCHAIN_AGENT_PROMPT"]
        super().__init__(name="BlockchainAgent", system_message=system_message, **kwargs)
    
