from .intent_agent import IntentAgent
from .planner_agent import PlannerAgent

class Orchestrator:
    def __init__(self):
        self.intent_agent = IntentAgent()
        self.planner = PlannerAgent()

    def run(self, user_input: str):
        intent = self.intent_agent.execute_function("classify", user_input)
        return intent