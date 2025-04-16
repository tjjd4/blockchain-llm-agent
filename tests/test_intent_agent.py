import asyncio
import json
from autogen import UserProxyAgent

from app.agent.intent_agent import IntentAgent

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
        human_input_mode="TERMINATE",
        code_execution_config = {
            "use_docker": False
        },
    )
    intent_agent = IntentAgent(
        is_termination_msg=is_termination_msg
    )

    result = user.initiate_chat(
        recipient=intent_agent,
        message="Do I have 1000 USDC on Optimism?",
        max_turns=6,
    )
    print(result.summary)

if __name__ == "__main__":
    asyncio.run(test_intent_agent_transfer())