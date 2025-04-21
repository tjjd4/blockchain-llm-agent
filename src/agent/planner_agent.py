from typing import List
from autogen import LLMConfig, UserProxyAgent, ConversableAgent
from autogen.mcp import create_toolkit
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client

from .base_ag2_agent import BaseAgent
from src.utils.prompt import LLM_PROMPTS
from src.utils.config import Config
from src.utils.pydantic_types import Intent

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

    async def register_mcp_tools(self, mcp_cmd: str, mcp_args: List[dict], agents: List[ConversableAgent]):
        server_params = StdioServerParameters(
            command=mcp_cmd,
            args=mcp_args,
        )

        async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
            await session.initialize()
            toolkit = await create_toolkit(session)
            toolkit.register_for_llm(self)
            for agent in agents:
                toolkit.register_for_execution(agent)


    async def plan(self, user_input: str, intent: Intent) -> list[str]:
        user_agent = UserProxyAgent(
            name="user",
            human_input_mode="NEVER",
            code_execution_config = {
                "use_docker": False
            },
        )

        await self.register_mcp_tools(mcp_cmd="node", mcp_args=["src/mcp/evm-mcp-server/build/index.js"], agents=[user_agent])
        print("MCP tools registered")
        result = user_agent.initiate_chat(
            recipient=self,
            message=f"User input: {user_input}\nIntent: {intent}",
            max_turns=2,
        )
        return result.summary
    
