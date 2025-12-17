"""
Test GGUF Model
Kiểm tra model hoạt động tốt trước khi deploy
"""

import os
from pathlib import Path

GGUF_PATH = "models/cookshare.gguf"

print("=" * 60)
print("🧪 TEST GGUF MODEL")
print("=" * 60)

# Check file exists
if not os.path.exists(GGUF_PATH):
    print(f"❌ Không tìm thấy: {GGUF_PATH}")
    print("👉 Cần convert sang GGUF trước (xem POST_TRAINING.md)")
    exit(1)

size_mb = os.path.getsize(GGUF_PATH) / (1024 * 1024)
print(f"✅ File: {GGUF_PATH}")
print(f"💾 Size: {size_mb:.1f} MB")

# Try to load
try:
    from llama_cpp import Llama
    
    print("\n📥 Loading model...")
    llm = Llama(
        model_path=GGUF_PATH,
        n_ctx=2048,
        n_batch=512,
        verbose=False
    )
    print("✅ Model loaded successfully!")
    
    # Test prompt
    prompt = "<|im_start|>system\nBạn là CookBot - AI tư vấn món ăn của CookShare. Trả lời thân thiện bằng tiếng Việt.<|im_end|>\n<|im_start|>user\nXin chào!<|im_end|>\n<|im_start|>assistant\n"
    
    print("\n🧪 Testing với prompt:")
    print(f"   {prompt[:100]}...")
    
    output = llm(
        prompt,
        max_tokens=100,
        temperature=0.7,
        top_p=0.9,
        stop=["<|im_end|>", "<|im_start|>"],
        echo=False
    )
    
    response = output["choices"][0]["text"]
    print(f"\n🤖 Response: {response}")
    
    print("\n" + "=" * 60)
    print("✅ MODEL HOẠT ĐỘNG TỐT!")
    print("=" * 60)
    print("\n📝 Next steps:")
    print("   1. Deploy lên Railway (xem POST_TRAINING.md)")
    print("   2. Hoặc test API local: python api.py")
    
except ImportError:
    print("\n❌ llama-cpp-python chưa được cài đặt")
    print("👉 Chạy: pip install llama-cpp-python")
    exit(1)
except Exception as e:
    print(f"\n❌ Lỗi khi test: {e}")
    exit(1)

