# Data Files

Thư mục này chứa các files data cần thiết cho backend:

## Required Files

1. **drug_tfidf_reduced_128d.csv**
   - TF-IDF embeddings cho 18,487 thuốc
   - Mỗi thuốc có 128 dimensions
   - Copy từ: `web/data/drug_tfidf_reduced_128d.csv`

2. **graphsage.pt**
   - GraphSAGE model weights
   - Copy từ: `web/data/graphsage.pt`

3. **edge_predictor.pt**
   - Edge Predictor model weights
   - Copy từ: `web/data/edge_predictor.pt`

## Cách copy files

### Windows PowerShell
```powershell
# Copy CSV
Copy-Item "..\web\data\drug_tfidf_reduced_128d.csv" -Destination ".\data\"

# Copy models
Copy-Item "..\web\data\graphsage.pt" -Destination ".\data\"
Copy-Item "..\web\data\edge_predictor.pt" -Destination ".\data\"
```

### Command Prompt
```cmd
copy ..\web\data\drug_tfidf_reduced_128d.csv .\data\
copy ..\web\data\graphsage.pt .\data\
copy ..\web\data\edge_predictor.pt .\data\
```

## Note

⚠️ **Git LFS cho files lớn**

Nếu .pt files > 100MB, cần dùng Git LFS:

```bash
# Install Git LFS
git lfs install

# Track .pt files
git lfs track "*.pt"
git add .gitattributes

# Add and commit
git add data/
git commit -m "Add model files"
```

Hoặc Railway có thể tải files từ external storage (S3, Google Drive) trong startup script.
