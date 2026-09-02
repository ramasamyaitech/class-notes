from models import OllamaModel


class LLMService:

    def __init__(self):

        self.model = OllamaModel()
        self.llm = self.model.get_llm()

    def generate(self, prompt: str):

        response = self.llm.invoke(prompt)

        return response.content