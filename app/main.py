import os
import uvicorn
from fastapi import FastAPI, Body
import dotenv

from app.agent.txt2txn_agent import Txt2TxnAgent
from app.services.ollama_service import OllamaService
from app.services.blockchain_service import BlockchainService

dotenv.load_dotenv()
ETH_RPC_URL = os.getenv("ETH_RPC_URL","https://eth.llamarpc.com")

app = FastAPI(title="Blockchain + AI Agent Demo", version="1.0.0")

ai_service = OllamaService(model_name="deepseek-r1")
blockchain_service = BlockchainService(rpc_url=ETH_RPC_URL)

txt2txn_agent = Txt2TxnAgent(ai_service=ai_service, blockchain_service=blockchain_service)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Blockchain-AI Agent API"}

@app.post("/txt2txn_agent/run")
async def agent_run(data: dict = Body(...)):
    user_input = data.get("input", "")
    print("[Main] User Input: ", user_input)
    result = await txt2txn_agent.run(user_input)
    return {"Result": result}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
