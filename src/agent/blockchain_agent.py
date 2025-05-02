from autogen import LLMConfig, UserProxyAgent
import logging

from .base_ag2_agent import BaseAgent
from src.utils.prompt import LLM_PROMPTS
from src.utils.config import Config
from src.utils.pydantic_types import Intent

logger = logging.getLogger(__name__)

llm_config = Config.get_llm_config()


class BlockchainAgent(BaseAgent):
    def __init__(self, **kwargs):
        system_message = LLM_PROMPTS["BLOCKCHAIN_AGENT_PROMPT"]
        super().__init__(name="BlockchainAgent", system_message=system_message, llm_config=llm_config, **kwargs)
    
