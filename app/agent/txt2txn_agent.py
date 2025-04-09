import json
from typing import Dict, Any
from app.agent.base_agent import BaseAgent
from app.services.base_ai_service import BaseAIService
from app.services.blockchain_service import BlockchainService

class Txt2TxnAgent(BaseAgent):
    def __init__(self, ai_service: BaseAIService, blockchain_service: BlockchainService):
        self.ai_service = ai_service
        self.blockchain_service = blockchain_service

    async def run(self, user_input: str) -> str:
        txn_type_response = await self.ai_service.classify_transaction(user_input)
        print("[Txt2TxnAgent] Txn Type Response: ",txn_type_response)

        txn_type = self.get_valid_txn_type(txn_type_response)
        txn_response = {}

        if txn_type == 0:
            print("[Txt2TxnAgent] Invalid transaction type. Please try again.")
        elif txn_type == 1:
            txn_response = await self.ai_service.convert_transfer_intent(user_input)
            print("[Txt2TxnAgent] Txn Type Response: ",txn_response)
            is_sufficient = await self.has_sufficient_balance(txn_response)
            txn_response["check"] = is_sufficient
        elif txn_type == 2:
            print("[Txt2TxnAgent] Swap not supported yet. Please try again later.")
        txn = self.get_valid_txn(txn_response)
        return json.dumps(txn)

    async def has_sufficient_balance(self, txn_response: Dict[str, Any]) -> bool:
        from_address = txn_response.get("fromAddress")
        amount = txn_response.get("amount")

        if not from_address or not amount:
            print("[Txt2TxnAgent] Missing 'from' or 'amount' in txn_response.")
            return False

        balance = await self.blockchain_service.get_balance(from_address)
        print(f"[Txt2TxnAgent] Balance for {from_address}: {balance}")

        if balance is None:
            return False

        try:
            return float(balance) >= float(amount)
        except ValueError:
            return False

    def get_valid_txn_type(self, response: str) -> int:
        valid_responses = ["0", "1", "2"]
        found = None

        for valid in valid_responses:
            # Count the occurrences of each valid response in the string
            if response.count(valid) == 1:
                if found is not None:
                    # If another valid response was already found, return 0
                    return 0
                found = int(valid)  # Store the found valid response

        return found if found is not None else 0

    def get_valid_txn(self, response: Dict[str, Any]) -> Dict[str, Any]:
        return response
