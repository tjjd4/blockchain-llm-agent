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
    user_input = "Do I have 10 DAI on Optimism? My address is 0x1234567890123456789012345678901234567890, I want to send 10 DAI to peter, his address is peter.eth"
    user_intent = Intent(
        intent="User wants to check their DAI balance on Optimism and intends to send 10 DAI to a specified address.",
        chain="Optimism",
    )
    
    result = await planner_agent.plan(user_input, user_intent)
    print("Result: ", result)

    
if __name__ == "__main__":
    asyncio.run(test_planner_agent_plan())