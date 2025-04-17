import asyncio
import json
from autogen import UserProxyAgent

from src.agent.intent_agent import IntentAgent

def is_termination_msg(message: dict) -> bool:
        try:
            data = json.loads(message["content"])
            return isinstance(data, dict) and "intent" in data
        except Exception:
            return False

async def test_intent_agent_transfer():
    user = UserProxyAgent(
        name="user", 
        max_consecutive_auto_reply=0,
        human_input_mode="NEVER",
        code_execution_config = {
            "use_docker": False
        },
        is_termination_msg=is_termination_msg,

    )
    intent_agent = IntentAgent()

    result = user.initiate_chat(
        recipient=intent_agent,
        message="Do I have 10 DAI on Optimism? My address is 0x1234567890123456789012345678901234567890, I want to send 10 DAI to peter, his address is peter.eth",
        max_turns=6,
    )
    print(result.summary)

if __name__ == "__main__":
    asyncio.run(test_intent_agent_transfer())