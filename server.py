"""
Drug Interaction Backend API
FastAPI server để load PyTorch models và tính toán predictions
Hỗ trợ GraphSAGE và Edge Predictor models
"""
import os
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import torch
import torch.nn.functional as F
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

app = FastAPI(
    title="Drug Interaction Backend API",
    description="API để dự đoán tương tác thuốc sử dụng GraphSAGE và Edge Predictor models",
    version="1.0.0"
)

# CORS configuration - support both local dev and production
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Add your Vercel frontend URL here
    # "https://your-app.vercel.app",
]

# Allow origins from environment variable (for flexibility in production)
cors_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
if cors_origins and cors_origins[0]:
    ALLOWED_ORIGINS.extend([origin.strip() for origin in cors_origins if origin.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    drug1: str
    drug2: str
    model: str = "graphsage"

class PredictResponse(BaseModel):
    drug1: str
    drug2: str
    interaction_probability: float
    risk_level: str
    model_used: str
    message: Optional[str] = None

# Global variables for models and data
graphsage_model = None
edge_predictor_model = None
drugs_df = None
node_index_map = None

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

def load_data():
    """Load CSV data và node index map"""
    global drugs_df, node_index_map
    
    try:
        csv_path = DATA_DIR / "drug_tfidf_reduced_128d.csv"
        if not csv_path.exists():
            print(f"⚠️  Warning: {csv_path} not found")
            return
        
        drugs_df = pd.read_csv(csv_path)
        print(f"✅ Loaded {len(drugs_df)} drugs from CSV")
        
        # Create node index map
        node_index_map = {drug: idx for idx, drug in enumerate(drugs_df.iloc[:, 0])}
        print(f"✅ Created node index map with {len(node_index_map)} entries")
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")

def load_graphsage_model():
    """Load GraphSAGE model"""
    global graphsage_model
    
    try:
        model_path = DATA_DIR / "graphsage.pt"
        if not model_path.exists():
            print(f"⚠️  GraphSAGE model not found at {model_path}")
            return None
        
        graphsage_model = torch.load(model_path, map_location=torch.device('cpu'))
        print(f"✅ Loaded GraphSAGE model from {model_path}")
        return graphsage_model
        
    except Exception as e:
        print(f"⚠️  Could not load GraphSAGE model: {e}")
        print("   Will use cosine similarity fallback")
        return None

def load_edge_predictor_model():
    """Load Edge Predictor model"""
    global edge_predictor_model
    
    try:
        model_path = DATA_DIR / "edge_predictor.pt"
        if not model_path.exists():
            print(f"⚠️  Edge Predictor model not found at {model_path}")
            return None
        
        edge_predictor_model = torch.load(model_path, map_location=torch.device('cpu'))
        print(f"✅ Loaded Edge Predictor model from {model_path}")
        return edge_predictor_model
        
    except Exception as e:
        print(f"⚠️  Could not load Edge Predictor model: {e}")
        print("   Will use cosine similarity fallback")
        return None

def cosine_sim(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """Tính cosine similarity giữa 2 embeddings"""
    embedding1 = embedding1.reshape(1, -1)
    embedding2 = embedding2.reshape(1, -1)
    similarity = cosine_similarity(embedding1, embedding2)[0][0]
    # Convert to probability (0-1 range)
    probability = (similarity + 1) / 2
    return float(probability)

def get_risk_level(probability: float) -> str:
    """Xác định mức độ rủi ro dựa vào probability"""
    if probability >= 0.8:
        return "Rất cao (Very High)"
    elif probability >= 0.6:
        return "Cao (High)"
    elif probability >= 0.4:
        return "Trung bình (Medium)"
    elif probability >= 0.2:
        return "Thấp (Low)"
    else:
        return "Rất thấp (Very Low)"

def find_drug(drug_name: str) -> Optional[pd.Series]:
    """Tìm thuốc trong dataset (case-insensitive)"""
    if drugs_df is None:
        return None
    
    # Case-insensitive search
    drug_name_lower = drug_name.lower()
    mask = drugs_df.iloc[:, 0].str.lower() == drug_name_lower
    
    if mask.any():
        return drugs_df[mask].iloc[0]
    return None

@app.on_event("startup")
async def startup_event():
    """Load models khi server start"""
    print("🚀 Starting Drug Interaction Backend API...")
    print(f"📁 Data directory: {DATA_DIR}")
    
    load_data()
    load_graphsage_model()
    load_edge_predictor_model()
    
    print("✅ Server ready!")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Drug Interaction Backend API",
        "version": "1.0.0",
        "models": {
            "graphsage": graphsage_model is not None,
            "edge_predictor": edge_predictor_model is not None,
        },
        "data_loaded": drugs_df is not None,
        "total_drugs": len(drugs_df) if drugs_df is not None else 0
    }

@app.get("/drugs", response_model=List[str])
async def get_drugs():
    """Lấy danh sách tất cả thuốc"""
    if drugs_df is None:
        raise HTTPException(status_code=500, detail="Drug data not loaded")
    
    return drugs_df.iloc[:, 0].tolist()

@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    """
    Dự đoán tương tác giữa 2 thuốc
    
    Models:
    - graphsage: GraphSAGE neural network
    - edge_predictor: Edge Predictor model
    """
    if drugs_df is None:
        raise HTTPException(status_code=500, detail="Drug data not loaded")
    
    # Find drugs
    drug1_data = find_drug(request.drug1)
    drug2_data = find_drug(request.drug2)
    
    if drug1_data is None:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy thuốc: {request.drug1}")
    
    if drug2_data is None:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy thuốc: {request.drug2}")
    
    # Get embeddings (skip first column which is drug name)
    embedding1 = drug1_data.iloc[1:].values.astype(float)
    embedding2 = drug2_data.iloc[1:].values.astype(float)
    
    probability = 0.0
    message = None
    
    # GraphSAGE model
    if request.model == "graphsage":
        if graphsage_model is not None:
            try:
                # Convert to tensors
                emb1_tensor = torch.tensor(embedding1, dtype=torch.float32).unsqueeze(0)
                emb2_tensor = torch.tensor(embedding2, dtype=torch.float32).unsqueeze(0)
                
                # Get predictions from model
                with torch.no_grad():
                    if hasattr(graphsage_model, 'forward'):
                        # Concatenate embeddings
                        combined = torch.cat([emb1_tensor, emb2_tensor], dim=1)
                        output = graphsage_model(combined)
                        probability = torch.sigmoid(output).item()
                    else:
                        # Model might be state_dict only, use cosine similarity
                        probability = cosine_sim(embedding1, embedding2)
                        message = "Using cosine similarity (GraphSAGE model structure not available)"
            except Exception as e:
                print(f"Error using GraphSAGE model: {e}")
                probability = cosine_sim(embedding1, embedding2)
                message = f"Fallback to cosine similarity (GraphSAGE error: {str(e)})"
        else:
            probability = cosine_sim(embedding1, embedding2)
            message = "GraphSAGE model not available, using cosine similarity"
    
    # Edge Predictor model
    elif request.model == "edge_predictor":
        if edge_predictor_model is not None:
            try:
                # Convert to tensors
                emb1_tensor = torch.tensor(embedding1, dtype=torch.float32).unsqueeze(0)
                emb2_tensor = torch.tensor(embedding2, dtype=torch.float32).unsqueeze(0)
                
                # Get predictions from model
                with torch.no_grad():
                    if hasattr(edge_predictor_model, 'forward'):
                        # Concatenate embeddings
                        combined = torch.cat([emb1_tensor, emb2_tensor], dim=1)
                        output = edge_predictor_model(combined)
                        probability = torch.sigmoid(output).item()
                    else:
                        # Model might be state_dict only, use cosine similarity
                        probability = cosine_sim(embedding1, embedding2)
                        message = "Using cosine similarity (Edge Predictor model structure not available)"
            except Exception as e:
                print(f"Error using Edge Predictor model: {e}")
                probability = cosine_sim(embedding1, embedding2)
                message = f"Fallback to cosine similarity (Edge Predictor error: {str(e)})"
        else:
            probability = cosine_sim(embedding1, embedding2)
            message = "Edge Predictor model not available, using cosine similarity"
    
    else:
        raise HTTPException(status_code=400, detail=f"Invalid model: {request.model}")
    
    risk_level = get_risk_level(probability)
    
    return PredictResponse(
        drug1=request.drug1,
        drug2=request.drug2,
        interaction_probability=round(probability, 4),
        risk_level=risk_level,
        model_used=request.model,
        message=message
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
