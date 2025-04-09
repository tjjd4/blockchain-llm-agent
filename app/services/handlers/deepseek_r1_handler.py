from typing import Any
from app.services.handlers.default_handler import DefaultHandler

class DeepSeekR1Handler(DefaultHandler):
    def handle_classification(self, response: str) -> str:
        print("[DeepSeekR1Handler] Custom classification logic.")
        response = self.remove_think_tag_from_deepseek(response)
        return super().handle_classification(response[-1])

    def handle_transfer_intent(self, response: str) -> Any:
        print("[DeepSeekR1Handler] Custom transfer intent logic.")
        response = self.remove_think_tag_from_deepseek(response)
        response = self.remove_json_tag_from_deepseek(response)
        print("[DeepSeekR1Handler] After truncate response: ", response)
        return super().handle_transfer_intent(response)

    def remove_think_tag_from_deepseek(self, text: str) -> str:
        start = text.find('<think>')
        end = text.find('</think>')

        if start == -1 or end == -1:
            return text.strip()

        result = text[:start] + text[end + len('</think>'):]

        return result.strip()

    def remove_json_tag_from_deepseek(self, text: str) -> str:
        start = text.find('```json')
        if start == -1:
            return text.strip()

        end = text.find('```', start + len('```json'))
        if end == -1:
            return text[start + len('```json'):].strip()

        return text[start + len('```json'):end].strip()
