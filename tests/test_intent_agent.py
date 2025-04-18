import asyncio
import json

from src.agent.intent_agent import IntentAgent

def is_termination_msg(message: dict) -> bool:
        try:
            data = json.loads(message["content"])
            return isinstance(data, dict) and "intent" in data
        except Exception:
            return False

async def test_intent_agent_transfer():
    intent_agent = IntentAgent()
    result = intent_agent.extract_intent("Do I have 10 DAI on Optimism? My address is 0x1234567890123456789012345678901234567890, I want to send 10 DAI to peter, his address is peter.eth")
    print("Result: ", result)

if __name__ == "__main__":
    asyncio.run(test_intent_agent_transfer())