# src/train.py
import torch
import random
from typing import Dict


class DeepSceneModels:
    """
    Enhanced models with better mood classification
    """

    def __init__(self, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.models = {}

        # Enhanced mood mapping
        self.mood_keywords = {
            "happy": ["happy", "joy", "celebrat", "dancing", "laugh", "smile", "fun", "party"],
            "sad": ["sad", "cry", "tear", "depressed", "lonely", "heartbreak", "loss"],
            "tense": ["tense", "suspense", "nervous", "anxious", "worried", "stress"],
            "fearful": ["fear", "scared", "afraid", "terrified", "horror", "frighten"],
            "romantic": ["romantic", "love", "passion", "intimate", "affection", "kiss"],
            "energetic": ["energy", "exciting", "dynamic", "action", "fast", "intense", "dancing"],
            "mysterious": ["mystery", "secret", "unknown", "puzzle", "curious", "enigma"],
            "peaceful": ["calm", "peace", "quiet", "serene", "tranquil", "relax"]
        }

    def initialize_all_models(self):
        """Initialize model placeholders"""
        self.models["mood_classifier"] = "stub_mood_classifier"
        self.models["dialogue_generator"] = "stub_dialogue_generator"
        self.models["tts"] = "stub_text_to_speech"
        self.models["image_gen"] = "stub_image_gen"
        return self

    def classify_scene_mood(self, description: str) -> Dict[str, any]:
        """
        Enhanced mood classification based on keywords and context
        """
        description_lower = description.lower()

        # Score each mood based on keyword matches
        mood_scores = {}

        for mood, keywords in self.mood_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in description_lower:
                    score += 1
                    # Bonus for exact matches
                    if f" {keyword} " in f" {description_lower} ":
                        score += 2

            mood_scores[mood] = score

        # Get mood with highest score
        best_mood = max(mood_scores.items(), key=lambda x: x[1])

        # If no strong match, use context-based fallback
        if best_mood[1] == 0:
            detected_mood = self._context_based_mood(description_lower)
            confidence = 0.6
        else:
            detected_mood = best_mood[0]
            confidence = min(0.95, 0.7 + (best_mood[1] * 0.1))

        return {"mood": detected_mood, "confidence": round(confidence, 2)}

    def _context_based_mood(self, description: str) -> str:
        """Context-based mood fallback"""
        if any(word in description for word in ["dancing", "dance", "party", "celebrat"]):
            return "happy"
        elif any(word in description for word in ["fight", "battle", "chase"]):
            return "tense"
        elif any(word in description for word in ["love", "romantic", "kiss"]):
            return "romantic"
        else:
            return random.choice(["happy", "energetic", "peaceful"])

    def generate_dialogue(self, description: str) -> str:
        """Enhanced dialogue generation"""
        # Simple template-based dialogue generation
        templates = [
            f"\"This is quite a situation,\" one character remarked, looking around.",
            f"\"I can't believe we're here,\" said another, shaking their head.",
            f"\"What should we do now?\" someone asked nervously.",
            f"\"This reminds me of that time...\" a voice trailed off.",
            f"\"Let's make the most of this moment!\" someone exclaimed cheerfully."
        ]

        # Context-aware selection
        description_lower = description.lower()
        if "dancing" in description_lower or "dance" in description_lower:
            return "\"I love this song! Let's dance!\" they shouted over the music."
        elif "fight" in description_lower:
            return "\"You'll never get away with this!\" the hero declared."
        elif "love" in description_lower:
            return "\"I've never felt this way about anyone before,\" they whispered."

        return random.choice(templates)

    def generate_tts(self, text: str):
        """Stub for TTS"""
        return f"[Audio for text: '{text[:50]}...']"

    def generate_image(self, prompt: str):
        """Stub for image generation"""
        return f"[Generated image for prompt: '{prompt[:60]}...']"