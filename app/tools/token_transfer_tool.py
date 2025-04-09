from typing import Optional
from blockchain_txn_tool import BlockchainTxnTool

ERC20_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    },
    {
        "name": "transfer",
        "type": "function",
        "stateMutability": "nonpayable",
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "outputs": [{"name": "", "type": "bool"}]
    }
]

class Erc20TokenTransferTool(BlockchainTxnTool):
    def __init__(self, rpc_url: str, private_key: str):
        super().__init__(rpc_url, private_key)

    def run(self, data: dict) -> Optional[str]:
        token_address = data["token"]
        amount_float = data["amount"]
        chain = data["chain"]
        from_address = data["fromAddress"]
        to_address = data["toAddress"]

        if not self.is_valid_address(token_address):
            print(f"[SimpleTokenTransferTool] Unsupported Token: {token_address}")
            return None

        if self.get_address().lower() != from_address.lower():
            print(f"[SimpleTokenTransferTool] Mismatch fromAddress vs private key address\n {self.get_address()} vs {from_address}")
            return None

        try:
            token_contract = self.web3.eth.contract(address=self.web3.to_checksum_address(token_address), abi=ERC20_ABI)
            decimals = token_contract.functions.decimals().call()
        except Exception as e:
            print(f"[SimpleTokenTransferTool] Failed to fetch token decimals: {e}")
            decimals = 18  # fallback

        amount = int(amount_float * (10 ** decimals))
        msg_data = self.encode_msg_data(abi=ERC20_ABI, function_name="transfer", args=[to_address, amount])

        return self.send_transaction(
            from_address=from_address,
            to_address=token_address,
            data=msg_data,
            value=0
        )
