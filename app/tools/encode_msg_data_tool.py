class EncodeMsgDataTool:
    name = "encode_msg_data"
    description = "Encode msg.data for any smart contract function input data using args."

    def run(self, data: Dict[str, Any]) -> Optional[str]:
        signature = data["signature"]  # e.g., "transfer(address,uint256)"
        args = data["args"]
        try:
            selector = keccak(text=signature)[:4]
            types = signature[signature.find("(")+1:signature.find(")")].split(",")
            encoded_args = encode_abi(types, args)
            return "0x" + (selector + encoded_args).hex()
        except Exception as e:
            print(f"[EncodeMsgDataTool] Error encoding msg.data: {e}")
            return None
