from autogen import AssistantAgent

class MathAgent(AssistantAgent):
    def __init__(self, toolkit):
        super().__init__(
            name="math_agent",
            system_message="""
            You are a smart math assistant.
            You have access to:
            - MCP tools: add(a, b), multiply(a, b)
            - A local tool: is_even(n)
            Use tools as needed. Do not guess. Respond clearly.
            """,
            llm_config={
                "config_list": [
                    {
                        "model": "llama3.2:latest",
                        "api_type": "ollama",
                    }
                ]
            },
        )

        toolkit.register_for_llm(self)

        @self.register_for_llm(name="is_even", description="Return '1' if the number is even, else '0'")
        def is_even(n: int) -> str:
            return "1" if n % 2 == 0 else "0"
