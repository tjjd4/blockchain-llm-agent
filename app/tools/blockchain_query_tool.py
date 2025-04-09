from web3 import Web3
from eth_typing import Address as EthAddress, ChecksumAddress as EthChecksumAddress
from web3.types import ENS
from typing import Optional, Dict, Any
from hexbytes import HexBytes

class BlockchainQueryTool:
    def __init__(self, rpc_url: str):
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))

        if not self.web3.is_connected():
            raise ConnectionError(f"Failed to connect to blockchain RPC: {rpc_url}")

    def get_balance(self, address: EthAddress | EthChecksumAddress | ENS) -> Optional[float]:
        try:
            if self.web3.is_address(address) and not self.web3.is_checksum_address(address):
                address = self.web3.to_checksum_address(address)

                address = self.web3.to_checksum_address(address)
            balance_wei = self.web3.eth.get_balance(address)
            balance_eth = self.web3.from_wei(balance_wei, 'ether')
            return float(balance_eth)
        except Exception as e:
            print(f"[BlockchainDataTool] get_balance error: {e}")
            return None

    def get_balance_from_str(self, address_str: str) -> Optional[float]:
            if not self.web3.is_address(address_str):
                print(f"[BlockchainDataTool] Invalid address: {address_str}")
                return None
            checksum_address = self.web3.to_checksum_address(address_str)
            return self.get_balance(checksum_address)

    def get_transaction_by_hash(self, tx_hash_str: str) -> Optional[Dict[str, Any]]:
        if not self.is_valid_tx_hash(tx_hash_str):
            print(f"[BlockchainDataTool] Invalid tx hash format: {tx_hash_str}")
            return None
        try:
            tx_hash = HexBytes(tx_hash_str)
            tx = self.web3.eth.get_transaction(tx_hash)
            return dict(tx)
        except Exception as e:
            print(f"[BlockchainDataTool] get_transaction_by_hash error: {e}")
            return None

    def get_transaction_receipt(self, tx_hash_str: str) -> Optional[Dict[str, Any]]:
        if not self.is_valid_tx_hash(tx_hash_str):
            print(f"[BlockchainDataTool] Invalid tx hash format: {tx_hash_str}")
            return None
        try:
            tx_hash = HexBytes(tx_hash_str)
            receipt = self.web3.eth.get_transaction_receipt(tx_hash)
            return dict(receipt)
        except Exception as e:
            print(f"[BlockchainDataTool] get_transaction_receipt error: {e}")
            return None

    def is_valid_tx_hash(self, tx_hash_str: str) -> bool:
        return (
            isinstance(tx_hash_str, str)
            and tx_hash_str.startswith("0x")
            and len(tx_hash_str) == 66
        )
