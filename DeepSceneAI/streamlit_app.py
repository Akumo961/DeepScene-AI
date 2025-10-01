# streamlit_app.py
import streamlit as st
import sys
import os
import json
import re
from pathlib import Path

# Add src to path
sys.path.append('src')

# Initialize components with fallbacks
data_loader = None
preprocessor = None
models = None
modules_loaded = False

try:
    from src.data_loader import SceneDataLoader
    from src.preprocess import TextPreprocessor
    from src.train import DeepSceneModels

    # Try to initialize components
    try:
        data_loader = SceneDataLoader(data_dir="data")
        preprocessor = TextPreprocessor()
        models = DeepSceneModels().initialize_all_models()
        modules_loaded = True
        st.success("✅ All AI modules loaded successfully!")
    except Exception as e:
        st.warning(f"⚠️ Custom modules loaded but initialization failed: {e}")
        modules_loaded = False

except ImportError as e:
    st.warning(f"🔧 Custom modules not found: {e}")
    modules_loaded = False


# ENHANCED Fallback classes
class EnhancedFallbackDataLoader:
    def __init__(self):
        self.scene_templates = self._load_enhanced_templates()

    def _load_enhanced_templates(self):
        return {
            "comedy": {
                "keywords": ["funny", "comedy", "humor", "laugh", "absurd", "silly", "dancing", "party", "joke"],
                "style": "bright lighting, vibrant colors, energetic composition, lively atmosphere"
            },
            "action": {
                "keywords": ["fight", "chase", "explosion", "battle", "action", "combat", "run", "escape"],
                "style": "dynamic composition, high contrast, dramatic lighting, motion blur"
            },
            "drama": {
                "keywords": ["emotional", "serious", "relationship", "family", "personal", "conflict", "sad"],
                "style": "natural lighting, intimate framing, warm colors, shallow depth of field"
            },
            "romance": {
                "keywords": ["love", "romantic", "couple", "kiss", "relationship", "date", "heart"],
                "style": "soft lighting, warm colors, gentle focus, romantic atmosphere"
            },
            "horror": {
                "keywords": ["scary", "dark", "fear", "ghost", "haunted", "terror", "monster"],
                "style": "low-key lighting, high contrast, atmospheric, eerie shadows"
            },
            "thriller": {
                "keywords": ["suspense", "mystery", "tense", "danger", "conspiracy", "investigate"],
                "style": "dramatic lighting, sharp contrasts, cool colors, dynamic composition"
            },
            "musical": {
                "keywords": ["dancing", "singing", "music", "song", "dance", "performance", "stage"],
                "style": "colorful lighting, dynamic camera angles, vibrant colors, theatrical"
            }
        }

    def classify_scene_genre(self, description):
        desc_lower = description.lower()

        # Enhanced genre detection with context awareness
        genre_scores = {}

        for genre, data in self.scene_templates.items():
            score = 0
            for keyword in data["keywords"]:
                if keyword in desc_lower:
                    score += 2  # Base score for keyword match
                    # Bonus for exact word matches
                    if f" {keyword} " in f" {desc_lower} ":
                        score += 1

            genre_scores[genre] = score

        # Context-based adjustments
        if "dancing" in desc_lower or "dance" in desc_lower:
            genre_scores["musical"] += 3
            genre_scores["comedy"] += 2

        if "party" in desc_lower or "celebrat" in desc_lower:
            genre_scores["comedy"] += 2
            genre_scores["musical"] += 1

        # Get best genre
        best_genre = max(genre_scores.items(), key=lambda x: x[1])

        return best_genre[0] if best_genre[1] > 0 else "drama"

    def get_style_prompt(self, genre):
        return self.scene_templates.get(genre, {}).get("style", "cinematic style, professional photography")


class EnhancedFallbackPreprocessor:
    def extract_characters(self, description):
        # Enhanced character extraction
        characters = []
        desc_lower = description.lower()

        # Simple and reliable character detection
        if "man" in desc_lower:
            characters.append("Man")
        if "woman" in desc_lower:
            characters.append("Woman")
        if "person" in desc_lower:
            characters.append("Person")
        if "dancer" in desc_lower:
            characters.append("Dancer")
        if "detective" in desc_lower:
            characters.append("Detective")
        if "child" in desc_lower or "kid" in desc_lower:
            characters.append("Child")
        if "friend" in desc_lower:
            characters.append("Friend")

        # If no specific characters found, infer from context
        if not characters:
            if "dancing" in desc_lower:
                characters.append("Dancer")
            elif any(word in desc_lower for word in ["investigate", "crime", "mystery"]):
                characters.append("Detective")
            else:
                characters.append("Main Character")

        return characters

    def extract_setting(self, description):
        desc_lower = description.lower()

        # Enhanced setting detection with context
        setting_patterns = [
            r"(in|at|inside|on|through)\s+(?:a|an|the)?\s*([^,.!?]+?(?:room|house|building|street|park|forest|beach|office|school|restaurant|bar|club|studio|stage|theater|hall|arena))",
            r"(at|in)\s+(?:a|an|the)?\s*([^,.!?]+?(?:party|celebration|event|festival|concert))",
            r"on\s+(?:a|an|the)?\s*([^,.!?]+\s+(?:street|avenue|road|boulevard|beach|island))",
            r"in\s+(?:a|an|the)?\s*([^,.!?]+\s+(?:city|town|village|countryside|mountains|forest))"
        ]

        for pattern in setting_patterns:
            match = re.search(pattern, desc_lower)
            if match:
                setting = match.group(2).strip()
                return setting.title()

        # Context-based fallback settings
        if any(word in desc_lower for word in ["dancing", "dance", "party"]):
            return "Party Venue"
        elif any(word in desc_lower for word in ["detective", "crime", "investigate"]):
            return "City Streets"
        elif any(word in desc_lower for word in ["beach", "ocean", "sand"]):
            return "Beach"
        elif any(word in desc_lower for word in ["forest", "woods", "jungle"]):
            return "Forest"

        return "Various Locations"

    def generate_image_prompt(self, description, style):
        # Enhanced prompt generation
        prompt_parts = [
            description,
            f"cinematic style: {style}",
            "high quality, detailed, professional photography",
            "film still, dramatic composition, 4K resolution"
        ]
        return ", ".join(prompt_parts)


class EnhancedFallbackModels:
    def classify_scene_mood(self, description):
        desc_lower = description.lower()

        # Enhanced mood detection with weighted scoring
        mood_scores = {
            "happy": 0, "energetic": 0, "romantic": 0,
            "tense": 0, "mysterious": 0, "fearful": 0, "sad": 0
        }

        mood_keywords = {
            "happy": ["happy", "joy", "dancing", "laugh", "smile", "fun", "party", "celebrat", "enjoy"],
            "energetic": ["energy", "exciting", "dynamic", "dancing", "action", "fast", "intense", "vibrant"],
            "romantic": ["romantic", "love", "passion", "kiss", "affection", "heart", "date"],
            "tense": ["tense", "suspense", "nervous", "anxious", "worried", "stress", "conflict"],
            "mysterious": ["mystery", "secret", "unknown", "puzzle", "curious", "enigma", "detective"],
            "fearful": ["fear", "scared", "afraid", "terrified", "horror", "frighten", "panic"],
            "sad": ["sad", "cry", "tear", "depressed", "lonely", "heartbreak", "loss", "grief"]
        }

        # Score moods based on keyword matches
        for mood, keywords in mood_keywords.items():
            for keyword in keywords:
                if keyword in desc_lower:
                    mood_scores[mood] += 2
                    if f" {keyword} " in f" {desc_lower} ":
                        mood_scores[mood] += 1

        # Context-based adjustments
        if "dancing" in desc_lower:
            mood_scores["happy"] += 3
            mood_scores["energetic"] += 2

        if "party" in desc_lower:
            mood_scores["happy"] += 2
            mood_scores["energetic"] += 2

        # Get best mood
        best_mood = max(mood_scores.items(), key=lambda x: x[1])
        confidence = min(0.95, 0.6 + (best_mood[1] * 0.1))

        return {"mood": best_mood[0], "confidence": round(confidence, 2)}

    def generate_dialogue(self, description):
        desc_lower = description.lower()

        # Context-aware dialogue generation
        if "dancing" in desc_lower:
            dialogues = [
                "\"I love this rhythm! Let's dance all night!\" they shouted joyfully.",
                "\"This music is incredible!\" she exclaimed while moving to the beat.",
                "\"I haven't felt this alive in years!\" he laughed, spinning around."
            ]
        elif "detective" in desc_lower:
            dialogues = [
                "\"The evidence doesn't lie,\" the detective said, examining the scene.",
                "\"There's more to this case than meets the eye,\" she muttered.",
                "\"We need to find the missing piece,\" he said, looking at the clues."
            ]
        elif "love" in desc_lower or "romantic" in desc_lower:
            dialogues = [
                "\"I've never felt this way about anyone before,\" they whispered softly.",
                "\"You complete me,\" he said, looking into her eyes.",
                "\"This moment is perfect,\" she sighed contentedly."
            ]
        else:
            dialogues = [
                "\"This is quite unexpected,\" one of them remarked.",
                "\"What do you think we should do now?\" someone asked.",
                "\"I have a feeling this is just the beginning,\" they said thoughtfully."
            ]

        import random
        return random.choice(dialogues)


# Use enhanced fallbacks if custom modules failed to initialize properly
if not modules_loaded or data_loader is None:
    data_loader = EnhancedFallbackDataLoader()
    preprocessor = EnhancedFallbackPreprocessor()
    models = EnhancedFallbackModels()
    st.info("🎭 Using enhanced fallback mode with improved analysis")


# Simple file utilities
def save_fallback_json(data, filename, folder="results/exports"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return filepath
    except Exception as e:
        st.warning(f"Could not save JSON: {e}")
        return None


def create_visual_placeholder(genre, mood, description, folder="results/images"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, f"{genre}_scene.png")

    try:
        from PIL import Image, ImageDraw

        # Create a colorful placeholder based on genre and mood
        colors = {
            "comedy": "#FF6B6B", "musical": "#4ECDC4", "action": "#FFE66D",
            "drama": "#95E1D3", "romance": "#F8B195", "horror": "#6A0572",
            "thriller": "#355C7D"
        }

        bg_color = colors.get(genre, "#2E86AB")

        img = Image.new('RGB', (800, 450), color=bg_color)
        d = ImageDraw.Draw(img)

        # Add text
        title = f"{genre.upper()} SCENE"
        mood_text = f"Mood: {mood}"
        desc_preview = description[:80] + "..." if len(description) > 80 else description

        # Simple text rendering
        d.text((50, 50), title, fill='white')
        d.text((50, 100), mood_text, fill='white')
        d.text((50, 140), desc_preview, fill='white')

        # Add border
        d.rectangle([40, 40, 760, 410], outline='white', width=3)

        img.save(filepath)
        return filepath

    except Exception as e:
        st.warning(f"Could not create visual: {e}")
        return None


# Streamlit UI
st.set_page_config(
    page_title="DeepScene AI",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 DeepScene - AI Virtual Film Director")
st.write("Describe your scene and let the AI create a storyboard draft with AI-generated images!")

# Main input
description = st.text_area(
    "Enter your scene description:",
    placeholder="Example: A man dancing happily at a party with friends...",
    height=100,
    key="scene_input"
)

if st.button("🎯 Analyze Scene", type="primary"):
    if description and description.strip():
        with st.spinner("🤖 Analyzing your scene..."):
            try:
                # Step 1: Genre & Style
                genre = data_loader.classify_scene_genre(description)
                style = data_loader.get_style_prompt(genre)

                # Step 2: Extract features
                characters = preprocessor.extract_characters(description)
                setting = preprocessor.extract_setting(description)
                image_prompt = preprocessor.generate_image_prompt(description, style)

                # Step 3: Models
                mood = models.classify_scene_mood(description)
                dialogue = models.generate_dialogue(description)

                # Package result
                scene_result = {
                    "description": description,
                    "genre": genre,
                    "style": style,
                    "characters": characters,
                    "setting": setting,
                    "mood": mood,
                    "dialogue": dialogue,
                    "image_prompt": image_prompt,
                }

                # Save outputs
                saved_file = save_fallback_json(scene_result, filename=f"{genre}_scene.json")
                if saved_file:
                    st.success(f"💾 Analysis saved to: {saved_file}")

                # Display Results
                st.success("✅ Scene analysis complete!")

                # Results in columns
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("🎭 Genre", genre)
                    st.metric("📍 Setting", setting)

                with col2:
                    st.metric("👥 Characters", len(characters))
                    st.metric("😄 Mood", mood['mood'])

                with col3:
                    st.metric("🎯 Confidence", f"{mood['confidence'] * 100:.0f}%")

                # Characters list
                if characters:
                    st.subheader("👥 Characters Identified")
                    for i, character in enumerate(characters, 1):
                        st.write(f"{i}. {character}")

                # Style
                st.subheader("🎨 Visual Style")
                st.write(style)

                # Dialogue
                st.subheader("💬 Generated Dialogue")
                st.write(dialogue)

                # Mood details
                st.subheader("😄 Mood Analysis")
                st.json(mood)

                # Image prompt
                st.subheader("🖼️ Image Prompt")
                st.code(image_prompt, language="text")

                # Display AI-generated image
                try:
                    from src.utils.io_utils import generate_ai_image_free

                    with st.spinner("🎨 Generating AI image locally (FREE)..."):
                        image_path = generate_ai_image_free(
                            prompt=image_prompt,
                            filename=f"{genre}_scene"
                        )

                        if image_path and os.path.exists(image_path):
                            st.image(image_path, caption="AI-Generated Scene", use_container_width=True)

                            # Check what type of image was generated
                            if "placeholder" not in image_path.lower():
                                st.success("✨ AI image generated locally for FREE!")

                                # Show generation info
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("Model", "Stable Diffusion v1.5")
                                with col2:
                                    st.metric("Method", "Local Generation")
                            else:
                                st.info("🔄 Enable local AI: pip install diffusers torch")

                        else:
                            st.warning("⚠️ Could not generate AI image")

                except Exception as e:
                    st.error(f"❌ Image generation error: {e}")
                    # Ultimate fallback
                    st.info("🖼️ Install: pip install diffusers torch transformers")

            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                st.info("Please check your scene description and try again.")
    else:
        st.warning("⚠️ Please enter a scene description before analyzing.")

# Add some helpful info
st.markdown("---")
st.markdown("### 💡 Try These Examples:")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💃 Dancing Scene", use_container_width=True):
        st.session_state.scene_input = "A man dancing joyfully at a colorful party with friends"

with col2:
    if st.button("🕵️ Detective Scene", use_container_width=True):
        st.session_state.scene_input = "A detective investigates a mysterious crime in a rainy city at night"

with col3:
    if st.button("💕 Romantic Scene", use_container_width=True):
        st.session_state.scene_input = "Two lovers share their first kiss on a moonlit beach at sunset"

st.markdown("---")
st.markdown("### 🔧 System Status")
st.write(f"**Custom Modules:** {'✅ Loaded' if modules_loaded else '🔧 Using Fallback'}")
st.write(f"**AI Image Generation:** {'✅ Available' if modules_loaded else '🔧 Install dependencies'}")

st.markdown("### 📦 Required for AI Images:")
st.code("pip install diffusers transformers accelerate torch torchvision")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "DeepScene AI • Virtual Film Director • Powered by Streamlit & Stable Diffusion"
    "</div>",
    unsafe_allow_html=True
)