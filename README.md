# Drug Interaction Backend API

Backend API cho dự đoán tương tác thuốc sử dụng GraphSAGE và Edge Predictor models.

## 🚀 Quick Start

### Local Development

```bash
# Clone repo
git clone <your-repo-url>
cd drug-interaction-backend

# Tạo virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate.ps1

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

Server sẽ chạy tại: http://localhost:8000

## 📦 Deploy lên Railway

### Option 1: Deploy từ GitHub (Recommended)

1. Push code lên GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. Vào https://railway.app
3. Click **New Project**
4. Chọn **Deploy from GitHub repo**
5. Chọn repo này
6. Railway sẽ tự động detect Python và deploy

### Option 2: Deploy từ CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

## 🔧 Environment Variables

Railway sẽ tự động set `PORT` environment variable.

Nếu cần thêm CORS origins, thêm trong Railway dashboard:
```
ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-domain.com
```

## 📡 API Endpoints

### POST /predict
Dự đoán tương tác giữa 2 thuốc

**Request:**
```json
{
  "drug1": "Aspirin",
  "drug2": "Warfarin",
  "model": "graphsage"
}
```

**Response:**
```json
{
  "drug1": "Aspirin",
  "drug2": "Warfarin",
  "interaction_probability": 0.85,
  "risk_level": "High",
  "model_used": "graphsage"
}
```

### GET /
Health check

### GET /drugs
Lấy danh sách tất cả thuốc

## 🗂️ Cấu trúc Files

```
drug-interaction-backend/
├── server.py                          # FastAPI application
├── requirements.txt                   # Python dependencies
├── Procfile                           # Railway start command
├── railway.json                       # Railway config
├── runtime.txt                        # Python version
├── .gitignore                         # Git ignore
├── README.md                          # Documentation
└── data/                              # Data files
    ├── drug_tfidf_reduced_128d.csv    # TF-IDF embeddings
    ├── graphsage.pt                   # GraphSAGE model
    └── edge_predictor.pt              # Edge Predictor model
```

## 🐛 Troubleshooting

### Model loading fails
- Nếu .pt files là state_dict, backend sẽ tự động fallback về cosine similarity
- Check logs: `railway logs`

### CORS errors
- Thêm frontend URL vào `ALLOWED_ORIGINS` environment variable
- Hoặc update `server.py` trực tiếp

### Port issues
- Railway tự động set PORT, không cần config

## 📝 Notes

- Backend tự động detect và load GraphSAGE/Edge Predictor models
- Fallback về cosine similarity nếu PyTorch models không load được
- Hỗ trợ CORS cho multiple origins
- Health check endpoint tại `/`

## 🔗 Links

- Frontend: https://your-app.vercel.app
- Backend API: https://your-backend.railway.app
- API Docs: https://your-backend.railway.app/docs

## 📄 License

MIT
