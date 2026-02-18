# main.py
import os
import traceback
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

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
    return FileResponse("chatbot-ui/index.html")

@app.get("/style.css")
def get_css():
    return FileResponse("chatbot-ui/style.css", media_type="text/css")

@app.get("/chatbot.js")
def get_js():
    return FileResponse("chatbot-ui/chatbot.js", media_type="application/javascript")

@app.post("/chat")
def chat_with_memory(request: ChatRequest):
    try:
        session_id = request.session_id
        user_query = request.query
        if contains_crisis_keywords(user_query):
            log_chat(session_id, user_query, SAFETY_MESSAGE, True)
            return {"response": SAFETY_MESSAGE}
        response = get_response(session_id, user_query)
        log_chat(session_id, user_query, response, False)
        return {"response": response}
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/doc-chat")
def chat_with_docs(request: ChatRequest):
    try:
        response = query_documents(request.query)
        return {"response": response}
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
