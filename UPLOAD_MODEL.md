# 📤 Hướng Dẫn Upload Model lên Railway

File `cookshare.gguf` (948MB) quá lớn để push lên GitHub (>100MB limit).

**Giải pháp:** Upload trực tiếp lên Railway khi deploy.

---

## 🚀 Cách 1: Upload qua Railway Dashboard (Đơn giản nhất)

1. **Deploy code lên Railway:**
   - Railway sẽ clone code từ GitHub
   - Build Docker image
   - Nhưng **chưa có file model**

2. **Upload file model:**
   - Vào Railway Dashboard → Service của bạn
   - Vào tab **"Files"** hoặc **"Volumes"**
   - Upload file `cookshare.gguf` vào thư mục `models/`
   - Hoặc dùng Railway CLI:
     ```bash
     railway upload models/cookshare.gguf
     ```

---

## 🚀 Cách 2: Dùng Railway CLI (Nhanh hơn)

1. **Cài Railway CLI:**
   ```bash
   npm i -g @railway/cli
   ```

2. **Login:**
   ```bash
   railway login
   ```

3. **Link project:**
   ```bash
   cd F:\modelllmchatbot
   railway link
   ```

4. **Upload file model:**
   ```bash
   railway upload models/cookshare.gguf
   ```

---

## 🚀 Cách 3: Download từ Cloud Storage (Tự động)

Nếu bạn upload file lên Google Drive / Dropbox, có thể thêm script download trong Dockerfile:

```dockerfile
# Download model từ cloud storage
RUN curl -L "YOUR_GOOGLE_DRIVE_LINK" -o models/cookshare.gguf
```

---

## ✅ Sau khi upload

1. **Restart service trên Railway**
2. **Kiểm tra logs:** Model sẽ load khi service start
3. **Test API:** `GET /model-info` để xem model đã load chưa

---

## 📝 Lưu ý

- File `cookshare.gguf` phải ở đúng path: `models/cookshare.gguf`
- Railway sẽ tự động map PORT
- Model sẽ load khi service start (mất ~10-30 giây)

---

**Khuyến nghị:** Dùng **Cách 2 (Railway CLI)** - Nhanh và đơn giản nhất!

