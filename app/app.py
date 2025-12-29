import os 
from fastapi import FastAPI , Depends
from pydantic import BaseModel
from src.ai.gemini import Gemini
from src.auth.dependencies import get_user_identifier
from src.auth.throttling import apply_rate_limit



app = FastAPI()

def load_system_prompt():
    try:
        with open("src/prompts/system_prompt.md", "r") as file:
            return file.read()
    except FileNotFoundError:
        return None

system_prompt = load_system_prompt()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

ai_platform = Gemini(api_key=gemini_api_key, system_prompt=system_prompt)


class ChatRequest(BaseModel):
    prompt: str
    
class ChatResponse(BaseModel):
    response: str
    

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, user_id:str = Depends(get_user_identifier)):
    apply_rate_limit(user_id)
    
    response_text = ai_platform.chat(request.prompt)
    return ChatResponse(response=response_text)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Chat API!"}
