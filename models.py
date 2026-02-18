from pydantic import BaseModel  # Import BaseModel from Pydantic

class ChatRequest(BaseModel):
    session_id: str
    query: str
