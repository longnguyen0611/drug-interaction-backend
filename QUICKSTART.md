# 🚀 Quick Deploy Guide

## ✅ Backend đã sẵn sàng deploy lên Railway!

### 📁 Cấu trúc
```
drug-interaction-backend/
├── server.py              # FastAPI application
├── requirements.txt       # Python dependencies
├── Procfile              # Railway start command
├── railway.json          # Railway config
├── runtime.txt           # Python 3.11
├── .gitattributes        # Git LFS for .pt files
├── README.md             # Full documentation
├── DEPLOY.md             # Deployment guide
├── setup.ps1             # Local setup script
├── test.bat              # Test script
└── data/                 # ✅ Data files (41.67 MB CSV + models)
    ├── drug_tfidf_reduced_128d.csv
    ├── graphsage.pt
    └── edge_predictor.pt
```

---

## 🎯 Deploy trong 3 bước

### 1️⃣ Push lên GitHub

```bash
cd drug-interaction-backend

# Init git
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub: https://github.com/new
# Then push:
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/drug-interaction-backend.git
git push -u origin main
```

### 2️⃣ Deploy lên Railway

1. Vào https://railway.app
2. **New Project** → **Deploy from GitHub repo**
3. Chọn `drug-interaction-backend`
4. Railway tự động deploy! 🎉

### 3️⃣ Copy URL và update Frontend

1. Copy Railway URL: `https://your-backend.railway.app`
2. Vào Vercel Dashboard (frontend)
3. Settings → Environment Variables
4. Add:
   ```
   NEXT_PUBLIC_PYTHON_BACKEND_URL=https://your-backend.railway.app
   ```
5. Redeploy frontend

---

## 🧪 Test Local trước khi deploy

### Windows PowerShell
```powershell
.\setup.ps1
python server.py
```

### Command Prompt
```cmd
test.bat
```

Mở browser: http://localhost:8000/docs

---

## 📊 API Endpoints

### Health Check
```bash
GET https://your-backend.railway.app/
```

### Get All Drugs
```bash
GET https://your-backend.railway.app/drugs
```

### Predict Interaction
```bash
POST https://your-backend.railway.app/predict
Content-Type: application/json

{
  "drug1": "Aspirin",
  "drug2": "Warfarin",
  "model": "graphsage"
}
```

---

## ⚙️ Environment Variables (Optional)

Railway Dashboard → Variables:

```
ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

---

## 💰 Cost

**FREE** với Railway:
- $5 credit/month
- ~500 hours runtime
- 512 MB RAM
- 1 GB storage

**Upgrade nếu cần:**
- Railway Pro: $5/month
- 8GB RAM, always-on

---

## 🔍 Troubleshooting

### Build fails
→ Đọc `DEPLOY.md` phần Troubleshooting

### CORS errors
→ Set `ALLOWED_ORIGINS` environment variable

### Models không load
→ Backend tự động fallback về cosine similarity ✅

---

## 📚 Full Documentation

- **README.md** - Complete API documentation
- **DEPLOY.md** - Detailed deployment guide
- **data/README.md** - Data files info

---

## ✨ Ready to Deploy!

Làm theo 3 bước trên là xong! 🚀

Có vấn đề gì ping mình nhé! 💬
