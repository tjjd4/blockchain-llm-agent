from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAIService(ABC):
    def __init__(self, model_name: str):
        self._model_name = model_name

    @property
    def model_name(self) -> str:
        return self._model_name

    @abstractmethod
    async def classify_transaction(self, user_input: str) -> str:
        """
        Return '1' for transfer, '2' for swap, and '0' for neither.
        """
        pass

    @abstractmethod
    async def convert_transfer_intent(self, user_input: str) -> Dict[str, Any]:
        pass
