import logging
from autogen import UserProxyAgent, ConversableAgent
from autogen.agentchat import initiate_group_chat, a_initiate_group_chat
from autogen.agentchat.group.patterns import AutoPattern
from autogen.agentchat.group import (
    ContextVariables, ReplyResult, AgentTarget,
    OnCondition, StringLLMCondition,
    OnContextCondition, ExpressionContextCondition, ContextExpression,
    RevertToUserTarget
)

from .intent_agent import IntentAgent
from .planner_agent import PlannerAgent
from .blockchain_agent import BlockchainAgent
from src.utils.config import Config

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self):
        # self.intent_agent = IntentAgent()
        self.planner_agent = PlannerAgent()
        self.blockchain_agent = BlockchainAgent()
        self.user_agent = UserProxyAgent(
            name="user_agent",
            human_input_mode="NEVER",
            code_execution_config = {
                "use_docker": False
            },
        )

    # def classify(self, user_input: str):
    #     intent = self.intent_agent.execute_function("classify", user_input)
    #     return intent

    async def run(self, user_input: str):
        llm_config = Config.get_anthropic_llm_config()
        # server_params = StdioServerParameters(
        #     command="node",  # The command to run the server
        #     args=[
        #         "src/mcp/evm-mcp-server/build/index.js",
        #     ],
        # )
        await self.planner_agent.register_mcp_tools_for_llm("node", ["src/mcp/evm-mcp-server/build/index.js"], mode="stdio")
        await self.blockchain_agent.register_mcp_tools_for_execution("node", ["src/mcp/evm-mcp-server/build/index.js"], mode="stdio")
        logger.info("[Orchestrator] MCP tools registered")
            
        pattern = AutoPattern(
            initial_agent=self.planner_agent,
            agents=[
                self.planner_agent,
                self.blockchain_agent
            ],
            user_agent=self.user_agent,
            group_manager_args = {"llm_config": llm_config},
        )
    
        result, context, last_agent = await a_initiate_group_chat(
            pattern=pattern,
            messages=user_input,
            max_rounds=7
        )

        return result, context, last_agent