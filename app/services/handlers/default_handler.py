import json
from typing import Dict, Any

from .base_handler import BaseHandler

class DefaultHandler(BaseHandler):
    def __init__(self):
        super().__init__()

    def handle_classification(self, response: str) -> str:
        return response.strip() if response else "Unknown"

    def handle_transfer_intent(self, response: str) -> Dict[str, Any]:
        try:
            intent = json.loads(response.strip())
            if not isinstance(intent, dict):
                print(f"[DefaultHandler] Unexpected parsed type: {type(intent)}. Expected dict.")
                raise Exception
        except Exception:
            print("[DefaultHandler] JSON parse failed.")
            return {}

        try:
            chain = intent["chain"]
            token = intent["token"]
            intent["token"] = self.token_contracts["transfer_token_contracts"][chain][token]
        except Exception:
            print("[DefaultHandler] Invalid token mapping.")
            intent["token"] = None

        return intent
