import asyncio
import json
from autogen import UserProxyAgent

from src.agent.planner_agent import PlannerAgent

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
    planner_agent = PlannerAgent()

    intent_json = {
        "intent": "User wants to check their DAI balance on Optimism and intends to send 10 DAI to a specified address.",
        "info": {
            "token": "DAI",
            "amount": 10,
            "to": "peter.eth",
            "chain": "Optimism",
            "from": "0x1234567890123456789012345678901234567890"
        }
    }

    result = user.initiate_chat(
        recipient=planner_agent,
        message=json.dumps(intent_json),
        max_turns=6,
    )
    print(result.summary)

if __name__ == "__main__":
    asyncio.run(test_intent_agent_transfer())