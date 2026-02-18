# chat_engine.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini LLM wrapper
class GeminiLLMWrapper:
    def __init__(self, model="chat-bison-001", temperature=0.2):
        self.model = model
        self.temperature = temperature

    def generate(self, messages):
        response = genai.chat.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature
        )
        return response.last.split("\n")[0]

# Session memory
session_memory_map = {}

def get_response(session_id: str, user_query: str) -> str:
    if session_id not in session_memory_map:
        session_memory_map[session_id] = []

    # Add user message
    session_memory_map[session_id].append({"author": "user", "content": user_query})

    # Generate response
    llm = GeminiLLMWrapper()
    bot_response = llm.generate(session_memory_map[session_id])

    # Add bot response to memory
    session_memory_map[session_id].append({"author": "bot", "content": bot_response})

    return bot_response
