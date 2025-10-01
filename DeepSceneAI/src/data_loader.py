# src/data_loader.py
import json
from pathlib import Path
import random
from typing import Dict, List


class SceneDataLoader:
    """
    Enhanced scene data loader with improved genre classification
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.templates = self._load_json("scene_templates.json")
        self.samples = self._load_json("sample_scenes.json")

        # Enhanced keyword mapping for better classification
        self.genre_keywords = self._build_enhanced_keywords()

    def _load_json(self, filename: str):
        file_path = self.data_dir / filename
        if not file_path.exists():
            print(f"⚠️ File not found: {file_path}, using empty fallback")
            return {}
        with open(file_path, "r") as f:
            return json.load(f)

    def _build_enhanced_keywords(self) -> Dict[str, List[str]]:
        """Build enhanced keyword mapping for better genre detection"""
        enhanced_keywords = {}

        for genre, values in self.templates.items():
            base_keywords = values.get("keywords", [])
            enhanced_keywords[genre] = base_keywords

            # Add common variations and related words
            if genre == "comedy":
                enhanced_keywords[genre].extend(["funny", "laugh", "joke", "humorous", "comic", "silly", "hilarious"])
            elif genre == "action":
                enhanced_keywords[genre].extend(["fight", "battle", "chase", "explosion", "combat", "thrilling"])
            elif genre == "romance":
                enhanced_keywords[genre].extend(["love", "romantic", "couple", "relationship", "kiss", "date"])
            elif genre == "horror":
                enhanced_keywords[genre].extend(["scary", "frightening", "terrifying", "ghost", "monster", "dark"])
            elif genre == "drama":
                enhanced_keywords[genre].extend(["emotional", "serious", "intense", "relationship", "conflict"])
            elif genre == "thriller":
                enhanced_keywords[genre].extend(["suspense", "mystery", "tense", "suspenseful", "conspiracy"])

        return enhanced_keywords

    def get_templates(self):
        return self.templates

    def get_samples(self):
        return self.samples

    def classify_scene_genre(self, description: str) -> str:
        """
        Enhanced genre classification with better keyword matching
        """
        description_lower = description.lower()

        # Score each genre based on keyword matches
        genre_scores = {}

        for genre, keywords in self.genre_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in description_lower:
                    score += 1
                    # Bonus for exact matches at word boundaries
                    if f" {keyword} " in f" {description_lower} ":
                        score += 2

            genre_scores[genre] = score

        # Get genre with highest score
        best_genre = max(genre_scores.items(), key=lambda x: x[1])

        # If no strong match, use context-based fallback
        if best_genre[1] == 0:
            return self._context_based_fallback(description_lower)

        return best_genre[0]

    def _context_based_fallback(self, description: str) -> str:
        """Fallback genre classification based on context"""
        dancing_words = ["dancing", "dance", "party", "music", "celebrat"]
        happy_words = ["happy", "joy", "smile", "laugh", "fun"]
        sad_words = ["sad", "cry", "tear", "depressed", "lonely"]

        if any(word in description for word in dancing_words + happy_words):
            return "comedy"  # or "musical" if you add it
        elif any(word in description for word in sad_words):
            return "drama"
        else:
            return random.choice(list(self.templates.keys()))

    def get_style_prompt(self, genre: str) -> str:
        """Returns the style description for the given genre"""
        return self.templates.get(genre, {}).get("style", "cinematic, professional photography")