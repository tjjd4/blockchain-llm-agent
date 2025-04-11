from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client

from autogen import LLMConfig
from autogen.agentchat import AssistantAgent
from autogen.mcp import create_toolkit
import asyncio


llm_config = LLMConfig(
    config_list=[
        {
            "model": "mistral-nemo:12b-instruct-2407-q2_K",
            "api_type": "ollama",
        }
    ]
)

async def create_toolkit_and_run(session: ClientSession) -> None:
    # Create a toolkit with available MCP tools
    toolkit = await create_toolkit(session=session)
    agent = AssistantAgent(name="assistant", llm_config=llm_config)
    # Register MCP tools with the agent
    toolkit.register_for_llm(agent)

    # Make a request using the MCP tool
    result = await agent.a_run(
        message="""How much USDC does address 0x860201656ece07cb8d5133dd704bb6f10a09fe93 have?""",
        tools=toolkit.tools,
        max_turns=2,
        user_input=False,
    )
    await result.process()

async def main():
    server_params = StdioServerParameters(
        command="node",
        args=["app/mcp/evm-mcp-server/build/index.js"],
    )
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        # Initialize the connection
        await session.initialize()
        await create_toolkit_and_run(session)

if __name__ == "__main__":
    asyncio.run(main())