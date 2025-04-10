import asyncio
from autogen import UserProxyAgent, GroupChat, GroupChatManager, LLMConfig, AssistantAgent
from autogen.agentchat import assistant_agent
from autogen.tools import tool

from app.agent.math_agent import MathAgent

llm_config = LLMConfig(
    config_list=[
        {
            "model": "llama3.2:latest",
            "api_type": "ollama",
        }
    ]
)
    

async def main():
    math_agent = MathAgent()

    assistant_agent = AssistantAgent(
        name="assistant_agent",
        system_message="""
        You are a smart math assistant.
        Use tools registered in self as needed. Do not guess. Respond clearly.
        You can execute tools by calling them.
        """,
        llm_config=llm_config,
        code_execution_config={
            "use_docker": False
        },
    )

    user = UserProxyAgent(
        name = "user", 
        human_input_mode = "NEVER",
        code_execution_config = {
            "use_docker": False
        },
    )

    # when using run(), if recipient is None or not provided,
    # it will default generate a executor to execute the tools specified in `tools` parameter
    result = math_agent.run(
        message="Is 4302237510 even?", 
        tools=math_agent.tools,
        max_turns=4)

    result.process()
    print(result.summary)


if __name__ == "__main__":
    asyncio.run(main())
