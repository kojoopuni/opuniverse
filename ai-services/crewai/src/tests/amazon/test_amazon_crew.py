# src/tests/test_amazon_crew.py

import unittest
import logging
from datetime import datetime, timedelta
from time import sleep
from typing import Dict, Any
from crews.amazon.amazon_crew import AmazonResearchCrew
from tools.amazon.junglescout_api import JungleScoutAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThrottlingManager:
    """Manage API request throttling"""
    def __init__(self, max_requests: int = 100, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window  # in seconds
        self.requests = []

    def check_throttle(self):
        """Check if we need to throttle requests"""
        current_time = datetime.now()
        # Remove requests older than time window
        self.requests = [t for t in self.requests 
                        if (current_time - t).total_seconds() < self.time_window]
        
        if len(self.requests) >= self.max_requests:
            sleep_time = (self.requests[0] + timedelta(seconds=self.time_window) - current_time).total_seconds()
            if sleep_time > 0:
                logger.info(f"Throttling: Sleeping for {sleep_time} seconds")
                sleep(sleep_time)
        
        self.requests.append(current_time)

class TestAmazonCrew(unittest.TestCase):
    """Test suite for Amazon Research Crew"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.crew = AmazonResearchCrew()
        cls.throttle = ThrottlingManager()
        cls.test_keywords = ["hammock", "camping gear", "outdoor furniture"]

    def test_01_agent_initialization(self):
        """Test that all agents are properly initialized"""
        logger.info("Testing agent initialization...")
        
        expected_agents = {
            "market_researcher": "Dr. Sarah Chen",
            "competition_analyst": "Michael Porter",
            "product_validator": "Marcus Thompson",
            "pricing_strategist": "Diana Price",
            "supplier_researcher": "Li Wei",
            "listing_optimizer": "Alexandra Rivera",
            "trend_analyst": "David Trends"
        }

        for agent_id, expected_name in expected_agents.items():
            self.assertIn(agent_id, self.crew.agents)
            self.assertEqual(self.crew.agents[agent_id].name, expected_name)

    def test_02_api_connections(self):
        """Test all API connections"""
        logger.info("Testing API connections...")
        
        # Test JungleScout API
        self.throttle.check_throttle()
        jungle_scout = JungleScoutAPI()
        response = jungle_scout.get_share_of_voice("test")
        self.assertEqual(response.get("status_code"), 200)

        # Test other APIs (Perplexity, etc.)
        # Add tests for other APIs used by agents

    def test_03_market_research_flow(self):
        """Test market research workflow"""
        logger.info("Testing market research workflow...")
        
        for keyword in self.test_keywords:
            self.throttle.check_throttle()
            market_data = self.crew.agents["market_researcher"].analyze_market(keyword)
            
            # Validate market data structure
            self.assertIn("estimated_30_day_search_volume", market_data)
            self.assertIn("competition_level", market_data)
            self.assertIn("opportunity_score", market_data)

    def test_04_product_validation_flow(self):
        """Test product validation workflow"""
        logger.info("Testing product validation flow...")
        
        # Get test market data
        self.throttle.check_throttle()
        market_data = self.crew.agents["market_researcher"].analyze_market(self.test_keywords[0])
        
        # Test validation
        validation_result = self.crew.agents["product_validator"].validate_opportunity(market_data)
        
        # Check validation result structure
        self.assertIn("validation_score", validation_result)
        self.assertIn("profit_potential", validation_result)
        self.assertIn("risk_factors", validation_result)

    def test_05_full_research_workflow(self):
        """Test complete research workflow"""
        logger.info("Testing complete research workflow...")
        
        self.throttle.check_throttle()
        result = self.crew.research_product_opportunity(self.test_keywords[0])
        
        # Validate result structure
        self.assertIn("status", result)
        if result["status"] == "success":
            self.assertIn("market_data", result)
            self.assertIn("competition_data", result)
            self.assertIn("validation_data", result)
            self.assertIn("supplier_data", result)
        else:
            self.assertIn("reason", result)

    def test_06_memory_persistence(self):
        """Test memory storage and retrieval"""
        logger.info("Testing memory persistence...")
        
        test_data = {
            "keyword": self.test_keywords[0],
            "timestamp": datetime.now().isoformat(),
            "market_data": {"test": "data"}
        }
        
        # Store data
        self.crew.memory_store.store_market_insight(
            self.test_keywords[0],
            test_data
        )
        
        # Retrieve data
        stored_data = self.crew.memory_store.get_market_insight(
            self.test_keywords[0]
        )
        
        self.assertEqual(stored_data["market_data"], test_data["market_data"])

    def test_07_validation_criteria(self):
        """Test validation criteria implementation"""
        logger.info("Testing validation criteria...")
        
        test_data = {
            "estimated_30_day_search_volume": 50000,
            "competition_level": "medium",
            "profit_margin": 0.35
        }
        
        validation_result = self.crew.validation.validate_market(test_data)
        self.assertTrue(isinstance(validation_result, tuple))
        self.assertEqual(len(validation_result), 2)  # (passed, results)

def run_tests():
    """Run all tests with proper logging"""
    try:
        unittest.main(verbosity=2)
    except Exception as e:
        logger.error(f"Test suite failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_tests()