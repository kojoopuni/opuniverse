# src/tests/test_market_research_agent.py
# COMPLETE SCRIPT

import unittest
import logging
import os
from dotenv import load_dotenv
from pathlib import Path
from crewai import Agent, Task, Crew, Process
from tools.amazon.junglescout_tool import analyze_market

logger = logging.getLogger(__name__)

class TestMarketResearchAgent(unittest.TestCase):
    """Test suite for Market Research Agent using JungleScout tool"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment and load API keys"""
        current_dir = Path(__file__).resolve().parent
        root_dir = current_dir.parent.parent.parent.parent
        env_path = root_dir / '.env'
        
        print(f"Looking for .env file at: {env_path}")
        print(f"File exists: {env_path.exists()}")
        
        load_dotenv(env_path)

    def setUp(self):
        """Initialize the agent with JungleScout tool"""
        self.market_researcher = Agent(
            role='Market Research Analyst',
            goal='Analyze Amazon market opportunities and competition',
            backstory="""Expert e-commerce analyst specializing in Amazon marketplace research.""",
            tools=[analyze_market],
            verbose=True
        )

    def test_market_analysis_task(self):
        """Test market analysis capabilities"""
        try:
            print("\nTesting Market Research Agent with JungleScout Tool:")
            
            task = Task(
                description="""Analyze the market for hammocks on Amazon.
                Provide detailed insights on:
                1. Market size and search volume
                2. Top competing brands and their market share
                3. Competition level assessment
                4. Market entry recommendations""",
                expected_output="""A comprehensive market analysis report including:
                - Market size metrics
                - Competitive landscape analysis
                - Brand market share breakdown
                - Strategic recommendations""",
                agent=self.market_researcher
            )

            crew = Crew(
                agents=[self.market_researcher],
                tasks=[task],
                process=Process.sequential,
                verbose=True
            )

            result = crew.kickoff()
            result_str = str(result)
            
            print("\nAgent's Market Analysis:")
            print(result_str)
            
            # Verify key components in the analysis
            self.assertIn("market", result_str.lower())
            self.assertIn("share", result_str.lower())
            self.assertIn("recommendation", result_str.lower())
            
            logger.info("Market Research Agent Test - Success")
            
        except Exception as e:
            self.fail(f"Market research agent test failed: {str(e)}")

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(process)d - %(filename)s-%(funcName)s:%(lineno)d - %(levelname)s: %(message)s'
    )
    unittest.main(verbosity=2)