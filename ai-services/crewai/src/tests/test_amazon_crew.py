# src/tests/test_amazon_crew_workflow.py
# COMPLETE SCRIPT

import unittest
import logging
import os
from dotenv import load_dotenv
from pathlib import Path
from crewai import Agent, Task, Crew, Process
from tools.amazon.junglescout_tool import analyze_market
# Import other agent tools as needed

logger = logging.getLogger(__name__)

class TestAmazonCrewWorkflow(unittest.TestCase):
    """Test suite for the complete Amazon Product Research Crew workflow"""

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
        """Initialize all agents with their tools"""
        # Market Research Agent
        self.market_researcher = Agent(
            role='Market Research Analyst',
            goal='Analyze Amazon market opportunities and competition',
            backstory="""Expert e-commerce analyst specializing in Amazon marketplace research.""",
            tools=[analyze_market],
            verbose=True
        )

        # Product Research Agent
        self.product_researcher = Agent(
            role='Product Research Specialist',
            goal='Identify product specifications and requirements',
            backstory="""Product development expert focusing on manufacturing requirements.""",
            tools=[],  # Add product research tools
            verbose=True
        )

        # Add other agents here...
        # self.supplier_researcher = Agent(...)
        # self.logistics_analyst = Agent(...)
        # etc.

        # Create the full crew
        self.crew = Crew(
            agents=[
                self.market_researcher,
                self.product_researcher,
                # Add other agents...
            ],
            tasks=[],  # Tasks will be added in tests
            process=Process.sequential,
            verbose=True
        )

    def test_complete_product_research_workflow(self):
        """Test the entire product research workflow"""
        try:
            print("\nTesting Complete Amazon Product Research Workflow:")
            
            # Create sequential tasks for the entire workflow
            tasks = [
                Task(
                    description="Analyze the market for hammocks on Amazon",
                    expected_output="Market analysis report",
                    agent=self.market_researcher
                ),
                Task(
                    description="""Based on the market analysis, research product 
                    specifications for hammocks that will be competitive""",
                    expected_output="Product specifications report",
                    agent=self.product_researcher
                ),
                # Add tasks for other agents...
            ]

            # Update crew with all tasks
            self.crew.tasks = tasks

            # Execute the full workflow
            result = self.crew.kickoff()
            result_str = str(result)
            
            print("\nCrew Workflow Results:")
            print(result_str)
            
            # Verify key components from all agents
            self.assertIn("market", result_str.lower())
            self.assertIn("product", result_str.lower())
            self.assertIn("specifications", result_str.lower())
            # Add more assertions for other agent outputs
            
            logger.info("Full Crew Workflow Test - Success")
            
        except Exception as e:
            self.fail(f"Crew workflow test failed: {str(e)}")

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(process)d - %(filename)s-%(funcName)s:%(lineno)d - %(levelname)s: %(message)s'
    )
    unittest.main(verbosity=2)