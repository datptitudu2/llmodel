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
                         f"👉 Model sẽ được download từ Google Drive trong Dockerfile."
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
            # Tối ưu cho tốc độ: giảm n_ctx, tắt verbose, tăng threads, dùng mmap
            self.llm = Llama(
                model_path=self.gguf_model_path,
                n_ctx=512,            # Giảm context window xuống 512 để tăng tốc đáng kể
                n_batch=128,          # Giảm batch size xuống 128 để tăng tốc
                n_gpu_layers=n_gpu_layers,
                verbose=False,        # Tắt verbose để tăng tốc
                n_threads=8,          # Tăng threads (Railway có 8 vCPUs)
                use_mmap=True,        # Dùng memory mapping để tăng tốc load
                use_mlock=False       # Không lock memory (tiết kiệm RAM)
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
        Compatible với Qwen2 model
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
        if self.llm is None:
            # Thử load lại model nếu chưa load
            self._initialize()
            if self.llm is None:
                return "Xin lỗi, model chưa được load. Vui lòng kiểm tra logs."

        try:
            prompt = self._format_prompt(messages)
            
            output = self.llm(
                prompt,
                max_tokens=256,       # Giảm xuống 256 để tăng tốc đáng kể (vẫn đủ cho câu trả lời ngắn)
                temperature=0.5,      # Giảm temperature để response chính xác hơn, ít hallucination
                top_p=0.8,            # Giảm top_p để tập trung vào tokens có xác suất cao
                top_k=40,             # Giới hạn top_k để tránh chọn tokens lạ
                repeat_penalty=1.3,   # Tăng penalty để tránh lặp lại (1.0 = không penalty, >1.0 = penalty)
                stop=["<|im_end|>", "<|im_start|>", "\n\n\n"],  # Stop sớm khi gặp stop token hoặc nhiều newlines
                echo=False
            )
            
            response = output["choices"][0]["text"]
            return self._clean_response(response)
            
        except Exception as e:
            return f"Xin lỗi, có lỗi xảy ra khi tạo phản hồi: {str(e)}"
    
    def _clean_response(self, text: str) -> str:
        """
        Clean up response text - Remove duplicates và format
        """
        import re
        
        # Remove trailing tags
        for tag in ["<|im_end|>", "<|im_start|>assistant", "<|im_start|>user", "<|im_start|>system"]:
            text = text.replace(tag, "")
        
        # Clean up multiple newlines (giữ lại \n\n nhưng loại bỏ \n\n\n\n...)
        text = re.sub(r'\n{3,}', '\n\n', text)  # Thay nhiều \n bằng \n\n
        
        # Remove duplicate sentences/phrases
        # Split thành sentences (dựa vào dấu chấm, chấm hỏi, chấm than, xuống dòng)
        sentences = re.split(r'[.!?]\s+|\n+', text)
        seen = set()
        unique_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Normalize sentence để so sánh (lowercase, remove extra spaces)
            normalized = re.sub(r'\s+', ' ', sentence.lower().strip())
            
            # Bỏ qua câu quá ngắn (có thể là dấu câu)
            if len(normalized) < 5:
                unique_sentences.append(sentence)
                continue
            
            # Kiểm tra duplicate (cho phép một số khác biệt nhỏ)
            is_duplicate = False
            for seen_sentence in seen:
                # Nếu câu mới giống >80% với câu đã thấy thì coi là duplicate
                similarity = self._calculate_similarity(normalized, seen_sentence)
                if similarity > 0.8:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                seen.add(normalized)
                unique_sentences.append(sentence)
        
        # Join lại thành text
        text = '\n'.join(unique_sentences)
        
        # Remove duplicate lines (exact match)
        lines = text.split('\n')
        seen_lines = set()
        unique_lines = []
        for line in lines:
            line_stripped = line.strip()
            if line_stripped and line_stripped not in seen_lines:
                seen_lines.add(line_stripped)
                unique_lines.append(line)
        text = '\n'.join(unique_lines)
        
        # Strip whitespace
        text = text.strip()
        
        return text
    
    def _calculate_similarity(self, s1: str, s2: str) -> float:
        """
        Tính similarity giữa 2 strings (simple word overlap)
        """
        words1 = set(s1.split())
        words2 = set(s2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    def get_response(self, user_message: str, history: List[Tuple[str, str]] = None) -> str:
        """
        Get response từ chatbot
        
        Args:
            user_message: Câu hỏi của user
            history: Lịch sử chat [(user_msg, assistant_msg), ...]
        
        Returns:
            Response từ chatbot
        """
        if history is None:
            history = []
        
        # Build messages
        messages = []
        
        # Add system prompt
        messages.append({"role": "system", "content": self.system_prompt})
        
        # Add history
        for user_msg, assistant_msg in history:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": assistant_msg})
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        # Get response
        response = self._generate_gguf(messages)
        
        return response.strip()
    
    def get_model_info(self) -> dict:
        """Get info về model đang dùng"""
        return {
            "model_path": self.gguf_model_path,
            "model_loaded": self.llm is not None,
            "model_type": "Fine-tuned Qwen2-0.5B (cookshare.gguf)" if self.llm else "Not loaded",
        }


# Test
if __name__ == "__main__":
    print("🤖 Testing CookBot...")
    
    bot = CookShareChatbot()
    print(f"Model info: {bot.get_model_info()}")
    
    # Test questions
    test_questions = [
        "Xin chào",
        "Mình có trứng và cà chua, làm món gì?",
        "Cách làm phở bò?",
    ]
    
    for q in test_questions:
        print(f"\n👤 User: {q}")
        response = bot.get_response(q)
        print(f"🤖 Bot: {response[:200]}..." if len(response) > 200 else f"🤖 Bot: {response}")
