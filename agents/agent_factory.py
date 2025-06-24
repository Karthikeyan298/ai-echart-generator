from enum import Enum

from agents.llama_agent import LlamaAgent
from agents.openai_agent import OpenAiAgent


class AgentType(Enum):
    """
    Enum for different types of agents.
    """
    LLAMA = 'llama'
    OPENAI = 'openai'

class AgentFactory:
    """
    Factory class for creating agents.
    """

    @staticmethod
    def create_agent(agent_type: AgentType, base_prompt, model_name, **kwargs):
        if agent_type ==  AgentType.LLAMA:
            return LlamaAgent(model_name=model_name, base_prompt=base_prompt)
        elif agent_type == AgentType.OPENAI:
            return OpenAiAgent(model_name=model_name, base_prompt=base_prompt)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")