import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration manager for the application."""
    
    @staticmethod
    def get_env(key: str, default: Optional[str] = None) -> str:
        """Get environment variable with optional default value."""
        value = os.getenv(key, default)
        if value is None:
            raise ValueError(f"Environment variable {key} is not set")
        return value
    
    # API Keys
    OPENAI_API_KEY: str = get_env("OPENAI_API_KEY")
    EVM_NETWORK: str = get_env("EVM_NETWORK", "mainnet")
    # Blockchain Configuration
    ETHEREUM_RPC_URL: str = get_env("ETHEREUM_RPC_URL", "https://eth.llamarpc.com")
    
    @classmethod
    def validate(cls) -> None:
        """Validate required configuration."""
        # Validate EVM network
        valid_networks = ["mainnet", "testnet"]
        if cls.EVM_NETWORK not in valid_networks:
            raise ValueError(f"EVM_NETWORK must be one of {valid_networks}")
