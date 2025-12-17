"""
CookShare Chatbot API Server
API endpoint cho React Native app
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from model import CookShareChatbot
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="CookShare Chatbot API",
    description="API cho chatbot ứng dụng CookShare",
    version="1.0.0"
)

# CORS middleware - cho phép React Native gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production nên set domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chatbot
chatbot = CookShareChatbot()

# Request/Response models
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []  # Lịch sử chat

class ChatResponse(BaseModel):
    response: str
    success: bool
    error: Optional[str] = None

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "CookShare Chatbot API is running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}

@app.get("/model-info")
async def model_info():
    """Get thông tin về model đang sử dụng"""
    return chatbot.get_model_info()

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint - React Native gọi endpoint này
    
    Request body:
    {
        "message": "Làm thế nào để nấu phở bò?",
        "history": [
            {"role": "user", "content": "Xin chào"},
            {"role": "assistant", "content": "Chào bạn! Tôi có thể giúp gì?"}
        ]
    }
    
    Response:
    {
        "response": "Để nấu phở bò, bạn cần...",
        "success": true
    }
    """
    try:
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Convert history format từ API sang format model cần
        history_tuples = []
        for msg in request.history:
            if msg.role == "user":
                # Tìm assistant response tiếp theo
                idx = request.history.index(msg)
                if idx + 1 < len(request.history) and request.history[idx + 1].role == "assistant":
                    history_tuples.append((msg.content, request.history[idx + 1].content))
        
        # Get response từ chatbot
        response = chatbot.get_response(request.message, history_tuples)
        
        return ChatResponse(
            response=response,
            success=True
        )
    
    except Exception as e:
        return ChatResponse(
            response="",
            success=False,
            error=str(e)
        )

@app.post("/chat/simple")
async def chat_simple(message: str):
    """
    Simple chat endpoint - không cần history
    
    Query param: ?message=your_message
    """
    try:
        if not message or not message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        response = chatbot.get_response(message, [])
        
        return {
            "response": response,
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run server
    # Đọc PORT từ environment variable (Railway tự động set)
    # Nếu không có thì dùng 8000 cho local development
    import os
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=port,
        reload=True  # Auto reload khi code thay đổi
    )

