from pydantic import BaseModel, Field

class Intent(BaseModel):
    intent: str = Field(..., description="A one-sentence summary of the user's intent from the input")
    chain: str = Field(description="The operating blockchain name, e.g., Ethereum, Polygon, Optimism", default="Ethereum")
