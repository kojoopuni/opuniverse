# src/test_api_key.py
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_openai_key():
    try:
        # Load environment variables
        load_dotenv()
        
        # Get the API key
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            logger.error("OPENAI_API_KEY not found in environment variables")
            return False
            
        # Check if it starts with 'sk-'
        if not api_key.startswith('sk-'):
            logger.error("OPENAI_API_KEY format appears incorrect")
            return False
            
        logger.info("OPENAI_API_KEY found and format appears correct")
        return True
        
    except Exception as e:
        logger.error(f"Error testing API key: {str(e)}")
        return False

if __name__ == "__main__":
    test_openai_key()