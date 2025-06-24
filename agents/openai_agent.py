import os

from langchain_openai import ChatOpenAI

from agents.agent import Agent


class OpenAiAgent(Agent):
    def __init__(self, model_name: str, base_prompt: str, stream: bool = False):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        self.model = ChatOpenAI(model=model_name, max_tokens=400, streaming=stream, disable_streaming=True)
        super().__init__(self.model, base_prompt, stream)

    def invoke(self, input: str) -> str:
        input = self.base_prompt + " " + input
        response = self.model.invoke(input=input)
        return response.content