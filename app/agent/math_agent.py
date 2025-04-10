from autogen import ConversableAgent

class MathAgent(ConversableAgent):
    def __init__(self):
        super().__init__(
            name="math_agent",
            system_message="""
            You are a smart math assistant.
            Use tools registered in self as needed. Do not guess. Respond clearly.
            You can execute tools by calling them.
            """,
            llm_config={
                "config_list": [
                    {
                        "model": "llama3.2:latest",
                        "api_type": "ollama",
                    }
                ]
            },
            code_execution_config={
                "use_docker": False
            },
        )

        @self.register_for_llm(name="is_even", description="Return '1' if the number is even, else is odd and return '0'")
        @self.register_for_execution(name="is_even", description="Return '1' if the number is even, else is odd and return '0'")
        def is_even(n: int) -> str:
            return "1" if n % 2 == 0 else "0"
