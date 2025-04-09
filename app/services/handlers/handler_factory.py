from app.services.handlers.base_handler import BaseHandler
from app.services.handlers.default_handler import DefaultHandler
from app.services.handlers.deepseek_r1_handler import DeepSeekR1Handler

class HandlerFactory:
    _handlers = {
        "deepseek-r1": DeepSeekR1Handler,
    }

    @classmethod
    def get_handler(cls, model_name: str) -> BaseHandler:
        return cls._handlers.get(model_name.lower(), DefaultHandler)()
