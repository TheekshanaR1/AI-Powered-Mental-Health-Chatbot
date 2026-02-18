# doc_engine.py
import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.llms import CustomLLM, CompletionResponse, LLMMetadata
from llama_index.core.llms.callbacks import llm_completion_callback
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from google import genai
from google.genai import types

load_dotenv()
_client = None

def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment. Check your .env file.")
        _client = genai.Client(api_key=api_key)
    return _client

# LLM wrapper for LlamaIndex
class GeminiLLMWrapperForLlama(CustomLLM):
    model: str = "models/gemini-2.5-flash"
    temperature: float = 0.2
    context_window: int = 8192
    num_output: int = 512

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.num_output,
            model_name=self.model,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs) -> CompletionResponse:
        response = _get_client().models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=self.temperature),
        )
        return CompletionResponse(text=response.text)

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs):
        raise NotImplementedError("Streaming not supported")

# Configure LlamaIndex to use Gemini LLM and FastEmbed for local embeddings
Settings.llm = GeminiLLMWrapperForLlama()
Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Load documents
documents = SimpleDirectoryReader("data").load_data()

# Create Vector Index
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()

def query_documents(user_query: str) -> str:
    response = query_engine.query(user_query)
    return str(response)
