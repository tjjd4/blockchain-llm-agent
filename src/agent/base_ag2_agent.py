from typing import List, Literal
from autogen import ConversableAgent
from autogen.mcp import create_toolkit
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client

class BaseAgent(ConversableAgent):

    def __init__(self, name: str, system_message: str, **kwargs):
        super().__init__(name=name, system_message=system_message, **kwargs)

    async def register_mcp_tools(self, mcp_cmd: str, mcp_args: List[dict], agents: List[ConversableAgent], mode: Literal["stdio", "sse"] = "stdio"):
        server_params = StdioServerParameters(
            command=mcp_cmd,
            args=mcp_args,
        )

        if mode == "stdio":
            async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
                await session.initialize()
                toolkit = await create_toolkit(session)
                toolkit.register_for_llm(self)
                for agent in agents:
                    toolkit.register_for_execution(agent)
        elif mode == "sse":
            async with sse_client(server_params) as (read, write), ClientSession(read, write) as session:
                await session.initialize()
                toolkit = await create_toolkit(session)
                toolkit.register_for_llm(self)
                for agent in agents:
                    toolkit.register_for_execution(agent)
        else:
            raise ValueError(f"Invalid mode: {mode}")
