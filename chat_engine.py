# chat_engine.py
import os
from dotenv import load_dotenv
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

# Gemini LLM wrapper
class GeminiLLMWrapper:
    def __init__(self, model="models/gemini-2.5-flash", temperature=0.2):
        self.model = model
        self.temperature = temperature

    def generate(self, messages):
        # Convert session messages to Gemini Content format
        contents = [
            types.Content(
                role="user" if m["author"] == "user" else "model",
                parts=[types.Part(text=m["content"])]
            )
            for m in messages
        ]
        response = _get_client().models.generate_content(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(temperature=self.temperature),
        )
        return response.text

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
