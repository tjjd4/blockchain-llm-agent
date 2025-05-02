import asyncio
import json
from autogen import UserProxyAgent

from src.agent.planner_agent import PlannerAgent
from src.utils.pydantic_types import Intent
def is_termination_msg(message: dict) -> bool:
        try:
            data = json.loads(message["content"])
            return isinstance(data, dict) and "intent" in data
        except Exception:
            return False

async def test_planner_agent_plan():
    planner_agent = PlannerAgent()
    user_input = "Do I have 10 DAI on Optimism? My address is 0x1234567890123456789012345678901234567890, I want to send 10 DAI to peter, his address is peter.eth"
    
    result = await planner_agent.plan(user_input)
    print("Result: ", result)

    
if __name__ == "__main__":
    asyncio.run(test_planner_agent_plan())