from typing import Dict, Any
from ollama import Client, ChatResponse

from app.services.base_ai_service import BaseAIService
from app.services.handlers.handler_factory import HandlerFactory
from app.utils.messages import (
    get_classify_system_messages,
    get_convert_system_messages,
    get_swap_schema_message,
    get_transfer_schema_message,
    get_instruction_message,
)

class OllamaService(BaseAIService):

    def __init__(self, model_name: str):
        super().__init__(model_name=model_name)
        self.model = Client(
            host='http://localhost:11434',
        )
        self.response_handler = HandlerFactory.get_handler(model_name)

    async def classify_transaction(self, user_input: str) -> str:
        classify_system_message = get_classify_system_messages()
        swap_schema_message = get_swap_schema_message()
        transfer_schema_message = get_transfer_schema_message()
        user_message = {
            "role": "user",
            "content": user_input,
        }

        response: ChatResponse = self.model.chat(
            model=self.model_name,
            messages=[
                classify_system_message,
                swap_schema_message,
                transfer_schema_message,
                user_message,
            ],
        )
        print("[OllamaService] Transfer intent response: ", response.message.content)

        if response.message.content == None:
            return "Unknown"
        return self.response_handler.handle_classification(response.message.content)

    async def convert_transfer_intent(self, user_input: str) -> Dict[str, Any]:
        convert_system_message = get_convert_system_messages()
        transfer_schema_message = get_transfer_schema_message()
        instruction_message = get_instruction_message()
        user_message = {
            "role": "user",
            "content": user_input,
        }

        response: ChatResponse = self.model.chat(
            model=self.model_name,
            messages=[
                convert_system_message,
                transfer_schema_message,
                instruction_message,
                user_message,
            ],
        )
        print("[OllamaService] Transfer intent response: ", response.message.content)

        if response.message.content == None:
            return {}

        # Extract and interpret the last message from the completion
        return self.response_handler.handle_transfer_intent(response.message.content.strip())
