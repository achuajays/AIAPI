from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv() 

# Initialize router
router = APIRouter(prefix="/query", tags=["query"])

# Initialize Groq client
groq = Groq(api_key=os.getenv("GROQ_API_KEY"))


# Request/Response models
class QueryRequest(BaseModel):
    query: str
    model: Optional[str] = "meta-llama/llama-4-scout-17b-16e-instruct"
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1024


class QueryResponse(BaseModel):
    answer: str


@router.post("/", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a query and return an answer from Groq LLM
    """
    try:
        # Create chat completion
        chat_completion = groq.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Provide clear, accurate, and concise answers to user queries."
                },
                {
                    "role": "user",
                    "content": request.query
                }
            ],
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=False
        )
        
        # Extract the answer
        answer = chat_completion.choices[0].message.content
        
        return QueryResponse(
            answer=answer,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@router.get("/health")
async def health_check():
    """Check if the query endpoint is healthy"""
    return {"status": "healthy", "endpoint": "query"}
