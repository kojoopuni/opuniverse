# src/self_hosted/crews/test_amazon_crew.py
from self_hosted.crews.amazon_crew import AmazonResearchCrew
import logging

logging.basicConfig(level=logging.INFO)

def test_amazon_crew():
    try:
        # Initialize the crew
        amazon_crew = AmazonResearchCrew()
        
        # Create and run the crew
        crew = amazon_crew.create_crew()
        result = crew.kickoff()
        
        print("Crew Analysis Results:")
        print(result)
        
    except Exception as e:
        logging.error(f"Error running Amazon crew: {str(e)}")

if __name__ == "__main__":
    test_amazon_crew()