# src/preprocess.py
import re
import spacy
from typing import List


class TextPreprocessor:
    """
    Enhanced text preprocessing with better character and setting extraction
    """

    def __init__(self):
        # Try to load spaCy for better NLP, fallback to regex
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            self.nlp = None
            print("⚠️ spaCy model not found. Using fallback extraction methods.")

    def clean_text(self, text: str) -> str:
        return text.strip().replace("\n", " ")

    def extract_characters(self, description):
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

        # If no specific characters found, infer from context
        if not characters:
            if "dancing" in desc_lower:
                characters.append("Dancer")
            elif any(word in desc_lower for word in ["investigate", "crime", "mystery"]):
                characters.append("Detective")
            else:
                characters.append("Main Character")

        return characters

    def extract_setting(self, description: str) -> str:
        """Enhanced setting extraction"""
        if self.nlp:
            doc = self.nlp(description)
            # Look for locations and facilities
            locations = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC", "FAC", "ORG"]]
            if locations:
                return locations[0]

        # Fallback: improved regex patterns for settings
        setting_patterns = [
            r"(in|at|inside|on|through|outside|within)\s+(?:a|an|the)?\s*([^,.!?]+?(?:room|house|building|street|park|forest|beach|office|school|restaurant|bar|club|studio|stage|theater))",
            r"(in|at)\s+(?:a|an|the)?\s*([^,.!?]+)",
            r"on\s+(?:a|an|the)?\s*([^,.!?]+\s+(?:street|avenue|road|boulevard))",
        ]

        for pattern in setting_patterns:
            match = re.search(pattern, description.lower())
            if match:
                return match.group(2).strip()

        return "general location"

    def generate_image_prompt(self, description: str, style: str) -> str:
        """Generate enhanced image prompt"""
        # Clean up the style string
        style_clean = style.replace("style:", "").replace("Style:", "").strip()

        # Build a more descriptive prompt
        prompt_parts = [
            description,
            f"cinematic style, {style_clean}",
            "high quality, detailed, professional photography",
            "film still, dramatic composition"
        ]

        return ", ".join(prompt_parts)