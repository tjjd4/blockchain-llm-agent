from typing import Dict, List

from .base_agent import BaseAgent

class PlannerAgent(BaseAgent):
    def __init__(self, **kwargs):
        system_message = (
            "You are a blockchain planning agent. Your job is to receive a structured intent object and convert it into a sequence of blockchain operation steps.\n"
            "You must output a list of steps. Each step is a dictionary with a 'step' key and optional parameters.\n"
            "Supported steps: check_balance, validate_address, send_transaction, fetch_transaction_history, read_contract.\n"
            "Do not include any explanations. Only return the list."
        )
        super().__init__(name="PlannerAgent", system_message=system_message, **kwargs)