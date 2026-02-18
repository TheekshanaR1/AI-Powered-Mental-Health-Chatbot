# main.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import ChatRequest
from chat_engine import get_response
from doc_engine import query_documents
from crisis import contains_crisis_keywords, SAFETY_MESSAGE
from logger import log_chat

load_dotenv()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-Powered Mental Health Chatbot! Use /chat endpoint."}

@app.post("/chat")
def chat_with_memory(request: ChatRequest):
    session_id = request.session_id
    user_query = request.query

    # Crisis detection
    if contains_crisis_keywords(user_query):
        log_chat(session_id, user_query, SAFETY_MESSAGE, True)
        return {"response": SAFETY_MESSAGE}

    # Normal chatbot response
    response = get_response(session_id, user_query)
    log_chat(session_id, user_query, response, False)
    return {"response": response}

@app.post("/doc-chat")
def chat_with_docs(request: ChatRequest):
    response = query_documents(request.query)
    return {"response": response}
