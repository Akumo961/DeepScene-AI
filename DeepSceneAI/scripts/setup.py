setup_script = '''
#!/usr/bin/env python3
"""
DeepScene Setup Script
Handles initial setup, model downloads, and environment verification
"""

import os
import sys
import subprocess
import urllib.request
from pathlib import Path
import json

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def create_directories():
    """Create necessary project directories"""
    directories = [
        "data", "models", "results", "notebooks", 
        "results/images", "results/exports", "results/logs"
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def install_requirements():
    """Install Python requirements"""
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        sys.exit(1)

def check_gpu_availability():
    """Check GPU availability"""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            gpu_name = torch.cuda.get_device_name(0)
            print(f"✅ GPU available: {gpu_name} (Count: {gpu_count})")
            return True
        else:
            print("⚠️ No GPU detected, will use CPU (slower)")
            return False
    except ImportError:
        print("⚠️ PyTorch not installed, cannot check GPU")
        return False

def download_sample_data():
    """Download sample scene templates and data"""
    sample_data = {
        "scene_templates": [
            {
                "id": 1,
                "description": "A tense confrontation in a dimly lit warehouse",
                "genre": "thriller",
                "characters": ["Detective", "Suspect"],
                "expected_mood": "tense"
            },
            {
                "id": 2, 
                "description": "A romantic dinner under candlelight",
                "genre": "romance",
                "characters": ["Lover1", "Lover2"],
                "expected_mood": "romantic"
            },
            {
                "id": 3,
                "description": "An epic battle on a mountain peak",
                "genre": "action", 
                "characters": ["Hero", "Villain", "Dragon"],
                "expected_mood": "epic"
            }
        ]
    }

    with open("data/sample_scenes.json", "w") as f:
        json.dump(sample_data, f, indent=2)

    print("✅ Sample data created")

def verify_installation():
    """Verify that key components can be imported"""
    try:
        import streamlit
        import torch
        import transformers
        import diffusers
        print("✅ Core libraries verified")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def create_env_file():
    """Create environment configuration file"""
    env_content = """# DeepScene Environment Configuration
PYTHONPATH=.
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost

# Model Configuration
DEFAULT_IMAGE_WIDTH=1024
DEFAULT_IMAGE_HEIGHT=576
DEFAULT_INFERENCE_STEPS=20

# Cache Settings
HF_HOME=./models/huggingface
TRANSFORMERS_CACHE=./models/transformers

# Logging
LOG_LEVEL=INFO
LOG_FILE=results/logs/deepscene.log
"""

    with open(".env", "w") as f:
        f.write(env_content)

    print("✅ Environment file created")

def main():
    """Main setup process"""
    print("🚀 Starting DeepScene Setup...")

    check_python_version()
    create_directories()
    install_requirements()
    has_gpu = check_gpu_availability()
    download_sample_data()
    create_env_file()

    if verify_installation():
        print("\\n🎉 Setup completed successfully!")
        print("\\nNext steps:")
        print("1. Run 'streamlit run app.py' to start the application")
        print("2. Open http://localhost:8501 in your browser")
        print("3. Check out the notebooks/ folder for experiments")

        if not has_gpu:
            print("\\n⚠️ Note: Running on CPU will be slower. Consider using GPU for better performance.")
    else:
        print("\\n❌ Setup completed with errors. Check the logs above.")

if __name__ == "__main__":
    main()
'''
