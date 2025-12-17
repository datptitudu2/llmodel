"""
CookShare Chatbot Model
Sử dụng Fine-tuned Model hoặc Hugging Face Inference API
"""

import os
from typing import List, Tuple, Optional
import requests

class CookShareChatbot:
    """
    CookBot - AI tư vấn món ăn cho ứng dụng CookShare
    
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
        Priority: Fine-tuned model > Inference API > Base model
        """
        # Config
        self.use_inference_api = os.getenv("USE_INFERENCE_API", "true").lower() == "true"
        self.api_token = os.getenv("HF_TOKEN", "")
        
        # Model paths
        self.finetuned_model_path = os.getenv("FINETUNED_MODEL_PATH", "models/cookbot-finetuned")
        self.base_model_name = "microsoft/Phi-3-mini-4k-instruct"
        
        # Current model (will be set later)
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
        
        # System prompt (QUAN TRỌNG: Giúp model trả lời chính xác, đúng format như training data)
        self.system_prompt = """Bạn là CookBot - AI tư vấn món ăn của CookShare. 

QUY TẮC QUAN TRỌNG:
1. CHỈ đưa ra thông tin CHÍNH XÁC về nguyên liệu, công thức nấu ăn
2. KHÔNG được bịa đặt nguyên liệu không tồn tại (như xà phòng, bột nước, nước thay nước, etc.)
3. CHỈ dùng nguyên liệu thực phẩm THẬT: thịt, rau, gia vị, nước mắm, đường, muối, dầu ăn, etc.
4. Trả lời theo FORMAT trong training data:
   - Dùng emoji phù hợp (🍚 🍜 🥢 🍳)
   - Có thông tin: ⏱ Thời gian, 📊 Độ khó, 👥 Khẩu phần
   - Liệt kê nguyên liệu rõ ràng
   - Hướng dẫn từng bước chi tiết
   - Có mẹo nấu ăn
5. Trả lời NGẮN GỌN, RÕ RÀNG, DỄ HIỂU
6. Nếu không chắc chắn, hãy nói "Tôi chưa có thông tin chính xác về món này"
7. Luôn nhắc nhở về an toàn thực phẩm khi cần

Trả lời thân thiện bằng tiếng Việt."""
        
        # Initialize
        self._initialize()
    
    def _initialize(self):
        """Initialize model hoặc API"""
        # Thử load fine-tuned model trước
        if os.path.exists(self.finetuned_model_path) and not self.use_inference_api:
            print(f"🔍 Tìm thấy fine-tuned model: {self.finetuned_model_path}")
            self._load_finetuned_model()
        elif self.use_inference_api and self.api_token:
            print("✅ Sử dụng Hugging Face Inference API")
        else:
            print("⚠️  Không có fine-tuned model, sẽ dùng Inference API")
            self.use_inference_api = True
    
    def _load_finetuned_model(self):
        """Load fine-tuned model (LoRA)"""
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            from peft import PeftModel
            import torch
            
            print(f"📥 Đang load fine-tuned model...")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.finetuned_model_path)
            
            # Load base model
            base_model = AutoModelForCausalLM.from_pretrained(
                self.base_model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None,
                trust_remote_code=True
            )
            
            # Load LoRA adapter
            self.model = PeftModel.from_pretrained(base_model, self.finetuned_model_path)
            self.model.eval()
            
            self.model_loaded = True
            self.use_inference_api = False
            print("✅ Fine-tuned model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Lỗi load fine-tuned model: {e}")
            print("Falling back to Inference API...")
            self.use_inference_api = True
            self.model_loaded = False
    
    def _load_base_model(self):
        """Load base model (fallback)"""
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            import torch
            
            print(f"📥 Đang load base model: {self.base_model_name}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.base_model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.base_model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None,
                trust_remote_code=True
            )
            
            self.model_loaded = True
            print("✅ Base model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Lỗi load base model: {e}")
            self.use_inference_api = True
    
    def _format_messages(self, messages: List[dict]) -> str:
        """
        Format messages theo Phi-3 chat template
        """
        formatted = ""
        has_system = False
        
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                formatted += f"<|system|>\n{content}<|end|>\n"
                has_system = True
            elif role == "user":
                formatted += f"<|user|>\n{content}<|end|>\n"
            elif role == "assistant":
                formatted += f"<|assistant|>\n{content}<|end|>\n"
        
        # Thêm system prompt nếu chưa có
        if not has_system:
            formatted = f"<|system|>\n{self.system_prompt}<|end|>\n" + formatted
        
        # Thêm assistant tag để model tiếp tục
        formatted += "<|assistant|>\n"
        
        return formatted
    
    def _call_inference_api(self, messages: List[dict]) -> str:
        """
        Gọi Hugging Face Inference API
        """
        # Thử fine-tuned model trên HF Hub trước, rồi base model
        model_to_use = os.getenv("HF_MODEL_ID", self.base_model_name)
        api_url = f"https://api-inference.huggingface.co/models/{model_to_use}"
        
        headers = {}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        
         payload = {
             "inputs": self._format_messages(messages),
             "parameters": {
                 "max_new_tokens": 512,      # Giảm để tăng tốc và tránh hallucination
                 "temperature": 0.5,         # Giảm để response chính xác hơn
                 "top_p": 0.8,               # Giảm để tập trung vào tokens có xác suất cao
                 "top_k": 40,                # Giới hạn top_k để tránh chọn tokens lạ
                 "do_sample": True,
                 "return_full_text": False,
                 "repetition_penalty": 1.2   # Tránh lặp lại
             }
         }
        
        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                text = result[0].get("generated_text", "")
            elif isinstance(result, dict):
                text = result.get("generated_text", "")
            else:
                text = "Xin lỗi, mình không thể trả lời câu hỏi này."
            
            # Clean up response
            text = self._clean_response(text)
            return text
            
        except requests.exceptions.RequestException as e:
            return f"Xin lỗi, có lỗi kết nối: {str(e)}"
    
    def _generate_local(self, messages: List[dict]) -> str:
        """
        Generate response từ local model
        """
        try:
            import torch
            
            formatted_input = self._format_messages(messages)
            inputs = self.tokenizer(formatted_input, return_tensors="pt")
            
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
             with torch.no_grad():
                 outputs = self.model.generate(
                     **inputs,
                     max_new_tokens=512,      # Giảm để tăng tốc và tránh hallucination
                     temperature=0.5,         # Giảm để response chính xác hơn
                     top_p=0.8,               # Giảm để tập trung vào tokens có xác suất cao
                     top_k=40,                # Giới hạn top_k để tránh chọn tokens lạ
                     do_sample=True,
                     pad_token_id=self.tokenizer.eos_token_id,
                     repetition_penalty=1.2   # Tránh lặp lại
                 )
            
            # Decode only new tokens
            response = self.tokenizer.decode(
                outputs[0][inputs["input_ids"].shape[1]:], 
                skip_special_tokens=True
            )
            
            # Clean up
            response = self._clean_response(response)
            return response
            
        except Exception as e:
            return f"Xin lỗi, có lỗi xảy ra: {str(e)}"
    
    def _clean_response(self, text: str) -> str:
        """
        Clean up response text
        """
        # Remove trailing tags
        for tag in ["<|end|>", "<|assistant|>", "<|user|>", "<|system|>"]:
            text = text.replace(tag, "")
        
        # Strip whitespace
        text = text.strip()
        
        return text
    
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
        if self.use_inference_api or not self.model_loaded:
            response = self._call_inference_api(messages)
        else:
            response = self._generate_local(messages)
        
        return response.strip()
    
    def get_model_info(self) -> dict:
        """Get info về model đang dùng"""
        return {
            "using_inference_api": self.use_inference_api,
            "model_loaded": self.model_loaded,
            "finetuned_path": self.finetuned_model_path if os.path.exists(self.finetuned_model_path) else None,
            "base_model": self.base_model_name,
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
