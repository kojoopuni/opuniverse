from crewai import Agent, Task, Crew
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from tools.amazon.amz_market_research_tool import AmazonMarketResearchTool
from tools.amazon.amz_supplier_research_tool import AmazonSupplierResearchTool

class AmazonResearchCrew:
    def __init__(self):
        self.market_tool = AmazonMarketResearchTool()
        self.supplier_tool = AmazonSupplierResearchTool()
        
    def create_crew(self) -> Crew:
        # Market Research Analyst with GPT-4
        market_analyst = Agent(
            role="Senior Market Research Analyst",
            goal="""Identify profitable Amazon product niches by:
            - Finding products with >500 monthly sales and <100 competitor reviews
            - Analyzing seasonal trends and long-term market viability
            - Identifying emerging market gaps and untapped opportunities
            - Ensuring 30%+ profit margins after all costs
            - Validating compliance with Amazon's policies""",
            backstory="""20-year veteran in Amazon marketplace analysis with expertise in:
            - Identifying emerging market trends before they become saturated
            - Understanding seasonal buying patterns
            - Analyzing competitor weaknesses and market gaps
            - Evaluating long-term product viability
            - Spotting potential regulatory issues before they become problems
            Previous success includes identifying multiple six-figure niches.""",
            verbose=True,
            allow_delegation=True,
            tools=[self.market_tool],
            llm=ChatOpenAI(
                model_name="gpt-4-turbo-preview",
                temperature=0.7
            )
        )
        
        # Sourcing Specialist with Claude
        sourcing_specialist = Agent(
            role="Product Sourcing Specialist",
            goal="""Find and validate reliable US-based suppliers by:
            - Identifying suppliers with consistent quality and delivery
            - Ensuring shipping times under 7 days
            - Validating supplier reliability and track record
            - Confirming competitive pricing and bulk discounts
            - Verifying compliance with Amazon's requirements""",
            backstory="""15 years in supply chain management specializing in:
            - Building reliable US supplier networks
            - Negotiating favorable terms and pricing
            - Quality control and compliance verification
            - Logistics optimization
            - Supplier relationship management
            Has established relationships with over 500 reliable US suppliers.""",
            verbose=True,
            allow_delegation=True,
            tools=[self.supplier_tool],
            llm=ChatAnthropic(
                model="claude-3.5-sonnet",
                temperature=0.6
            )
        )

        # Tasks with detailed but flexible outputs
        market_research = Task(
            description="""Analyze Amazon marketplace to identify top 5 
            low-competition, high-demand product niches.""",
            agent=market_analyst,
            expected_output="""Comprehensive analysis of profitable niches 
            including demand metrics, competition levels, and market opportunities."""
        )

        supplier_research = Task(
            description="""For each identified niche, find and evaluate 
            potential suppliers based on Amazon's criteria.""",
            agent=sourcing_specialist,
            expected_output="""Detailed supplier analysis including reliability metrics, 
            shipping capabilities, and compliance status."""
        )

        return Crew(
            agents=[market_analyst, sourcing_specialist],
            tasks=[market_research, supplier_research],
            verbose=True
        )