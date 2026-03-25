"""
FastAPI application for AI Hackathon project.
Provides endpoints for chat interactions and article credibility scoring.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# Initialize FastAPI app
app = FastAPI(
    title="AI Hackathon API",
    description="Backend API for credibility scoring and RAG-based chat",
    version="1.0.0",
)

# Configure CORS middleware
# Allow requests from React development server on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class ChatRequest(BaseModel):
    """Model for chat endpoint requests."""

    user_message: str


class ChatResponse(BaseModel):
    """Model for chat endpoint responses."""

    status: str
    message: str
    response: Optional[str] = None


class ScoreRequest(BaseModel):
    """Model for scoring endpoint requests."""

    article_url: str


class ScoreResponse(BaseModel):
    """Model for scoring endpoint responses."""

    status: str
    message: str
    score: Optional[float] = None


@app.get("/")
async def root():
    """Root endpoint to verify API is running."""
    return {"status": "success", "message": "AI Hackathon API is running"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint for processing user messages.

    Args:
        request: ChatRequest containing user_message

    Returns:
        ChatResponse with status and response message
    """
    user_message = request.user_message

    # TODO: Integrate RAG engine here
    # - Extract context from RAG engine based on user_message
    # - Generate response using LLM
    # - Return structured response

    return ChatResponse(
        status="success",
        message="Message received",
        response=f"Processed message: '{user_message}' (RAG integration pending)",
    )


@app.post("/api/score", response_model=ScoreResponse)
async def score_endpoint(request: ScoreRequest):
    """
    Article scoring endpoint for assessing credibility.

    Args:
        request: ScoreRequest containing article_url

    Returns:
        ScoreResponse with credibility score
    """
    article_url = request.article_url

    # TODO: Integrate scoring algorithm here
    # - Fetch article from URL
    # - Extract article data (citations, author credentials, emotional language)
    # - Calculate credibility score using calculate_credibility_score()
    # - Return structured response

    return ScoreResponse(
        status="success",
        message="Article scoring initiated",
        score=75.0,  # Placeholder score
    )


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "AI Hackathon API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
