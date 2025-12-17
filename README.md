# 🍳 CookShare AI Chatbot

AI Chatbot tư vấn món ăn cho ứng dụng CookShare.

## 📋 Tổng Quan

### Kiến Trúc

```
React Native App
       ↓ HTTP Request
┌──────────────────────────────────────────┐
│            Railway ($5/month)            │
│  ┌────────────────────────────────────┐  │
│  │  api.py (FastAPI)                  │  │
│  │  - POST /chat                      │  │
│  │  - GET /health                     │  │
│  └────────────────────────────────────┘  │
│                    ↓                     │
│  ┌────────────────────────────────────┐  │
│  │  model.py (Wrapper)                │  │
│  │  - Gửi prompt → Engine             │  │
│  │  - Nhận output ← Engine            │  │
│  └────────────────────────────────────┘  │
│                    ↓                     │
│  ┌────────────────────────────────────┐  │
│  │  llama-cpp-python (Engine)         │  │
│  │  - Load & run GGUF model           │  │
│  └────────────────────────────────────┘  │
│                    ↓                     │
│  ┌────────────────────────────────────┐  │
│  │  models/cookshare.gguf             │  │
│  │  (Fine-tuned, Quantized Q4)        │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
```

### Quy Trình Training (Chuẩn Học Thuật)

```
train.jsonl (172 samples)
         ↓
┌────────────────────────┐
│ 1. Fine-tune với LoRA  │  ← Tiết kiệm VRAM, train nhanh
│    (Qwen2-0.5B base)   │
└────────────────────────┘
         ↓
┌────────────────────────┐
│ 2. Merge LoRA weights  │  ← Gộp adapter vào model gốc
│    vào base model      │
└────────────────────────┘
         ↓
┌────────────────────────┐
│ 3. Quantize → GGUF     │  ← Nén model (Q4_K_M)
│    (~300MB output)     │
└────────────────────────┘
         ↓
┌────────────────────────┐
│ 4. Deploy lên Railway  │  ← Chạy với llama-cpp-python
└────────────────────────┘
```

## 🚀 Hướng Dẫn Sử Dụng

### 📚 Tài Liệu

- **Training trên Colab:** [COLAB_TRAINING.md](COLAB_TRAINING.md) - Hướng dẫn chi tiết từng bước
- **Sau khi training:** [POST_TRAINING.md](POST_TRAINING.md) - Convert GGUF, test, deploy

---

### 1. Training Model (Google Colab)

**Xem chi tiết:** [COLAB_TRAINING.md](COLAB_TRAINING.md)

**Tóm tắt:**
1. Mở Colab → Chọn GPU
2. Copy 8 cells từ `COLAB_TRAINING.md`
3. Chạy theo thứ tự
4. Download `cookbot-merged.zip`

---

### 2. Sau Khi Training

**Xem chi tiết:** [POST_TRAINING.md](POST_TRAINING.md)

**Tóm tắt:**
1. Giải nén `cookbot-merged.zip` → `models/cookbot-merged/`
2. Convert sang GGUF → `models/cookshare.gguf`
3. Test model → `python test_model.py`
4. Deploy Railway

---

### 3. Test Local

```bash
# Test GGUF model
python test_model.py

# Run API server
python api.py
# Server chạy tại http://localhost:8000
```

---

### 4. Deploy lên Railway

1. Push code lên GitHub (có file `cookshare.gguf`)
2. Tạo project mới trên Railway
3. Connect GitHub repo
4. Set environment variables:
   ```
   GGUF_MODEL_PATH=models/cookshare.gguf
   PORT=7860
   ```
5. Deploy!

## 📁 Cấu Trúc Project

```
cookshare-chatbot/
├── api.py                      # FastAPI server
├── model.py                    # Chatbot wrapper (llama-cpp)
├── train_full_pipeline.py      # Training script
├── requirements.txt            # Deployment dependencies
├── requirements-training.txt   # Training dependencies
├── Dockerfile                  # Docker config
│
├── dataset/
│   ├── train.jsonl            # Combined training data (172 samples)
│   ├── merge_all.py           # Script merge dataset
│   ├── 01_core/               # Core features data
│   ├── 02_advanced/           # Advanced features data
│   └── 03_ai_features/        # AI features data
│
└── models/
    ├── cookbot-lora/          # LoRA adapter (after step 1)
    ├── cookbot-merged/        # Merged model (after step 2)
    └── cookshare.gguf         # Final GGUF file (after step 3)
```

## 🔌 API Endpoints

### POST /chat
Chat với chatbot (có hỗ trợ history)

**Request:**
```json
{
  "message": "Làm thế nào để nấu phở bò?",
  "history": [
    {"role": "user", "content": "Xin chào"},
    {"role": "assistant", "content": "Chào bạn!"}
  ]
}
```

**Response:**
```json
{
  "response": "Để nấu phở bò, bạn cần...",
  "success": true
}
```

### GET /health
Health check

**Response:**
```json
{"status": "healthy"}
```

### GET /model-info
Thông tin về model đang sử dụng

**Response:**
```json
{
  "engine": "llama-cpp-python",
  "model_path": "models/cookshare.gguf",
  "model_loaded": true,
  "using_api": false
}
```

## 🎯 Features

### Core Features
- Gợi ý công thức từ nguyên liệu
- Hướng dẫn nấu từng bước
- Thay thế nguyên liệu
- Điều chỉnh khẩu phần
- Cảnh báo dị ứng/kiêng kỵ

### Advanced Features
- Lên lịch ăn theo tuần
- Gợi ý món theo thời tiết
- Tạo danh sách mua sắm
- Ước tính chi phí
- Tips nấu ăn

### AI Features
- Nhớ sở thích người dùng
- Phát hiện yêu cầu nguy hiểm
- Giải thích gợi ý

## 📊 Dataset

- **Tổng số samples:** 172
- **Core features:** ~80 samples
- **Advanced features:** ~60 samples
- **AI features:** ~32 samples

Dataset bao gồm:
- Món ăn Việt Nam (Bắc, Trung, Nam)
- Món ăn quốc tế
- Các tình huống đặc biệt (dị ứng, bệnh lý, trẻ em, bà bầu...)
- Tips và kiến thức nấu ăn

## 💰 Chi Phí

- **Training:** Free (Google Colab với GPU)
- **Deployment:** $5/month (Railway Hobby Plan)
- **Total:** $5/month

## 📝 License

MIT License
