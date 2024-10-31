# src/utils/test_api_keys.py
import os
from dotenv import load_dotenv

def test_api_keys():
    # Get the project root directory (opuniverse)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
    
    # Load .env from project root
    load_dotenv(os.path.join(project_root, '.env'))
    
    # Check all API keys
    api_keys = {
        'OpenAI': os.getenv('OPENAI_API_KEY'),
        'JungleScout (inupo_goods)': os.getenv('JUNGLE_SCOUT_API_KEY'),
        'Anthropic (opuniverse)': os.getenv('ANTHROPIC_API_KEY'),
        'Perplexity': os.getenv('PERPLEXITY_API_KEY'),
        'Google Gemini': os.getenv('GOOGLE_API_KEY')
    }
    
    # Test each key
    for service, key in api_keys.items():
        if key:
            print(f"✅ {service} API key loaded successfully")
        else:
            print(f"❌ {service} API key not found")

if __name__ == "__main__":
    test_api_keys()