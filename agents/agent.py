from abc import abstractmethod, ABC


class Agent(ABC):

    def __init__(self, model, base_prompt, stream=False):
        self.model = model
        self.base_prompt = base_prompt
        self.stream = stream

    @abstractmethod
    def invoke(self, input: str):
        pass
