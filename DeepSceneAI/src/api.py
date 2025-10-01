fastapi_backend = '''
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import asyncio
from datetime import datetime
import json
import os

# Import our models
from train import DeepSceneModels
from data_loader import SceneDataLoader
from preprocess import TextPreprocessor

app = FastAPI(
    title="DeepScene API",
    description="AI-Powered Virtual Film Director Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instance
models = None
data_loader = SceneDataLoader()
text_processor = TextPreprocessor()

# Pydantic models
class SceneRequest(BaseModel):
    description: str
    style: Optional[str] = None
    width: int = 1024
    height: int = 576
    num_variations: int = 1

class SceneResponse(BaseModel):
    id: str
    description: str
    genre: str
    style: str
    dialogue: str
    mood: Dict[str, Any]
    characters: List[str]
    setting: str
    generation_time: float
    timestamp: str

class ProjectResponse(BaseModel):
    project_id: str
    scenes: List[SceneResponse]
    total_scenes: int
    created_at: str
    updated_at: str

@app.on_event("startup")
async def startup_event():
    """Initialize AI models on startup"""
    global models
    try:
        models = DeepSceneModels().initialize_all_models()
        print("✅ AI models initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing models: {e}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "DeepScene API is running",
        "version": "1.0.0",
        "status": "healthy",
        "models_loaded": models is not None
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models": {
            "image_generation": "image_gen" in (models.pipelines if models else {}),
            "text_generation": "text_gen" in (models.pipelines if models else {}),
            "classification": "classifier" in (models.pipelines if models else {}),
            "tts": "tts" in (models.pipelines if models else {})
        }
    }

@app.post("/generate-scene", response_model=SceneResponse)
async def generate_scene(request: SceneRequest):
    """Generate a complete scene from description"""
    if not models:
        raise HTTPException(status_code=503, detail="AI models not loaded")

    start_time = datetime.now()

    try:
        # Analyze scene
        genre = data_loader.classify_scene_genre(request.description)
        style = request.style or data_loader.get_style_prompt(genre)
        characters = text_processor.extract_characters(request.description)
        setting = text_processor.extract_setting(request.description)

        # Generate image prompt
        image_prompt = text_processor.generate_image_prompt(request.description, style)

        # Generate content
        image = models.generate_scene_image(
            image_prompt,
            width=request.width,
            height=request.height
        )

        dialogue = models.generate_dialogue(request.description)
        mood = models.classify_scene_mood(request.description)

        generation_time = (datetime.now() - start_time).total_seconds()

        # Save image temporarily (in production, use proper storage)
        scene_id = f"scene_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        response = SceneResponse(
            id=scene_id,
            description=request.description,
            genre=genre,
            style=style,
            dialogue=dialogue,
            mood=mood,
            characters=characters,
            setting=setting,
            generation_time=generation_time,
            timestamp=datetime.now().isoformat()
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scene generation failed: {str(e)}")

@app.get("/genres")
async def get_available_genres():
    """Get list of supported genres"""
    return {
        "genres": list(data_loader.scene_templates.keys()),
        "templates": data_loader.scene_templates
    }

@app.post("/analyze-text")
async def analyze_text(text: str):
    """Analyze text for characters, setting, and genre"""
    genre = data_loader.classify_scene_genre(text)
    characters = text_processor.extract_characters(text)
    setting = text_processor.extract_setting(text)

    return {
        "text": text,
        "genre": genre,
        "characters": characters,
        "setting": setting,
        "suggested_style": data_loader.get_style_prompt(genre)
    }

@app.get("/models/status")
async def get_models_status():
    """Get status of all AI models"""
    if not models:
        return {"status": "not_loaded", "models": {}}

    return {
        "status": "loaded",
        "device": models.device,
        "models": {
            "image_generation": "image_gen" in models.pipelines,
            "text_generation": "text_gen" in models.pipelines,
            "classification": "classifier" in models.pipelines,
            "tts": "tts" in models.pipelines
        },
        "pipeline_count": len(models.pipelines)
    }

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=1
    )
'''