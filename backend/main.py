from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.sherlock_bot import SherlockBot
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

load_dotenv()

bot = SherlockBot(api_key)

class QueryInput(BaseModel):
    query: str



@app.get("/")
async def root():
    return {"message": "Welcome to Sherlock Bot API,"}

@app.post("/chat")
async def chat(query_input: QueryInput):
    try:
        response = bot.chat(
            query_input.query,
            conversation_id=query_input.conversation_id
        )
        return {
            "status": "success",
            "message": response.content,
            "conversation_id": response.conversation_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/reset")
async def reset_conversation(conversation_id: str):
    try:
        bot.reset_conversation(conversation_id)
        return {"status": "success", "message": "Conversation reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
