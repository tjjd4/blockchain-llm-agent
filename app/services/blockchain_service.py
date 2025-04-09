from typing import Optional

from app.tools.blockchain_query_tool import BlockchainQueryTool

class BlockchainService:
    def __init__(self, rpc_url: str):
        self.tool = BlockchainQueryTool(rpc_url)

    async def get_balance(self, address: str) -> Optional[float]:
        return self.tool.get_balance_from_str(address)

    async def get_transaction(self, tx_hash: str) -> Optional[dict]:
        return self.tool.get_transaction_by_hash(tx_hash)

    async def get_receipt(self, tx_hash: str) -> Optional[dict]:
        return self.tool.get_transaction_receipt(tx_hash)
