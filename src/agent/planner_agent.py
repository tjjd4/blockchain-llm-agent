from autogen import UserProxyAgent
import logging

from .base_ag2_agent import BaseAgent
from .user_agent import UserAgent
from src.utils.prompt import LLM_PROMPTS
from src.utils.config import Config

logger = logging.getLogger(__name__)

ollama_llm_config = Config.get_ollama_llm_config()
openai_llm_config = Config.get_openai_llm_config()
anthropic_llm_config = Config.get_anthropic_llm_config()

class PlannerAgent(BaseAgent):
    def __init__(self, **kwargs):
        system_message = LLM_PROMPTS["PLANNER_AGENT_PROMPT"]
        super().__init__(name="PlannerAgent", system_message=system_message, llm_config=anthropic_llm_config, **kwargs)


    async def plan(self, user_input: str) -> list[str]:
        user_agent = UserAgent(
            name="user_agent",
            human_input_mode="NEVER",
            code_execution_config = {
                "use_docker": False
            },
        )

        await self.register_mcp_tools_for_llm(mcp_cmd="node", mcp_args=["src/mcp/evm-mcp-server/build/index.js"], mode="stdio")
        await user_agent.register_mcp_tools_for_execution(mcp_cmd="node", mcp_args=["src/mcp/evm-mcp-server/build/index.js"], mode="stdio")

        logger.info("[PlannerAgent] MCP tools registered")
        result = await user_agent.a_initiate_chat(
            recipient=self,
            message=f"User input: {user_input}",
            max_turns=4,
        )
        return result.summary
    
