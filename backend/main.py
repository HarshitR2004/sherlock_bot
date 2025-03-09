from fastapi import FastAPI, HTTPException
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from sherlock_bot import SherlockBot  

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Retrieve API Key
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY not found") 

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

bot = SherlockBot(api_key)

class QueryInput(BaseModel):
    query: str
    conversation_id: Optional[str] = None

@app.get("/")
async def root():
    return {
        "api": {
            "title": "THE SHERLOCK HOLMES DETECTIVE API",
            "version": "1.0.0"
        },
        "welcome_message": {
            "title": "THE GAME IS AFOOT!",
            "subtitle": "221B Baker Street • Established 1887 • Digital Consultancy"
        },
        "introduction": "I am Sherlock Holmes, the world's only consulting detective. Through this digital interface, my methods of observation, deduction, and analysis are at your service. No puzzle too small, no mystery too complex.",
        "quotation": "When you have eliminated the impossible, whatever remains, however improbable, must be the truth.",
        "status": {
            "investigations": "OPEN FOR CONSULTATION",
            "telegraph": "OPERATIONAL",
            "mood": "CONTEMPLATIVE"
        },
        "signature": "Yours in the pursuit of logic and reason, S.H."
    }

@app.post("/chat")
async def chat(query_input: QueryInput):
    try:
        response_text = bot.chat(query_input.query, conversation_id=query_input.conversation_id)
        return {
            "status": "success",
            "message": response_text,  
            "conversation_id": query_input.conversation_id  
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset")
async def reset_conversation(conversation_id: str):
    try:
        bot.reset_conversation(conversation_id)
        return {"status": "success", "message": f"Conversation {conversation_id} reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
