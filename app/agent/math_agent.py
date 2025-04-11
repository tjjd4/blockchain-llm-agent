from autogen import ConversableAgent

class MathAgent(ConversableAgent):
    def __init__(
        self,
        name: str,
        system_message: str = """
            You are a smart math assistant.
            Use tools registered in self as needed. Do not guess. Respond clearly.
            You can execute tools by calling them.
            """,
        **kwargs,
    ):
        super().__init__(
            name=name,
            system_message=system_message,
            code_execution_config={
                "use_docker": False
            },
            **kwargs,
        )

        @self.register_for_llm(name="is_even", description="Return '1' if the number is even, else is odd and return '0'")
        # @self.register_for_execution(name="is_even", description="Return '1' if the number is even, else is odd and return '0'")
        def is_even(n: int) -> str:
            return "1" if n % 2 == 0 else "0"

        @self.register_for_llm(name="add", description="Return the sum of two numbers")
        # @self.register_for_execution(name="add", description="Return the sum of two numbers")
        def add(a: int, b: int) -> int:
            return a + b
