import os
from uu import Error
from dotenv import load_dotenv
from typing import Optional
from autogen import LLMConfig

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
    OPENAI_API_KEY: str = get_env("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = get_env("ANTHROPIC_API_KEY", "")
    EVM_NETWORK: str = get_env("EVM_NETWORK", "mainnet")
    # Blockchain Configuration
    ETHEREUM_RPC_URL: str = get_env("ETHEREUM_RPC_URL", "https://eth.llamarpc.com")
    USE_API: str = get_env("USE_API", "ollama")
    
    @classmethod
    def validate(cls) -> None:
        """Validate required configuration."""
        # Validate EVM network
        valid_networks = ["mainnet", "testnet"]
        if cls.EVM_NETWORK not in valid_networks:
            raise ValueError(f"EVM_NETWORK must be one of {valid_networks}")

    @classmethod
    def get_ollama_llm_config(cls):
        ollama_llm_config = LLMConfig(
            model= "mistral-nemo:12b-instruct-2407-q2_K",
            api_type= "ollama",
        )
        return ollama_llm_config

    @classmethod
    def get_openai_llm_config(cls):
        if cls.OPENAI_API_KEY == "":
            raise 
        openai_llm_config = LLMConfig(
            model= "gpt-4o-mini",
            api_type= "openai",
            api_key= cls.OPENAI_API_KEY,
        )
        return openai_llm_config

    @classmethod
    def get_anthropic_llm_config(cls):
        if cls.ANTHROPIC_API_KEY == "":
            raise 
        anthropic_llm_config = LLMConfig(
            model= "claude-3-7-sonnet-20250219",
            api_type= "anthropic",
            api_key= cls.ANTHROPIC_API_KEY,
        )
        return anthropic_llm_config

    @classmethod
    def get_llm_config(cls):
        if cls.USE_API == "ollama":
            return Config.get_ollama_llm_config()
        elif cls.USE_API == "openai":
            return Config.get_openai_llm_config()
        elif cls.USE_API == "anthropic":
            return Config.get_anthropic_llm_config()
        else:
            raise ValueError(f"Invalid API: {cls.USE_API}")
    