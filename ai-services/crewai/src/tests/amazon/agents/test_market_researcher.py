# src/tests/amazon/agents/test_market_researcher.py

import unittest
from unittest.mock import Mock, patch
import os
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from agents.amazon.market_researcher import MarketResearchAgent
from crews.amazon.amazon_memory_store import AmazonMemoryStore
from tools.amazon.junglescout_api import JungleScoutAPI

class TestMarketResearchAgent(unittest.TestCase):
    """Test suite for Market Research Agent"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment and load API keys"""
        current_dir = Path(__file__).resolve().parent
        root_dir = current_dir.parent.parent.parent.parent.parent
        env_path = root_dir / '.env'
        
        print(f"Looking for .env file at: {env_path}")
        print(f"File exists: {env_path.exists()}")
        
        load_dotenv(env_path)
        
        if not os.getenv('JUNGLE_SCOUT_API_KEY'):
            raise ValueError("JUNGLE_SCOUT_API_KEY not found in environment variables")

    def setUp(self):
        """Set up test environment"""
        self.memory = AmazonMemoryStore(storage_dir="test_memory")
        
        # Sample Share of Voice data based on actual API response
        self.sample_data = {
            "data": {
                "id": "us/hammock",
                "type": "share_of_voice",
                "attributes": {
                    "estimated_30_day_search_volume": 275615,
                    "product_count": 180,
                    "brands": [
                        {
                            "brand": "Amazon Basics",
                            "combined_weighted_sov": 0.29,
                            "combined_average_price": 65.42,
                            "combined_average_position": 22.33
                        },
                        {
                            "brand": "SXSEAGLE",
                            "combined_weighted_sov": 0.18,
                            "combined_average_price": 58.66,
                            "combined_average_position": 27.33
                        }
                    ]
                }
            }
        }
        
        # Initialize agent with proper API key and tool configuration
        self.agent = MarketResearchAgent(
            name="Dr. Sarah Chen",
            api_key=os.getenv('JUNGLE_SCOUT_API_KEY'),
            memory=self.memory
        )

    def test_analyze_market_opportunity(self):
        """Test market opportunity analysis"""
        with patch('tools.amazon.junglescout_api.JungleScoutAPI.get_share_of_voice') as mock_sov:
            mock_sov.return_value = self.sample_data
            
            result = self.agent.analyze_market_opportunity("hammock")
            
            self.assertIn("market_size", result)
            self.assertEqual(result["market_size"], 275615)
            self.assertIn("competition_level", result)
            self.assertIn("opportunity_score", result)
            self.assertIn("market_leaders", result)
            
            # Verify market leaders
            leaders = result["market_leaders"]
            self.assertEqual(leaders[0]["brand"], "Amazon Basics")
            self.assertEqual(leaders[0]["market_share"], 0.29)

    def test_market_validation(self):
        """Test market validation criteria"""
        with patch('tools.amazon.junglescout_api.JungleScoutAPI.get_share_of_voice') as mock_sov:
            mock_sov.return_value = self.sample_data
            
            result = self.agent.validate_market("hammock")
            
            self.assertIn("is_valid", result)
            self.assertIn("metrics", result)
            self.assertIn("reasons", result)
            
            metrics = result["metrics"]
            self.assertGreater(metrics["search_volume"], 10000)
            self.assertIn("price_range", metrics)
            self.assertIn("market_leaders", metrics)

    def test_competition_analysis(self):
        """Test competition analysis"""
        competition = self.agent._analyze_competition(self.sample_data["data"]["attributes"]["brands"])
        self.assertIn(competition, ["low", "medium", "high"])

    def test_price_analysis(self):
        """Test price range analysis"""
        price_range = self.agent._analyze_price_range(self.sample_data["data"]["attributes"]["brands"])
        
        self.assertIn("min", price_range)
        self.assertIn("max", price_range)
        self.assertIn("average", price_range)
        self.assertGreater(price_range["max"], price_range["min"])

    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists("test_memory"):
            import shutil
            shutil.rmtree("test_memory")

if __name__ == '__main__':
    unittest.main(verbosity=2)