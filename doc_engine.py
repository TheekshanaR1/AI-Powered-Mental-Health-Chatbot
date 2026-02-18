# doc_engine.py
import os
from dotenv import load_dotenv
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index import ServiceContext, LLMPredictor, PromptHelper
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# LLM wrapper for LlamaIndex
class GeminiLLMWrapperForLlama:
    def __init__(self, model="text-bison-001", temperature=0.2):
        self.model = model
        self.temperature = temperature

    def predict(self, prompt: str) -> str:
        response = genai.chat.create(
            model=self.model,
            messages=[{"author": "user", "content": prompt}],
            temperature=self.temperature
        )
        return response.last.split("\n")[0]

llama_llm = LLMPredictor(llm=GeminiLLMWrapperForLlama())

# Load documents
documents = SimpleDirectoryReader("data").load_data()

# Create Vector Index
index = VectorStoreIndex.from_documents(
    documents,
    service_context=ServiceContext.from_defaults(
        llm_predictor=llama_llm,
        prompt_helper=PromptHelper.from_defaults(
            max_input_size=4096,
            num_output=512,
            max_chunk_overlap=20
        )
    )
)

query_engine = index.as_query_engine(llama_llm)

def query_documents(user_query: str) -> str:
    response = query_engine.query(user_query)
    return response.response
