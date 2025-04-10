import asyncio
from autogen import UserProxyAgent, GroupChat, GroupChatManager, LLMConfig

from app.agent.mcp_assistant_agent import MCPAssistantAgent
from app.agent.mcp_executor_agent import MCPExecutorAgent

llm_config = LLMConfig(
    config_list=[
        {
            "model": "llama3.2:latest",
            "api_type": "ollama",
        }
    ]
)
    

async def main():
    assistant_agent = MCPAssistantAgent(
        name="mcp_assistant_agent",
        system_message="""
        You are a crypto expert. 
        You can use the tools provided to you to answer questions.
        You are given a message and you need to determine if it is a crypto related question. 
        If it is, you should use the tools to answer the question. 
        If it is not, you should say that you do not know.
        """,
        llm_config=llm_config,
        mcp_server_command="npx",
        mcp_server_args=["-y","@mcpdotdirect/evm-mcp-server"],
        env={
            "WALLET_PRIVATE_KEY": "0x51897b64e85c3f714bba707e867914295a1377a7463a9dae8ea6a8b914246319",
            "RPC_PROVIDER_URL": "https://eth-mainnet.public.blastapi.io"
        }
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
        llm_config=llm_config,
        mcp_server_command="node",
        mcp_server_args=["app/mcp/goat-model-context-protocol/build/evm.js"],
        env={
            "WALLET_PRIVATE_KEY": "0x51897b64e85c3f714bba707e867914295a1377a7463a9dae8ea6a8b914246319",
            "RPC_PROVIDER_URL": "https://eth-mainnet.public.blastapi.io"
        }
    )
    await executor_agent.initialize()

    user = UserProxyAgent(
        name = "user", 
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

    result = user.run(
        manager=manager,
        recipient=manager,
        message="How many USDC does 0x860201656ece07cb8d5133dd704bb6f10a09fe93 have?",
        tools=assistant_agent.tools,
        max_turns=4)

    result.process()
    print(result.summary)


if __name__ == "__main__":
    asyncio.run(main())
