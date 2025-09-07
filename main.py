from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
from pathlib import Path

import sys

app = FastAPI()

MODEL_DIR = Path(__file__).parent / "Models"

@app.get("/categories")
def list_categories():
    categories = [f.name for f in MODEL_DIR.iterdir() if f.is_dir()]
    return JSONResponse(content={"categories": categories})

@app.get("/models/{category}")
def list_models_in_category(category : str):
    category_path = MODEL_DIR / category
    if not category_path.exists() or not category_path.is_dir():
        return JSONResponse(content={"error" : "Category not found"}, status_code=404)
    
    bundles = [f.name for f in category_path.glob("*")]
    return JSONResponse(content={"bundles": bundles})

@app.get("/download/{category}/{bundle_name}")
def download_bundle(category: str, bundle_name: str):
    file_path = MODEL_DIR / category / bundle_name
    if file_path.exists():
        return FileResponse(file_path, media_type='application/octet-stream')
    return JSONResponse(content={"error": "File not found"}, status_code=404)

if __name__ == "__main__":
    port = 5000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print ("Invalid port number. Using default 5000")
    uvicorn.run(app, host="0.0.0.0", port=5000)