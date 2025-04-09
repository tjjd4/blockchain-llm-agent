import asyncio
from autogen import UserProxyAgent, GroupChat, GroupChatManager

from app.agent.mcp_assistant_agent import MCPAssistantAgent

async def main():
    assistant_agent = MCPAssistantAgent(
        name="mcp_agent",
        system_message="""
        You are a crypto expert. 
        You can use the tools provided to you to answer questions.
        You are given a message and you need to determine if it is a crypto related question. 
        If it is, you should use the tools to answer the question. 
        If it is not, you should say that you do not know.
        """,
        llm_config={
            "config_list": [
                {
                    "model": "llama3.2:latest",
                    "api_type": "ollama",
                }
            ]
        },
        mcp_server_command="node",
        mcp_server_args=["app/mcp/goat-model-context-protocol/build/evm.js"],
        env={
            "WALLET_PRIVATE_KEY": "0x51897b64e85c3f714bba707e867914295a1377a7463a9dae8ea6a8b914246319",
            "RPC_PROVIDER_URL": "https://eth-mainnet.public.blastapi.io"
        }
    )
    await assistant_agent.initialize()

    user = UserProxyAgent(
        name = "user", 
        human_input_mode = "NEVER",
        code_execution_config = {
            "use_docker": False
        },
    )

    # print("🔗 Ready! Ask questions like: How many USDC does 0xabc... have?")
    await user.a_initiate_chat(
        recipient=assistant_agent,
        message="How many USDC does 0x860201656ece07cb8d5133dd704bb6f10a09fe93 have?", 
        max_turns=2)

if __name__ == "__main__":
    asyncio.run(main())
