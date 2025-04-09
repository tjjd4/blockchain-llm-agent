import os
import json
from typing import Dict

CONTRACT_DIR = os.path.join("app", "contracts")

def get_token_contracts() -> Dict[str, str]:
    contract_path = os.path.join(CONTRACT_DIR, "token_contracts.json")
    with open(contract_path, "r", encoding="utf-8") as f:
        token_contracts = json.load(f)

        return token_contracts
