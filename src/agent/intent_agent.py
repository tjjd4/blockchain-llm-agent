from autogen import LLMConfig, UserProxyAgent

from .base_ag2_agent import BaseAgent
from src.utils.prompt import LLM_PROMPTS
from src.utils.config import Config
from src.utils.pydantic_types import Intent

ollama_llm_config = Config.get_ollama_llm_config()
ollama_llm_config.response_format = Intent

openai_llm_config = Config.get_openai_llm_config()
openai_llm_config.response_format = Intent

class IntentAgent(BaseAgent):
    def __init__(self, **kwargs):
        system_message = LLM_PROMPTS["INTENT_AGENT_PROMPT"]
        super().__init__(name="IntentAgent", system_message=system_message, llm_config=ollama_llm_config, **kwargs)

    def extract_intent(self, user_input: str) -> Intent:
        user_agent = UserProxyAgent(
            name="user",
            human_input_mode="NEVER",
            code_execution_config = {
                "use_docker": False
            },
        )

        result = user_agent.initiate_chat(
            recipient=self,
            message=user_input,
            max_turns=2,
        )
        return Intent.model_validate_json(result.summary)