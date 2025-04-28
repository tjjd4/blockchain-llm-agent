import logging
from autogen import UserProxyAgent, ConversableAgent
from autogen.agentchat import initiate_group_chat
from autogen.agentchat.group.patterns import AutoPattern
from autogen.agentchat.group import (
    ContextVariables, ReplyResult, AgentTarget,
    OnCondition, StringLLMCondition,
    OnContextCondition, ExpressionContextCondition, ContextExpression,
    RevertToUserTarget
)
from autogen.tools.tool import tool
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client

from autogen import LLMConfig
from autogen.agentchat import AssistantAgent
from autogen.mcp import create_toolkit

from .intent_agent import IntentAgent
from .planner_agent import PlannerAgent
from .blockchain_agent import BlockchainAgent
from src.utils.config import Config

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self):
        self.intent_agent = IntentAgent()
        self.planner_agent = PlannerAgent()
        self.blockchain_agent = BlockchainAgent()
        self.user_agent = UserProxyAgent(
            name="user_agent",
            human_input_mode="NEVER",
            code_execution_config = {
                "use_docker": False
            },
        )
        self.executor_agent = ConversableAgent(
            name="executor_agent",
            human_input_mode="NEVER",
        )

    def classify(self, user_input: str):
        intent = self.intent_agent.execute_function("classify", user_input)
        return intent

    async def run(self, user_input: str):
        llm_config = Config.get_ollama_llm_config()

        server_params = StdioServerParameters(
            command="node",  # The command to run the server
            args=[
                "src/mcp/evm-mcp-server/build/index.js",
            ],
        )

        async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            toolkit = await create_toolkit(session=session)
            toolkit.register_for_llm(self.planner_agent)
            toolkit.register_for_execution(self.blockchain_agent)
            logger.info("[Orchestrator] MCP tools registered")
            pattern = AutoPattern(
                initial_agent=self.planner_agent,
                agents=[
                    self.planner_agent,
                    self.executor_agent,
                ],
                user_agent=self.user_agent,
                group_manager_args = {"llm_config": llm_config},
                
            )
        
            result, context, last_agent = initiate_group_chat(
                pattern=pattern,
                messages=user_input,
                max_rounds=4
            )
            return result, context, last_agent