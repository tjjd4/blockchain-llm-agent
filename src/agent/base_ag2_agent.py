from abc import abstractmethod
from autogen import ConversableAgent

class BaseAgent(ConversableAgent):

    def __init__(self, name: str, system_message: str, **kwargs):
        super().__init__(name=name, system_message=system_message, **kwargs)