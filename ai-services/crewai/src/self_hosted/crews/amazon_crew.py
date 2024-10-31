# src/self_hosted/crews/amazon_crew.py
from crewai import Agent, Task, Crew
from tools.amazon.research_tools import MarketResearchTool

class AmazonResearchCrew:
    def __init__(self):
        self.market_tool = MarketResearchTool()
        
    def create_crew(self) -> Crew:
        # Market Research Analyst
        market_analyst = Agent(
            role="Market Research Analyst",
            goal="Identify profitable Amazon product niches",
            backstory="""Expert e-commerce analyst with deep understanding 
            of Amazon marketplace dynamics and product research methodologies.""",
            verbose=True,
            allow_delegation=True,
            tools=[self.market_tool]
        )
        
        # Product Sourcing Specialist
        sourcing_specialist = Agent(
            role="Product Sourcing Specialist",
            goal="Find reliable suppliers meeting Amazon's criteria",
            backstory="""Experienced sourcing expert with extensive knowledge 
            of supplier networks and Amazon compliance requirements.""",
            verbose=True,
            allow_delegation=True,
            tools=[self.market_tool]
        )

        # Create tasks with expected_output parameter
        market_research = Task(
            description="""Analyze Amazon marketplace to identify top 5 
            low-competition, high-demand product niches.""",
            agent=market_analyst,
            expected_output="""A detailed list of 5 product niches with their 
            demand metrics, competition analysis, and profit potential."""
        )

        supplier_research = Task(
            description="""For each identified niche, find and evaluate 
            potential suppliers based on Amazon's criteria.""",
            agent=sourcing_specialist,
            expected_output="""A comprehensive supplier analysis for each 
            identified niche, including shipping times, costs, and compliance."""
        )

        # Create crew
        crew = Crew(
            agents=[market_analyst, sourcing_specialist],
            tasks=[market_research, supplier_research],
            verbose=True
        )
        
        return crew