"""
CookShare Chatbot Model
Wrapper cho llama-cpp-python với model đã train (.gguf)
CHỈ dùng model đã train - KHÔNG có fallback
"""

import os
from typing import List, Tuple, Optional

class CookShareChatbot:
    """
    CookBot - AI tư vấn món ăn cho ứng dụng CookShare
    
    Kiến trúc:
    - Model: Fine-tuned Qwen2-0.5B → cookshare.gguf
    - Engine: llama-cpp-python
    - CHỈ dùng model đã train - KHÔNG có fallback
    
    Features:
    - Gợi ý công thức từ nguyên liệu
    - Hướng dẫn nấu từng bước
    - Thay thế nguyên liệu
    - Điều chỉnh khẩu phần
    - Cảnh báo dị ứng/kiêng kỵ
    - Lên lịch ăn, gợi ý theo thời tiết
    - Ước tính chi phí
    """
    
    def __init__(self):
        """
        Initialize chatbot
        CHỈ dùng model đã train (cookshare.gguf)
        KHÔNG có fallback về model chưa train
        """
        # Config paths
        self.gguf_model_path = os.getenv("GGUF_MODEL_PATH", "models/cookshare.gguf")
        
        # Engine state
        self.llm = None  # llama-cpp model
        
        # System prompt (context cơ bản - model đã học từ training data)
        self.system_prompt = "Bạn là CookBot - AI tư vấn món ăn của CookShare. Trả lời thân thiện bằng tiếng Việt."
        
        # Initialize
        self._initialize()
    
    def _initialize(self):
        """Initialize model engine - CHỈ dùng model đã train"""
        # Kiểm tra file GGUF có tồn tại không
        if not os.path.exists(self.gguf_model_path):
            warning_msg = f"⚠️  CHƯA TÌM THẤY MODEL: {self.gguf_model_path}\n" \
                         f"👉 Service sẽ start nhưng chưa thể trả lời.\n" \
                         f"👉 Upload file model qua Railway CLI: railway upload models/cookshare.gguf\n" \
                         f"👉 Sau đó restart service."
            print(warning_msg)
            self.llm = None  # Model chưa load
            return
        
        print(f"🔍 Tìm thấy model đã train: {self.gguf_model_path}")
        self._load_gguf_model()
    
    def _load_gguf_model(self):
        """Load GGUF model với llama-cpp-python - Model đã train là bắt buộc"""
        try:
            from llama_cpp import Llama
            
            print(f"📥 Đang load model đã train...")
            
            # Detect GPU (trên Railway thường không có GPU)
            n_gpu_layers = 0
            try:
                import torch
                if torch.cuda.is_available():
                    n_gpu_layers = -1  # Use all GPU layers
                    print(f"🎮 GPU detected: {torch.cuda.get_device_name(0)}")
            except ImportError:
                pass
            
            # Load model đã train
            # Tối ưu cho tốc độ: giảm n_ctx, tắt verbose, tăng threads
            self.llm = Llama(
                model_path=self.gguf_model_path,
                n_ctx=1024,           # Giảm context window để tăng tốc
                n_batch=256,          # Giảm batch size để tăng tốc
                n_gpu_layers=n_gpu_layers,
                verbose=False,        # Tắt verbose để tăng tốc
                n_threads=8           # Tăng threads (Railway có 8 vCPUs)
            )
            
            print("✅ Model đã train loaded successfully!")
            
        except ImportError:
            error_msg = "❌ llama-cpp-python chưa được cài đặt.\n" \
                       "👉 Model đã train yêu cầu llama-cpp-python. " \
                       "Vui lòng cài đặt trong Dockerfile."
            print(error_msg)
            raise RuntimeError(error_msg)
            
        except Exception as e:
            error_msg = f"❌ KHÔNG THỂ LOAD MODEL ĐÃ TRAIN: {e}\n" \
                       "👉 File GGUF có thể bị corrupt hoặc convert không đúng.\n" \
                       "👉 Cần re-upload file lên Google Drive hoặc convert lại."
            print(error_msg)
            # Không raise error, để service vẫn start được
            # Model sẽ được load lại khi có request (nếu file được fix)
            self.llm = None
    
    def _format_prompt(self, messages: List[dict]) -> str:
        """
        Format messages sang ChatML format
        Compatible với nhiều model (Qwen, Phi, Llama, etc.)
        """
        prompt = ""
        has_system = False
        
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                prompt += f"<|im_start|>system\n{content}<|im_end|>\n"
                has_system = True
            elif role == "user":
                prompt += f"<|im_start|>user\n{content}<|im_end|>\n"
            elif role == "assistant":
                prompt += f"<|im_start|>assistant\n{content}<|im_end|>\n"
        
        # Thêm system prompt nếu chưa có
        if not has_system:
            prompt = f"<|im_start|>system\n{self.system_prompt}<|im_end|>\n" + prompt
        
        # Trigger assistant response
        prompt += "<|im_start|>assistant\n"
        
        return prompt
    
    def _generate_gguf(self, messages: List[dict]) -> str:
        """
        Generate response từ GGUF model
        """
        try:
            prompt = self._format_prompt(messages)
            
            output = self.llm(
                prompt,
                max_tokens=1024,
                temperature=0.7,
                top_p=0.9,
                stop=["<|im_end|>", "<|im_start|>"],
                echo=False
            )
            
            response = output["choices"][0]["text"]
            return self._clean_response(response)
            
        except Exception as e:
            return f"Xin lỗi, có lỗi xảy ra: {str(e)}"
    
    
    def _clean_response(self, text: str) -> str:
        """Clean up response text"""
        # Remove common tags
        tags_to_remove = [
            "<|im_end|>", "<|im_start|>", "<|end|>", 
            "<|assistant|>", "<|user|>", "<|system|>"
        ]
        for tag in tags_to_remove:
            text = text.replace(tag, "")
        
        return text.strip()
    
    def get_response(self, user_message: str, history: List[Tuple[str, str]] = None) -> str:
        """
        Get response từ chatbot
        
        Args:
            user_message: Câu hỏi của user
            history: Lịch sử chat [(user_msg, assistant_msg), ...]
        
        Returns:
            Response từ chatbot
        """
        # Kiểm tra model đã load chưa
        if self.llm is None:
            if not os.path.exists(self.gguf_model_path):
                return "⚠️ Model chưa được upload. Vui lòng upload file cookshare.gguf qua Railway CLI và restart service."
            # Thử load lại model (có thể đã upload sau khi start)
            print("🔄 Thử load model lại...")
            self._load_gguf_model()
            if self.llm is None:
                return "⚠️ Không thể load model. Vui lòng kiểm tra logs."
        
        if history is None:
            history = []
        
        # Build messages
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add history
        for user_msg, assistant_msg in history:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": assistant_msg})
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        # Generate response từ model đã train
        response = self._generate_gguf(messages)
        
        return response.strip()
    
    def get_model_info(self) -> dict:
        """Get info về model đang dùng"""
        return {
            "engine": "llama-cpp-python",
            "model_path": self.gguf_model_path,
            "model_loaded": self.llm is not None,
            "model_type": "Fine-tuned Qwen2-0.5B (cookshare.gguf)",
        }


# Test
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 Testing CookBot")
    print("=" * 50)
    
    bot = CookShareChatbot()
    print(f"\n📊 Model info: {bot.get_model_info()}")
    
    # Test questions
    test_questions = [
        "Xin chào!",
        "Mình có trứng và cà chua, làm món gì?",
        "Hướng dẫn cách làm phở bò",
    ]
    
    for q in test_questions:
        print(f"\n👤 User: {q}")
        response = bot.get_response(q)
        print(f"🤖 Bot: {response[:300]}..." if len(response) > 300 else f"🤖 Bot: {response}")
