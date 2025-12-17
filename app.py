"""
Entry point cho Railway/Hugging Face Spaces
Railway sẽ tự động chạy file này
"""

import os
import uvicorn
from api import app

if __name__ == "__main__":
    # Đọc PORT từ environment variable (Railway tự động set)
    # Nếu không có thì dùng 7860 (default cho Railway)
    port = int(os.getenv("PORT", 7860))
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )

