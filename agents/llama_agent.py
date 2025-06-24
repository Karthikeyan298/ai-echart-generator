from langchain_community.llms.ollama import Ollama
from agents.agent import Agent
import os

class LlamaAgent(Agent):
    """
    LlamaAgent class for interacting with the Llama model.
    Inherits from the Agent class.
    """

    def __init__(self, model_name, base_prompt, stream=False):
        url = os.getenv("LLAMA_URL")
        if not url:
            raise ValueError("LLAMA_URL environment variable is not set.")
        self.model = Ollama(base_url=url, model=model_name)
        super().__init__(self.model, base_prompt, stream)


    def invoke(self, input: str):
        """
        Invoke the Llama model with the given query.

        :param query: The query to be processed by the Llama model.
        :return: The response from the Llama model.
        """
        input = self.base_prompt + " " + str(input)
        return self.model.invoke(input, stream=self.stream)
