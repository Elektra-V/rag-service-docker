from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
import os

OLLAMA_URL = os.getenv("OLLAMA_URL","http://ollama:11434")
LLM = os.getenv("OLLAMA_LLM","llama3.1:8b")
EMBED = os.getenv("OLLAMA_EMBED","nomic-embed-text")

class OllamaService:
    def __init__(self):
        self.llm = Ollama(model=LLM, base_url=OLLAMA_URL, request_timeout=180)
        self.embed = OllamaEmbedding(model_name=EMBED, base_url=OLLAMA_URL, request_timeout=180)
    def get_llm(self): return self.llm
    def get_embed(self): return self.embed