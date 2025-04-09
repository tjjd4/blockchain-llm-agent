from web3 import Web3
from typing import Optional, Dict, List, Any

class BlockchainTxnTool:
    def __init__(self, rpc_url: str, private_key: str):
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))

        if not self.web3.is_connected():
            raise ConnectionError(f"Failed to connect to blockchain RPC: {rpc_url}")

        self.account = self.web3.eth.account.from_key(private_key)
        self.address = self.account.address

    def send_transaction(
        self,
        from_address: str,
        to_address: str,
        value: float = 0,
        data: Optional[bytes] = None,
        gas: Optional[int] = None,
        gas_price_gwei: Optional[float] = None,
        nonce: Optional[int] = None,
    ) -> Optional[str]:
        try:
            to_checksum = self.web3.to_checksum_address(to_address)
            gas_price = (
                self.web3.to_wei(gas_price_gwei, 'gwei') if gas_price_gwei
                else self.web3.eth.gas_price
            )
            nonce = nonce or self.web3.eth.get_transaction_count(self.address)

            txn = {
                'to': to_checksum,
                'value': self.web3.to_wei(value, 'ether'),
                'gas': gas or 100_000,
                'gasPrice': gas_price,
                'nonce': nonce,
                'data': data or b'',
            }

            signed_txn = self.account.sign_transaction(txn)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            return tx_hash.hex()
        except Exception as e:
            print(f"[BlockchainTxnTool] send_transaction error: {e}")
            return None

    def get_address(self) -> str:
        return self.address

    def is_valid_address(self, address: str) -> bool:
        try:
            self.web3.to_checksum_address(address)
            return True
        except ValueError:
            return False

    def encode_msg_data(
        self,
        abi: List[Dict[str, Any]],
        function_name: str,
        args: List[Any]
    ) -> Optional[bytes]:
        """
        Returns calldata (msg.data) as hex string for a given ABI function + args.
        No transaction is sent.
        """
        try:
            contract = self.web3.eth.contract(abi=abi)
            return contract.encode_abi(fn_name=function_name, args=args)
        except Exception as e:
            print(f"[BlockchainTxnTool] encode_msg_data error: {e}")
            return None
