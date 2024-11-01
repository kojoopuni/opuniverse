# src/tests/junglescout_tool_test.py

import unittest
import logging
import os
from dotenv import load_dotenv
from pathlib import Path
from tools.amazon.junglescout_tool import analyze_market

logger = logging.getLogger(__name__)

class TestJungleScoutTool(unittest.TestCase):
    """Test suite for CrewAI JungleScout tool"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment and load API keys"""
        current_dir = Path(__file__).resolve().parent
        root_dir = current_dir.parent.parent.parent.parent
        env_path = root_dir / '.env'
        
        print(f"Looking for .env file at: {env_path}")
        print(f"File exists: {env_path.exists()}")
        
        load_dotenv(env_path)
        
        if os.getenv('JUNGLE_SCOUT_API_KEY'):
            print("JUNGLE_SCOUT_API_KEY is set")

    def test_market_analysis(self):
        """Test market analysis tool"""
        try:
            print("\nTesting JungleScout Market Analysis Tool:")
            keyword = "hammock"
            
            # Call the function directly, not the decorated object
            result = analyze_market._run(keyword)
            
            # Print the formatted result
            print(result)
            
            # Verify result contains key information
            self.assertIn("Market Analysis", result)
            self.assertIn("Monthly Search Volume", result)
            self.assertIn("Top Brands", result)
            
            logger.info("JungleScout Tool Test - Success")
            
        except Exception as e:
            self.fail(f"Market analysis test failed: {str(e)}")

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(process)d - %(filename)s-%(funcName)s:%(lineno)d - %(levelname)s: %(message)s'
    )
    unittest.main(verbosity=2)