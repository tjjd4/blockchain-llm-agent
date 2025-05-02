from autogen import UserProxyAgent
import logging

from .base_ag2_agent import BaseAgent

logger = logging.getLogger(__name__)

class UserAgent(BaseAgent, UserProxyAgent):
    def __init__(self, **kwargs):
        UserProxyAgent.__init__(self, **kwargs)
    