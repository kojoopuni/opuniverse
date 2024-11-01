# src/tests/amazon/test_memory_store.py

import unittest
import shutil
import os
from pathlib import Path
from datetime import datetime
from crews.memory_store import BaseMemoryStore
from crews.amazon.amazon_memory_store import AmazonMemoryStore

class TestMemoryStore(unittest.TestCase):
    """Test suite for memory store implementations"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = "test_memory"
        self.memory = AmazonMemoryStore(storage_dir=self.test_dir)
        
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

    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_store_market_insight(self):
        """Test storing market research data"""
        keyword = "hammock"
        self.memory.store_market_insight(keyword, self.sample_data)
        
        # Retrieve stored data
        stored_data = self.memory.get_market_insight(keyword)
        
        # Verify data structure
        self.assertIsNotNone(stored_data)
        self.assertIn("search_volume", stored_data)
        self.assertEqual(stored_data["search_volume"], 275615)
        self.assertIn("top_brands", stored_data)
        self.assertEqual(len(stored_data["top_brands"]), 2)
        self.assertEqual(stored_data["top_brands"][0]["brand"], "Amazon Basics")

    def test_competition_analysis(self):
        """Test competition analysis storage"""
        keyword = "hammock"
        self.memory.store_competition_analysis(keyword, self.sample_data)
        
        # Retrieve competition analysis
        analysis = self.memory.get_competition_analysis(keyword)
        
        # Verify analysis
        self.assertIsNotNone(analysis)
        self.assertIn("market_leaders", analysis)
        self.assertIn("market_gaps", analysis)
        
        # Verify market leader data
        leaders = analysis["market_leaders"]
        self.assertEqual(leaders[0]["brand"], "Amazon Basics")
        self.assertEqual(leaders[0]["market_share"], 0.29)

    def test_historical_data(self):
        """Test historical data storage"""
        keyword = "hammock"
        
        # Store multiple data points
        for _ in range(3):
            self.memory.store_market_insight(keyword, self.sample_data)
        
        # Retrieve historical data
        stored_data = self.memory.get_market_insight(keyword)
        
        # Verify historical data structure
        self.assertIsInstance(stored_data, list)
        self.assertEqual(len(stored_data), 3)
        for entry in stored_data:
            self.assertIn("timestamp", entry)
            self.assertIn("search_volume", entry)

    def test_market_gaps(self):
        """Test market gap identification"""
        keyword = "hammock"
        self.memory.store_competition_analysis(keyword, self.sample_data)
        
        analysis = self.memory.get_competition_analysis(keyword)
        gaps = analysis["market_gaps"]
        
        # Verify gap analysis
        self.assertIsInstance(gaps, list)
        for gap in gaps:
            self.assertIn("price_segment", gap)
            self.assertIn("current_share", gap)
            self.assertIn("competitors", gap)

if __name__ == '__main__':
    unittest.main(verbosity=2)