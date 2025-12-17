# 🚀 Hướng Dẫn Deploy Lên Railway

**Model đã convert xong (`cookshare.gguf` - 948MB). Giờ deploy!**

---

## 📋 Checklist Trước Khi Deploy

- [x] Model đã convert: `models/cookshare.gguf`
- [ ] Code đã push lên GitHub
- [ ] Railway account đã tạo
- [ ] Credit card đã add (cần $5)

---

## 🔧 Bước 1: Chuẩn Bị Code

### 1.1: Kiểm Tra Files

Đảm bảo có các file sau:

```
F:\modelllmchatbot\
├── api.py                    ✅ FastAPI server
├── model.py                  ✅ Model wrapper
├── requirements.txt          ✅ Dependencies
├── Dockerfile               ✅ Docker config
└── models/
    └── cookshare.gguf       ✅ Model file (948MB)
```

### 1.2: Kiểm Tra .gitignore

Đảm bảo `.gitignore` KHÔNG ignore file `cookshare.gguf`:

```gitignore
# Models (cần commit file GGUF)
!models/cookshare.gguf
models/*.gguf
!models/cookshare.gguf
```

---

## 📤 Bước 2: Push Lên GitHub

### 2.1: Khởi Tạo Git (Nếu Chưa Có)

```bash
cd F:\modelllmchatbot
git init
git add .
git commit -m "Add trained model and API"
```

### 2.2: Tạo Repo Trên GitHub

1. Truy cập: https://github.com/new
2. Tên repo: `cookshare-chatbot` (hoặc tên khác)
3. **Public** hoặc **Private** (tùy bạn)
4. Click **Create repository**

### 2.3: Push Code

```bash
git remote add origin https://github.com/YOUR_USERNAME/cookshare-chatbot.git
git branch -M main
git push -u origin main
```

**⚠️ Lưu ý:** File `cookshare.gguf` (948MB) sẽ mất thời gian upload. Đảm bảo có kết nối ổn định.

---

## 🚂 Bước 3: Deploy Railway

### 3.1: Tạo Account

1. Truy cập: https://railway.app
2. Click **Login** → Chọn **GitHub**
3. Authorize Railway truy cập GitHub

### 3.2: Tạo Project

1. Click **New Project**
2. Chọn **Deploy from GitHub repo**
3. Chọn repo `cookshare-chatbot`
4. Railway sẽ tự động detect và deploy

### 3.3: Set Environment Variables

1. Vào **Variables** tab
2. Thêm các biến sau:

```
GGUF_MODEL_PATH=models/cookshare.gguf
PORT=7860
```

### 3.4: Chờ Deploy

- Railway sẽ tự động:
  - Build Docker image
  - Cài dependencies
  - Download model từ GitHub
  - Start server

**Thời gian:** ~5-10 phút (tùy tốc độ download model)

---

## 🧪 Bước 4: Test API

### 4.1: Lấy URL

Sau khi deploy xong, Railway sẽ cung cấp URL:
- Ví dụ: `https://cookshare-chatbot-production.up.railway.app`

### 4.2: Test Health Endpoint

```bash
curl https://YOUR_APP_URL.railway.app/health
```

**Kết quả mong đợi:**
```json
{"status": "healthy"}
```

### 4.3: Test Chat Endpoint

```bash
curl -X POST https://YOUR_APP_URL.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Xin chào!",
    "history": []
  }'
```

**Kết quả mong đợi:**
```json
{
  "response": "Chào bạn! Tôi có thể giúp gì?",
  "success": true
}
```

---

## 🔗 Bước 5: Kết Nối React Native

### 5.1: Update API URL

Trong React Native app, update API endpoint:

```javascript
const API_URL = "https://YOUR_APP_URL.railway.app";
```

### 5.2: Test Kết Nối

```javascript
// Test connection
fetch(`${API_URL}/health`)
  .then(res => res.json())
  .then(data => console.log(data));

// Chat
fetch(`${API_URL}/chat`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: "Xin chào!",
    history: []
  })
})
  .then(res => res.json())
  .then(data => console.log(data.response));
```

---

## 🆘 Troubleshooting

### Lỗi: "Model not found"
→ Kiểm tra `GGUF_MODEL_PATH` environment variable

### Lỗi: "Build failed"
→ Check logs trong Railway dashboard

### Lỗi: "Out of memory"
→ Model quá lớn, cần upgrade Railway plan hoặc quantize model nhỏ hơn

### Lỗi: "Timeout"
→ Railway free tier có giới hạn, nên upgrade hoặc optimize model

---

## 💰 Chi Phí

- **Railway Hobby Plan:** $5/month
- **Model size:** 948MB (fit trong 8GB RAM)
- **Total:** $5/month

---

## ✅ Checklist Sau Khi Deploy

- [ ] Health endpoint trả về `{"status": "healthy"}`
- [ ] Chat endpoint hoạt động
- [ ] React Native app kết nối được
- [ ] Test end-to-end trong app

---

**🎉 Chúc mừng! Chatbot đã sẵn sàng!**

