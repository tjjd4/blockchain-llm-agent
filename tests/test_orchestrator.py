import asyncio
import json

from src.agent.orchestrator import Orchestrator

async def test_orchestrator():
    orchestrator = Orchestrator()
    user_input = "Do I have 10 DAI on Optimism? My address is 0x1234567890123456789012345678901234567890, I want to send 10 DAI to peter, his address is peter.eth"
    
    result, context, last_agent = await orchestrator.run(user_input)
    print("Result: ", result.summary)

if __name__ == "__main__":
    asyncio.run(test_orchestrator())