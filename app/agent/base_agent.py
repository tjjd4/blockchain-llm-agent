# app/agent/base_agent.py

from abc import abstractmethod
from autogen import ConversableAgent

class BaseAgent(ConversableAgent):
    @abstractmethod
    async def run(self, user_input: str) -> str:
        """子類別需實作: 處理來自使用者或系統的 input"""
        pass