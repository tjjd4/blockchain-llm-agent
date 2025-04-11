import asyncio
from autogen import UserProxyAgent, GroupChat, GroupChatManager, LLMConfig

from app.agent.mcp_assistant_agent import MCPAssistantAgent
from app.agent.mcp_executor_agent import MCPExecutorAgent
from app.utils.messages import get_mcp_system_message

llm_config = LLMConfig(
    config_list=[
        {
            "model": "mistral-nemo:12b-instruct-2407-q2_K",
            "api_type": "ollama",
        }
    ]
)
    

async def main():
    assistant_agent = MCPAssistantAgent(
        name="mcp_assistant_agent",
        system_message=get_mcp_system_message()['content'],
        llm_config=llm_config,
        mcp_server_command="node",
        mcp_server_args=["app/mcp/evm-mcp-server/build/index.js"],
    )
    await assistant_agent.initialize()


    executor_agent = MCPExecutorAgent(
        name="mcp_executor_agent",
        system_message="""
        You are a crypto expert and the executor of mcp tools.
        You will recieve the parameters of a mcp call.
        You will use the tools provided to you to execute the call.
        You will return the result of the call.
        """,
        mcp_server_command="node",
        mcp_server_args=["app/mcp/evm-mcp-server/build/index.js"],
    )
    await executor_agent.initialize()

    user_agent = UserProxyAgent(
        name = "user_agent", 
        human_input_mode = "NEVER",
        code_execution_config = {
            "use_docker": False
        },
    )
    

    groupchat = GroupChat(
        agents=[assistant_agent, executor_agent],
        speaker_selection_method='round_robin',
        max_round=5
    )

    manager = GroupChatManager(groupchat=groupchat)

    result = user_agent.run(
        manager=manager,
        recipient=manager,
        message="How much USDC does 0x860201656ece07cb8d5133dd704bb6f10a09fe93 have?",
        max_turns=4,
        user_input=False
    )

    result.process()
    print(result.summary)


if __name__ == "__main__":
    asyncio.run(main())
