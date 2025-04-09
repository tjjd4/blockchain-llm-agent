import streamlit as st
import asyncio
import os
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from autogen.mcp import create_toolkit
from app.agent.mcp_agent import MCPAssistantAgent

st.set_page_config(page_title="MCP Math Agent")
st.title("🧠 MCP Math Assistant")

user_input = st.text_input("What do you want to calculate?")

if "response" not in st.session_state:
    st.session_state["response"] = ""

async def main(user_input):
    assistant = MCPAssistantAgent(
        name="math_agent",
        system_message="""
        You are a smart math assistant.
        You have access to:
        - MCP tools: add(a, b), multiply(a, b)
        - A local tool: is_even(n)
        Use tools as needed. Do not guess. Respond clearly.
        """,
        llm_config={
            "config_list": [
                {
                    "model": "llama3.2:latest",
                    "api_type": "ollama",
                }
            ]
        },
        mcp_server_command="uv",
        mcp_server_args=["run", "python", "app/mcp/math_mcp_server.py"]
    )

    response = await assistant.a_run(
        message=user_input,
        max_turns=2,
        user_input=False,
    )
    await response.process()
    return response.summary

if user_input and st.button("Run Agent"):
    st.session_state.response = asyncio.run(main(user_input))

if st.session_state.response:
    st.subheader("Response")
    st.markdown(st.session_state.response)
