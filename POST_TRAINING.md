# 📥 Sau Khi Download Model - Hướng Dẫn Tiếp Theo

**Bạn đã có file `cookbot-merged.zip` - Giờ làm gì?**

---

## 📋 Tổng Quan Các Bước

1. ✅ **Giải nén model** (2 phút)
2. ✅ **Convert sang GGUF** (10-15 phút)
3. ✅ **Test model** (5 phút)
4. ✅ **Deploy lên Railway** (10 phút)

**Tổng thời gian: ~30 phút**

---

## 📦 Bước 1: Giải Nén Model

### Trên Windows:

1. **Click chuột phải** vào `cookbot-merged.zip`
2. Chọn **"Extract All..."** hoặc **"Extract to cookbot-merged\"**
3. Giải nén vào thư mục `models/` trong project:

```
F:\modelllmchatbot\
└── models\
    └── cookbot-merged\
        ├── config.json
        ├── model.safetensors
        ├── tokenizer.json
        └── ... (các file khác)
```

### Kiểm tra:

```bash
# Trong PowerShell
cd F:\modelllmchatbot
dir models\cookbot-merged
```

**Phải thấy file `model.safetensors` (~988MB)**

---

## 🔄 Bước 2: Convert Sang GGUF Format

### Cách 1: Dùng llama.cpp (Khuyến nghị)

#### 2.1: Clone llama.cpp

```bash
# Mở PowerShell hoặc CMD
cd F:\
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
```

#### 2.2: Cài Dependencies

```bash
# Cài Python packages
pip install -r requirements.txt

# Hoặc cài thủ công
pip install numpy
```

#### 2.3: Convert Sang GGUF

```bash
# Convert từ HuggingFace format sang GGUF (f16)
python convert_hf_to_gguf.py F:\modelllmchatbot\models\cookbot-merged --outfile F:\modelllmchatbot\models\cookshare-f16.gguf --outtype f16
```

**Thời gian: ~5-10 phút**

#### 2.4: Quantize (Giảm Size)

```bash
# Build llama-quantize (nếu chưa có)
# Windows: Download pre-built từ releases
# Hoặc build từ source (phức tạp hơn)

# Quantize sang Q4_K_M (balance giữa size và quality)
# Nếu có llama-quantize.exe:
.\llama-quantize.exe F:\modelllmchatbot\models\cookshare-f16.gguf F:\modelllmchatbot\models\cookshare.gguf q4_k_m
```

**Kết quả:** File `cookshare.gguf` (~300-400MB)

---

### Cách 2: Dùng Python Script (Đơn giản hơn)

Tạo file `convert_to_gguf.py`:

```python
"""
Convert HuggingFace model sang GGUF
Cần cài: pip install llama-cpp-python[server]
"""

import os
from pathlib import Path

# Paths
HF_MODEL_PATH = "models/cookbot-merged"
GGUF_OUTPUT = "models/cookshare.gguf"

print("🔄 Converting to GGUF...")
print(f"   Input: {HF_MODEL_PATH}")
print(f"   Output: {GGUF_OUTPUT}")

# Method 1: Dùng llama.cpp CLI (khuyến nghị)
print("\n📝 Hướng dẫn:")
print("=" * 60)
print("""
1. Clone llama.cpp:
   git clone https://github.com/ggerganov/llama.cpp
   cd llama.cpp

2. Convert:
   python convert_hf_to_gguf.py ../models/cookbot-merged --outfile ../models/cookshare.gguf --outtype f16

3. Quantize (optional):
   ./llama-quantize cookshare.gguf cookshare-q4.gguf q4_k_m
""")
print("=" * 60)

# Method 2: Upload lên Hugging Face và dùng convert tool online
print("\n💡 Hoặc upload lên Hugging Face và dùng convert tool online")
```

**Chạy:**

```bash
python convert_to_gguf.py
```

---

## 🧪 Bước 3: Test Model

**⚠️ Lưu ý:** Trên Windows, `llama-cpp-python` cần C compiler để build. Không thể test local.

**Giải pháp:** Test trên Railway sau khi deploy (Railway sẽ build tự động).

### Hoặc: Test trên Colab (Nếu muốn test trước)

1. Upload `cookshare.gguf` lên Google Drive
2. Mở Colab, mount Drive
3. Chạy test script

### Test Script (Chạy trên Railway hoặc Colab)

File `test_model.py` đã có sẵn:

```python
"""
Test GGUF model
"""

from llama_cpp import Llama
import os

GGUF_PATH = "models/cookshare.gguf"

if not os.path.exists(GGUF_PATH):
    print(f"❌ Không tìm thấy: {GGUF_PATH}")
    print("👉 Cần convert sang GGUF trước (xem POST_TRAINING.md)")
    exit(1)

print("📥 Loading model...")
llm = Llama(
    model_path=GGUF_PATH,
    n_ctx=2048,
    n_batch=512,
    verbose=False
)

print("✅ Model loaded!")

# Test
prompt = "<|im_start|>system\nBạn là CookBot - AI tư vấn món ăn của CookShare. Trả lời thân thiện bằng tiếng Việt.<|im_end|>\n<|im_start|>user\nXin chào!<|im_end|>\n<|im_start|>assistant\n"

print("\n🧪 Testing...")
print(f"Prompt: {prompt[:100]}...")

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

print("\n✅ Model hoạt động tốt!")
```

**Chạy trên Railway hoặc Colab:**

```bash
pip install llama-cpp-python
python test_model.py
```

**Hoặc:** Skip test, deploy Railway luôn và test qua API endpoint `/health` và `/chat`

---

## 🚀 Bước 4: Deploy Lên Railway

### 4.1: Chuẩn Bị Files

Đảm bảo có các file sau:

```
F:\modelllmchatbot\
├── api.py
├── model.py
├── requirements.txt
├── Dockerfile
└── models/
    └── cookshare.gguf  ← File này!
```

### 4.2: Push Lên GitHub

```bash
# Khởi tạo git (nếu chưa có)
git init
git add .
git commit -m "Add trained model"

# Tạo repo trên GitHub, rồi:
git remote add origin https://github.com/yourusername/cookshare-chatbot.git
git push -u origin main
```

### 4.3: Deploy Railway

1. **Truy cập:** https://railway.app
2. **Login** bằng GitHub
3. **New Project** → **Deploy from GitHub repo**
4. **Chọn repo** `cookshare-chatbot`
5. **Set Environment Variables:**
   ```
   GGUF_MODEL_PATH=models/cookshare.gguf
   PORT=7860
   ```
6. **Deploy!**

### 4.4: Test API

Sau khi deploy xong, Railway sẽ cung cấp URL:

```bash
# Test health
curl https://your-app.railway.app/health

# Test chat
curl -X POST https://your-app.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Xin chào!"}'
```

---

## 📝 Checklist

- [ ] Giải nén `cookbot-merged.zip` vào `models/cookbot-merged/`
- [ ] Convert sang GGUF → `models/cookshare.gguf`
- [ ] Test model local → `python test_model.py`
- [ ] Push code lên GitHub
- [ ] Deploy lên Railway
- [ ] Test API endpoint
- [ ] Kết nối React Native app

---

## 🆘 Troubleshooting

### Lỗi: "llama.cpp not found"
→ Clone llama.cpp và cài dependencies

### Lỗi: "convert_hf_to_gguf.py not found"
→ Đảm bảo đang ở trong thư mục `llama.cpp/`

### Lỗi: "Model too large for Railway"
→ Quantize xuống Q4 hoặc Q5 (giảm size)

### Lỗi: "API timeout"
→ Railway free tier có giới hạn, nên upgrade hoặc dùng VPS

---

## 🎯 Next Steps

1. **Test model** → Đảm bảo hoạt động tốt
2. **Deploy Railway** → Public API
3. **Kết nối React Native** → Update API URL trong app
4. **Test end-to-end** → Thử chatbot trong app

---

**🎉 Chúc mừng! Model đã sẵn sàng để deploy!**

