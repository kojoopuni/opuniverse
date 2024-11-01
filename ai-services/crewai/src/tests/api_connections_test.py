# src/tests/api_connections_test.py

import unittest
import logging
import os
import time
from dotenv import load_dotenv
from pathlib import Path
from tools.amazon.junglescout_api import JungleScoutAPI
from tools.ai.gpt4_api import GPT4API
from tools.ai.claude_api import ClaudeAPI
from tools.ai.gemini_api import GeminiAPI
from tools.search.perplexity import PerplexitySearchTool
from tools.search.web_search import WebSearchTool

logger = logging.getLogger(__name__)

class TestAPIConnections(unittest.TestCase):
    """Test suite for verifying all API connections"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment and load API keys"""
        current_dir = Path(__file__).resolve().parent
        root_dir = current_dir.parent.parent.parent.parent
        env_path = root_dir / '.env'
        
        print(f"Looking for .env file at: {env_path}")
        print(f"File exists: {env_path.exists()}")
        
        load_dotenv(env_path)
        
        # Debug: Print environment variables (sanitized)
        for key in ['JUNGLE_SCOUT_API_KEY', 'OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 
                   'GOOGLE_API_KEY', 'PERPLEXITY_API_KEY', 'SERP_API_KEY']:
            value = os.getenv(key)
            print(f"{key} {'is set' if value else 'is NOT set'}")

    def setUp(self):
        """Initialize API clients for testing"""
        self.test_keyword = "hammock"
        
        # Initialize JungleScout API with proper credentials
        jungle_scout = JungleScoutAPI(
            api_key=os.getenv('JUNGLE_SCOUT_API_KEY'),
            api_name="inupo_goods"
        )
        
        self.apis = {
            "jungle_scout": jungle_scout,
            "gpt4": GPT4API(),
            "claude": ClaudeAPI(),
            "gemini": GeminiAPI(),
            "perplexity": PerplexitySearchTool(),
            "web_search": WebSearchTool()
        }
        self.logger = logging.getLogger(__name__)

    def test_junglescout_connection(self):
        """Test JungleScout API connection using Share of Voice endpoint"""
        try:
            print("\nTesting JungleScout Share of Voice API:")
            response = self.apis["jungle_scout"].get_share_of_voice(self.test_keyword)
            
            # Verify response structure
            self.assertIn("data", response)
            self.assertIn("attributes", response["data"])
            attributes = response["data"]["attributes"]
            
            # Print key metrics
            print(f"Search Volume: {attributes['estimated_30_day_search_volume']:,}")
            print(f"Product Count: {attributes['product_count']:,}")
            
            # Display top brands
            if attributes['brands']:
                print("\nTop Brands by Share of Voice:")
                for brand in sorted(
                    attributes['brands'],
                    key=lambda x: x['combined_weighted_sov'],
                    reverse=True
                )[:3]:
                    print(f"- {brand['brand']}: {brand['combined_weighted_sov']:.2%}")
            
            self.logger.info("JungleScout API Test - Success")
            
        except Exception as e:
            self.fail(f"JungleScout API test failed: {str(e)}")

    def test_api_throttling(self):
        """Test API throttling implementation"""
        try:
            requests_made = 0
            start_time = time.time()
            min_delay = 1.0  # Minimum 1 second between requests
            
            for i in range(3):  # Reduced to 3 requests to stay within limits
                self.logger.info(f"\nThrottling test request {i+1}")
                
                if i > 0:
                    elapsed = time.time() - start_time
                    required_time = i * min_delay
                    if elapsed < required_time:
                        sleep_duration = required_time - elapsed
                        self.logger.info(f"Sleeping for {sleep_duration:.2f}s")
                        time.sleep(sleep_duration)
                
                response = self.apis["jungle_scout"].get_share_of_voice(self.test_keyword)
                
                # Verify response
                self.assertIn("data", response)
                self.assertIn("attributes", response["data"])
                
                requests_made += 1
                current_elapsed = time.time() - start_time
                current_rate = requests_made / current_elapsed
                
                self.logger.info(f"Request {i+1}:")
                self.logger.info(f"- Total elapsed: {current_elapsed:.2f}s")
                self.logger.info(f"- Current rate: {current_rate:.2f} requests/second")
                
        except Exception as e:
            self.logger.error(f"API throttling test failed: {str(e)}")
            self.fail(f"API throttling test failed: {str(e)}")

    def test_gpt4_connection(self):
        """Test GPT-4 API connection"""
        try:
            response = self.apis["gpt4"].analyze("Analyze market potential for hammocks")
            self.assertIn("status", response)
            self.assertEqual(response["status"], "success")
            self.logger.info("GPT-4 API Test - Success")
        except Exception as e:
            self.fail(f"GPT-4 API test failed: {str(e)}")

    def test_claude_connection(self):
        """Test Claude API connection"""
        try:
            response = self.apis["claude"].analyze("Evaluate competition in hammock market")
            self.assertIn("status", response)
            self.assertEqual(response["status"], "success")
            self.logger.info("Claude API Test - Success")
        except Exception as e:
            self.fail(f"Claude API test failed: {str(e)}")

    def test_gemini_connection(self):
        """Test Gemini API connection"""
        try:
            response = self.apis["gemini"].analyze("Analyze market trends for hammocks")
            self.assertIn("status", response)
            self.assertEqual(response["status"], "success")
            self.logger.info("Gemini API Test - Success")
        except Exception as e:
            self.fail(f"Gemini API test failed: {str(e)}")

    def test_perplexity_connection(self):
        """Test Perplexity API connection"""
        try:
            response = self.apis["perplexity"].search(
                "Analyze market trends for hammocks and outdoor furniture"
            )
            self.assertIn("status", response)
            self.assertEqual(response["status"], "success")
            self.logger.info("Perplexity API Test - Success")
        except Exception as e:
            self.fail(f"Perplexity API test failed: {str(e)}")

    def test_web_search_connection(self):
        """Test Web Search (SerpAPI) connection"""
        try:
            response = self.apis["web_search"].search(
                "best hammock brands amazon dropshipping"
            )
            self.assertIn("status", response)
            self.assertEqual(response["status"], "success")
            self.logger.info("Web Search API Test - Success")
        except Exception as e:
            self.fail(f"Web Search API test failed: {str(e)}")

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(process)d - %(filename)s-%(funcName)s:%(lineno)d - %(levelname)s: %(message)s'
    )
    unittest.main(verbosity=2)