# src/utils/io_utils.py
import os
import requests
from PIL import Image, ImageDraw
import io


def generate_ai_image_free(prompt, filename, folder="results/images"):
    """
    FREE AI image generation with local model as primary option
    """
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, f"{filename}.png")

    # Try CPU-optimized generation first (most compatible)
    try:
        print("🚀 Attempting CPU-optimized AI image generation...")
        local_path = generate_local_free_cpu(prompt, filepath)
        if local_path and os.path.exists(local_path):
            print("✅ CPU-optimized AI image generated successfully!")
            return local_path
    except Exception as e:
        print(f"❌ CPU generation failed: {e}")

    # Try regular local generation (for GPU users)
    try:
        print("🎮 Attempting GPU AI image generation...")
        local_path = generate_local_free(prompt, filepath)
        if local_path and os.path.exists(local_path):
            print("✅ GPU AI image generated successfully!")
            return local_path
    except Exception as e:
        print(f"❌ GPU generation failed: {e}")

    # Fallback to Hugging Face API
    try:
        print("🌐 Trying Hugging Face API...")
        api_path = generate_with_huggingface_api(prompt, filepath)
        if api_path:
            return api_path
    except Exception as e:
        print(f"❌ API generation failed: {e}")

    # Final fallback - create nice placeholder
    return create_ai_placeholder(prompt, filepath)


def generate_local_free_cpu(prompt, filepath):
    """
    CPU-optimized version for low memory systems
    """
    try:
        from diffusers import StableDiffusionPipeline
        import torch

        # Force CPU and smaller settings
        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float32,
            safety_checker=None,
            requires_safety_checker=False
        )

        # Use CPU
        pipe = pipe.to("cpu")

        # Very conservative settings for CPU
        image = pipe(
            prompt=prompt,
            width=384,  # Even smaller
            height=384,
            num_inference_steps=10,  # Fewer steps
            guidance_scale=6.0
        ).images[0]

        image.save(filepath)
        return filepath

    except Exception as e:
        print(f"CPU generation failed: {e}")
        return None


def generate_local_free(prompt, filepath):
    """
    Completely free local generation (original version for GPU users)
    """
    try:
        from diffusers import StableDiffusionPipeline
        import torch

        # Use CPU if no GPU
        device = "cuda" if torch.cuda.is_available() else "cpu"

        # Smaller model for less RAM usage
        model_id = "runwayml/stable-diffusion-v1-5"

        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float32,
            safety_checker=None,
            requires_safety_checker=False
        )

        if device == "cpu":
            pipe = pipe.to(device)
        else:
            pipe = pipe.to(device)
            pipe.enable_attention_slicing()  # Reduce VRAM usage

        # Generate
        image = pipe(
            prompt=prompt,
            width=512,  # Smaller for faster generation
            height=512,
            num_inference_steps=15,  # Fewer steps = faster
            guidance_scale=7.0
        ).images[0]

        image.save(filepath)
        return filepath

    except Exception as e:
        print(f"Local generation failed: {e}")
        return None


def generate_with_huggingface_api(prompt, filepath):
    """
    Fallback: Hugging Face API
    """
    try:
        API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

        # Try without token first, then with token if available
        headers = {}

        response = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=60)

        if response.status_code == 200:
            image = Image.open(io.BytesIO(response.content))
            image.save(filepath)
            print("✅ API image generated successfully!")
            return filepath
        else:
            raise Exception(f"API returned {response.status_code}")

    except Exception as e:
        raise Exception(f"API error: {e}")


def create_ai_placeholder(prompt, filepath):
    """Create an attractive AI-themed placeholder"""
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color='#667eea')
    d = ImageDraw.Draw(img)

    # Add gradient effect
    for i in range(height):
        r = int(102 + (154 - 102) * i / height)
        g = int(126 + (206 - 126) * i / height)
        b = int(234 + (250 - 234) * i / height)
        d.line([(0, i), (width, i)], fill=(r, g, b))

    # Add content
    lines = [
        "🎨 AI IMAGE GENERATION",
        f'Prompt: "{prompt[:70]}..."',
        "",
        "Status: Trying Local AI Models",
        "CPU & GPU Optimized Versions",
        "Install: pip install diffusers torch"
    ]

    y = 50
    for line in lines:
        d.text((50, y), line, fill='white')
        y += 40

    # Add border
    d.rectangle([40, 30, width - 40, height - 30], outline='white', width=3)

    img.save(filepath)
    print("📝 Created AI-themed placeholder")
    return filepath


# Utility functions for saving other data
def save_json(data, filename, folder="results/exports"):
    """Save scene analysis as JSON"""
    import json
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return filepath
    except Exception as e:
        print(f"Could not save JSON: {e}")
        return None


def save_text_log(message, folder="results/logs"):
    """Save log message"""
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, "app.log")

    try:
        with open(filepath, 'a') as f:
            f.write(f"{message}\n")
    except Exception:
        pass