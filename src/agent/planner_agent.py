from autogen import LLMConfig

from .base_ag2_agent import BaseAgent
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


class PlannerAgent(BaseAgent):
    def __init__(self, **kwargs):
        system_message = LLM_PROMPTS["PLANNER_AGENT_PROMPT"]
        super().__init__(name="PlannerAgent", system_message=system_message, llm_config=ollama_llm_config, **kwargs)
        
        @self.register_for_llm(description="Plan the sequence of actions to execute the user's intent")
        def plan(self) -> list[str]:
            """
            Plan the sequence of actions to execute the user's intent.
            """
            return []
    
