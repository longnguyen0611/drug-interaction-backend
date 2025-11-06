# 🚀 Hướng dẫn Deploy Backend lên Railway

## Bước 1: Chuẩn bị Repository

### 1.1 Khởi tạo Git (nếu chưa có)

```bash
cd drug-interaction-backend
git init
git add .
git commit -m "Initial commit - Drug Interaction Backend API"
```

### 1.2 Push lên GitHub

```bash
# Tạo repo mới trên GitHub: https://github.com/new
# Tên repo: drug-interaction-backend

# Sau đó:
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/drug-interaction-backend.git
git push -u origin main
```

## Bước 2: Deploy lên Railway

### Option A: Deploy từ GitHub (Recommended) ✨

1. **Đăng nhập Railway**
   - Vào https://railway.app
   - Sign in with GitHub

2. **Tạo New Project**
   - Click **New Project**
   - Chọn **Deploy from GitHub repo**
   - Authorize Railway to access your GitHub
   - Chọn repo `drug-interaction-backend`

3. **Tự động Deploy**
   - Railway sẽ tự động:
     - ✅ Detect Python
     - ✅ Install dependencies từ `requirements.txt`
     - ✅ Run command từ `Procfile`
     - ✅ Expose public URL

4. **Copy URL**
   - Sau khi deploy xong, copy URL:
   - Ví dụ: `https://drug-interaction-backend-production.up.railway.app`

### Option B: Deploy từ CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to project
railway init

# Deploy
railway up
```

## Bước 3: Set Environment Variables (Optional)

### Thêm CORS origins cho frontend

1. Vào Railway Dashboard
2. Click vào project
3. Tab **Variables**
4. Add variable:
   ```
   ALLOWED_ORIGINS=https://your-frontend.vercel.app
   ```
5. Click **Deploy** để apply changes

## Bước 4: Verify Deployment

### Test API endpoints

```bash
# Health check
curl https://your-backend.railway.app/

# Get all drugs
curl https://your-backend.railway.app/drugs

# Test prediction
curl -X POST https://your-backend.railway.app/predict \
  -H "Content-Type: application/json" \
  -d '{
    "drug1": "Aspirin",
    "drug2": "Warfarin",
    "model": "graphsage"
  }'
```

### Hoặc dùng browser

Vào: `https://your-backend.railway.app/docs`

Railway tự động generate Swagger UI để test API!

## Bước 5: Connect với Frontend

### Update Frontend Environment Variables

1. Vào Vercel Dashboard
2. Settings → Environment Variables
3. Add:
   ```
   NEXT_PUBLIC_PYTHON_BACKEND_URL=https://your-backend.railway.app
   ```
4. Redeploy frontend

## 🐛 Troubleshooting

### Build fails

**Lỗi:** `ERROR: Could not find a version that satisfies the requirement torch`

**Giải pháp:** Railway đang dùng architecture không support torch binary

Update `requirements.txt`:
```txt
--extra-index-url https://download.pytorch.org/whl/cpu
torch==2.1.1+cpu
```

### Out of memory

**Lỗi:** `Process killed (out of memory)`

**Giải pháp:** 
- Railway free tier: 512MB RAM
- PyTorch models có thể quá lớn
- Xem xét dùng Railway Pro ($5/month) hoặc optimize models

### CORS errors

**Lỗi:** `Access-Control-Allow-Origin` error

**Giải pháp:**
- Update `ALLOWED_ORIGINS` environment variable
- Hoặc sửa trực tiếp trong `server.py`:
  ```python
  ALLOWED_ORIGINS = [
      "https://your-app.vercel.app"
  ]
  ```

### Cold starts

**Hiện tượng:** Request đầu tiên chậm (5-10s)

**Giải pháp:**
- Railway free tier sleep sau 5 phút inactive
- Railway Pro có always-on option
- Hoặc setup cron job ping endpoint mỗi 4 phút

## 📊 Monitor

### View Logs

Railway Dashboard → Your Project → **Deployments** → Click deployment → **View Logs**

### Metrics

Railway Dashboard → **Metrics** tab
- CPU usage
- Memory usage
- Network traffic

## 💰 Pricing

| Plan | Price | RAM | Storage | Bandwidth |
|------|-------|-----|---------|-----------|
| **Free** | $0 | 512MB | 1GB | - |
| **Pro** | $5/mo | 8GB | 100GB | 100GB |

Free tier có $5 credit/month (≈ 500 hours runtime)

## 🎉 Done!

Backend API của bạn đã live tại:
```
https://your-backend.railway.app
```

API Docs tại:
```
https://your-backend.railway.app/docs
```

---

**Next Steps:**
1. ✅ Deploy backend lên Railway
2. ✅ Copy Railway URL
3. ✅ Update frontend `NEXT_PUBLIC_PYTHON_BACKEND_URL`
4. ✅ Redeploy frontend
5. ✅ Test full stack!
