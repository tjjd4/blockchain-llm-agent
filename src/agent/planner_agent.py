from autogen import LLMConfig, UserProxyAgent
import logging

from .base_ag2_agent import BaseAgent
from src.utils.prompt import LLM_PROMPTS
from src.utils.config import Config
from src.utils.pydantic_types import Intent

logger = logging.getLogger(__name__)

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


    async def plan(self, user_input: str, intent: Intent) -> list[str]:
        user_agent = UserProxyAgent(
            name="user",
            human_input_mode="NEVER",
            code_execution_config = {
                "use_docker": False
            },
        )

        await self.register_mcp_tools(mcp_cmd="node", mcp_args=["src/mcp/evm-mcp-server/build/index.js"], agents=[user_agent])
        await self.register_mcp_tools(mcp_cmd="node", mcp_args=["src/mcp/bitcoin-mcp/build/cli.js"], agents=[user_agent])
        logger.info("[PlannerAgent] MCP tools registered")
        result = user_agent.initiate_chat(
            recipient=self,
            message=f"User input: {user_input}\nIntent: {intent}",
            max_turns=2,
        )
        return result.summary
    
