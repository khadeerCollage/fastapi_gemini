import os 
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class ChatRequest(BaseModel):
    prompt: str
    
class ChatResponse(BaseModel):
    response: str
    

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Chat API!"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    reponse_text = "..."
    return ChatResponse(response=reponse_text)

