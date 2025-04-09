import argparse
import sys
from app.tools.blockchain_query_tool import BlockchainQueryTool


def main():
    parser = argparse.ArgumentParser(description="Test Script for BlockchainDataTool")
    parser.add_argument("--rpc-url", required=True, help="區塊鏈 RPC 連線 URL (e.g. Infura / Alchemy / local node)")
    parser.add_argument("--address", required=True, help="要查詢餘額的地址 (0x...)")
    parser.add_argument("--tx-hash", required=True, help="要查詢的交易雜湊 (0x...)")
    args = parser.parse_args()

    # 初始化實體
    try:
        tool = BlockchainQueryTool(rpc_url=args.rpc_url)
        print(f"V : 成功連線到區塊鏈: {args.rpc_url}")
    except ConnectionError as e:
        print("X : 建構 BlockchainDataTool 時連線失敗: ", e)
        sys.exit(1)

    # 測試 get_balance
    print(f"\n=== 測試 get_balance({args.address}) ===")
    balance = tool.get_balance(args.address)
    if balance is not None:
        print(f"V : 取得餘額成功: Address {args.address} Balance = {balance} ETH")
    else:
        print("❌ 無法取得餘額或發生錯誤")

    # 測試 get_transaction_by_hash
    print(f"\n=== 測試 get_transaction_by_hash({args.tx_hash}) ===")
    tx_info = tool.get_transaction_by_hash(args.tx_hash)
    if tx_info is not None:
        print(f"V : 取得交易成功: \n{tx_info}")
    else:
        print("❌ : 查無此交易或發生錯誤")

    # 測試 get_transaction_receipt
    print(f"\n=== 測試 get_transaction_receipt({args.tx_hash}) ===")
    tx_receipt = tool.get_transaction_receipt(args.tx_hash)
    if tx_receipt is not None:
        print(f"V : 取得交易回執成功: \n{tx_receipt}")
    else:
        print("❌ : 取得交易回執失敗或發生錯誤")


if __name__ == "__main__":
    main()
