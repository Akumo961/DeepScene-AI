# app.py (FastAPI only)
from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_loader import SceneDataLoader
from src.preprocess import TextPreprocessor
from src.train import DeepSceneModels

# Setup
app = FastAPI(title="DeepScene API", version="0.1")

# Initialize components
data_loader = SceneDataLoader(data_dir="data")
preprocessor = TextPreprocessor()
models = DeepSceneModels().initialize_all_models()

# Request/Response Models
class SceneRequest(BaseModel):
    description: str

class SceneResponse(BaseModel):
    genre: str
    style: str
    characters: list
    setting: str
    mood: dict
    dialogue: str
    image_prompt: str

# API Routes
@app.get("/")
def root():
    return {"message": "Welcome to DeepScene API 🚀"}

@app.post("/analyze_scene", response_model=SceneResponse)
def analyze_scene(req: SceneRequest):
    # Your existing FastAPI logic here...
    pass