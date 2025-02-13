from sentence_transformers import SentenceTransformer
from langchain_community.llms import Ollama
from config import EMBED_MODEL_NAME, LLM_MODEL

class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer(EMBED_MODEL_NAME)

    def encode(self, texts):
        return self.model.encode(texts)

class LLMModel:
    def __init__(self):
        self.model = Ollama(model=LLM_MODEL)

    def generate(self, prompt):
        response = ""
        for token in self.model.stream(prompt):
            response += token
        return response
