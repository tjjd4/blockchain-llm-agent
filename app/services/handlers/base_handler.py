from abc import ABC, abstractmethod
from typing import Dict, Any

from app.utils.contracts import get_token_contracts

class BaseHandler(ABC):


    def __init__(self):
        self.token_contracts = get_token_contracts()

    @abstractmethod
    def handle_classification(self, response: str) -> str:
        pass

    @abstractmethod
    def handle_transfer_intent(self, response: str) -> Dict[str, Any]:
        pass
