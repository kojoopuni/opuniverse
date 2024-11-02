# src/tests/base_agent_test.py

import unittest
import logging
import os
from dotenv import load_dotenv
from pathlib import Path
from crewai import Agent, Task, Crew, Process

logger = logging.getLogger(__name__)

class BaseAgentTest(unittest.TestCase):
    """Base test class for all agent tests"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment and load API keys"""
        current_dir = Path(__file__).resolve().parent
        root_dir = current_dir.parent.parent.parent.parent
        env_path = root_dir / '.env'
        
        print(f"Looking for .env file at: {env_path}")
        print(f"File exists: {env_path.exists()}")
        
        load_dotenv(env_path)

    def execute_agent_task(self, agent, task_description, expected_outputs):
        """Execute a task with an agent and verify outputs"""
        try:
            task = Task(
                description=task_description,
                expected_output="Comprehensive analysis and recommendations",
                agent=agent
            )

            crew = Crew(
                agents=[agent],
                tasks=[task],
                process=Process.sequential,
                verbose=True
            )

            # Execute and get result
            result = crew.kickoff()
            result_text = str(result)
            
            print("\nAgent's Analysis:")
            print(result_text)
            
            # Verify expected outputs
            for expected in expected_outputs:
                self.assertIn(expected.lower(), result_text.lower())
            
            return result_text
            
        except Exception as e:
            self.fail(f"Agent task execution failed: {str(e)}")