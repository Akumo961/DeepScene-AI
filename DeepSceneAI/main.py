# test_setup.py
def test_basic_functionality():
    print("🧪 Testing DeepScene Setup...")

    # Test 1: Basic imports
    try:
        from src.data_loader import SceneDataLoader
        from src.preprocess import TextPreprocessor
        print("✅ Core modules imported successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return

    # Test 2: Basic functionality
    loader = SceneDataLoader()
    processor = TextPreprocessor()

    scene = "Two detectives in a dark warehouse"
    genre = loader.classify_scene_genre(scene)
    characters = processor.extract_characters(scene)

    print(f"✅ Scene: {scene}")
    print(f"✅ Genre: {genre}")
    print(f"✅ Characters: {characters}")
    print("🎉 Basic setup working perfectly!")


if __name__ == "__main__":
    test_basic_functionality()