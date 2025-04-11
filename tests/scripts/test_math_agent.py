import asyncio
from autogen import UserProxyAgent, GroupChat, GroupChatManager, LLMConfig, AssistantAgent
from autogen.agentchat import assistant_agent
from autogen.tools import tool

from app.agent.math_agent import MathAgent

llm_config = LLMConfig(
    config_list=[
        {
            "model": "mistral-nemo:12b-instruct-2407-q2_K",
            "api_type": "ollama",
        }
    ]
)
    

async def main():
    math_agent = MathAgent(
        name="math_agent",
        llm_config=llm_config
    )

    # when using run(), if recipient is None or not provided,
    # it will default generate a executor to execute the tools specified in `tools` parameter
    result = math_agent.run(
        message="8466546 + 103294394?", 
        tools=math_agent.tools,
        max_turns=4)

    result.process()
    print(result.summary)


if __name__ == "__main__":
    asyncio.run(main())
