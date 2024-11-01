# src/crews/amazon/amazon_crew.py

from typing import Dict, Any, List, Tuple
from datetime import datetime
import logging
from crewai import Agent, Task, Crew, Process

# Amazon specific tools
from tools.amazon.junglescout_api import JungleScoutAPI

# AI tools
from tools.ai.gpt4_api import GPT4API
from tools.ai.claude_api import ClaudeAPI
from tools.ai.gemini_api import GeminiAPI

# Search tools
from tools.search.web_search import WebSearchTool
from tools.search.perplexity import PerplexitySearchTool

logger = logging.getLogger(__name__)

class ValidationCriteria:
    """Validation criteria for Amazon product opportunities based on JungleScout data"""
    
    def __init__(self):
        # Market Criteria based on Share of Voice data
        self.market_criteria = {
            "min_search_volume": 10000,        # Based on sample showing 142,377 searches
            "max_competition": 0.7,            # Maximum market share for top 3 brands
            "min_profit_margin": 0.3,          # 30% minimum profit margin
            "max_price_volatility": 0.15       # Maximum price change percentage
        }

        # Product Criteria
        self.product_criteria = {
            "min_price": 20.00,               # Minimum viable price point
            "max_price": 200.00,              # Maximum price for easy entry
            "min_rating": 4.0,                # Minimum acceptable rating
            "min_reviews": 100,               # Minimum reviews for validation
            "max_weight": 5.0,                # Maximum weight for shipping
            "min_margin_dollars": 15.00       # Minimum profit in dollars
        }

        # Competition Criteria based on Share of Voice metrics
        self.competition_criteria = {
            "max_top_brand_share": 0.30,      # Max share for single brand (like sample showing 25%)
            "min_organic_opportunity": 0.20,   # Minimum organic opportunity
            "max_sponsored_share": 0.40,       # Maximum sponsored product share
            "min_market_gap": 0.10            # Minimum market gap opportunity
        }

class AmazonResearchCrew:
    """Specialized crew for Amazon product research and validation"""
    
    def __init__(self):
        self.validation = ValidationCriteria()
        self.agents = self._create_agents()
        self.memory_store = MemoryStore()

    def _create_agents(self) -> Dict[str, Agent]:
        """Initialize all specialized agents with rich personas and appropriate tools"""
        
        market_researcher = Agent(
            name="Dr. Sarah Chen",
            role="Market Intelligence Specialist",
            goal="""Identify profitable market opportunities with >30% margins by analyzing 
            market share, competition levels, and search volumes. Focus on products with 
            proven demand and sustainable competitive advantages.""",
            backstory="""Former data scientist with Ph.D. in Market Analytics and 8 years 
            of experience in e-commerce research. Developed proprietary frameworks for 
            evaluating market opportunities that have led to over 200 successful product 
            launches. Expert in analyzing Share of Voice data, competitor metrics, and 
            market trends to identify underserved niches with high profit potential.""",
            tools=[
                JungleScoutAPI(),
                PerplexitySearchTool(),
                GPT4API()
            ],
            verbose=True,
            allow_delegation=True
        )
        
        competition_analyst = Agent(
            name="Michael Porter",
            role="Competition Analysis Strategist",
            goal="""Analyze competitive landscape to identify market gaps and optimal 
            positioning strategies. Ensure selected opportunities have sustainable 
            competitive advantages.""",
            backstory="""Former management consultant with 12 years specializing in 
            competitive analysis. Expert in analyzing Share of Voice data, brand 
            positioning, and market dynamics. Developed frameworks for competitive 
            advantage analysis used by Fortune 500 companies.""",
            tools=[
                JungleScoutAPI(),
                ClaudeAPI(),
                PerplexitySearchTool()
            ],
            verbose=True,
            allow_delegation=True
        )
        
        product_validator = Agent(
            name="Marcus Thompson",
            role="Product Validation Strategist",
            goal="""Validate product opportunities through comprehensive data analysis 
            to ensure >30% profit margins and sustainable market position. Focus on 
            products with optimal shipping characteristics.""",
            backstory="""Former Amazon Category Manager with 10 years of experience in 
            product selection and validation. Developed a systematic approach that has 
            resulted in a 78% success rate for new product launches. Expert in analyzing 
            sales velocity, profit margins, and competition levels.""",
            tools=[
                JungleScoutAPI(),
                GPT4API(),
                WebSearchTool()
            ],
            verbose=True,
            allow_delegation=True
        )
        
        pricing_strategist = Agent(
            name="Diana Price",
            role="Strategic Pricing Specialist",
            goal="""Develop optimal pricing strategies that maximize profit margins while 
            maintaining market competitiveness. Ensure pricing aligns with market 
            positioning and customer expectations.""",
            backstory="""Former pricing optimization expert with 15 years of experience 
            in e-commerce. Developed pricing algorithms that increased profits by 40% 
            for major retailers. Expert in analyzing competitor pricing, market 
            positioning, and elasticity to find optimal price points.""",
            tools=[
                JungleScoutAPI(),
                GPT4API(),
                ClaudeAPI()
            ],
            verbose=True,
            allow_delegation=True
        )
        
        supplier_researcher = Agent(
            name="Li Wei",
            role="Global Sourcing Specialist",
            goal="""Identify and evaluate reliable suppliers who can deliver quality 
            products at competitive prices with consistent supply chain operations. 
            Ensure suppliers meet strict quality and shipping criteria.""",
            backstory="""Supply chain expert with 12 years of experience in international 
            trade and supplier relationships. Built an extensive network of reliable 
            suppliers across Asia. Developed quality control systems that reduced defect 
            rates by 95%.""",
            tools=[
                WebSearchTool(),
                PerplexitySearchTool(),
                GeminiAPI()
            ],
            verbose=True,
            allow_delegation=True
        )
        
        listing_optimizer = Agent(
            name="Alexandra Rivera",
            role="Listing Optimization Expert",
            goal="""Maximize product visibility and conversion rates through data-driven 
            listing optimization and strategic keyword implementation. Achieve top 
            search rankings and high conversion rates.""",
            backstory="""Former Amazon A9 Algorithm Specialist with deep expertise in 
            search ranking factors and buyer psychology. Optimized over 5,000 listings 
            achieving 156% average increase in conversion rates.""",
            tools=[
                JungleScoutAPI(),
                GPT4API(),
                ClaudeAPI()
            ],
            verbose=True,
            allow_delegation=True
        )
        
        trend_analyst = Agent(
            name="David Trends",
            role="Market Trend Analyst",
            goal="""Identify and analyze emerging market trends and seasonal patterns 
            to optimize product selection and timing. Predict market movements and 
            identify growth opportunities.""",
            backstory="""Data scientist specializing in market trend analysis with 
            10 years of experience. Developed predictive models that accurately 
            forecast market trends with 85% accuracy. Created trend prediction 
            models used by major e-commerce platforms.""",
            tools=[
                JungleScoutAPI(),
                PerplexitySearchTool(),
                GeminiAPI()
            ],
            verbose=True,
            allow_delegation=True
        )

        return {
            "market_researcher": market_researcher,
            "competition_analyst": competition_analyst,
            "product_validator": product_validator,
            "pricing_strategist": pricing_strategist,
            "supplier_researcher": supplier_researcher,
            "listing_optimizer": listing_optimizer,
            "trend_analyst": trend_analyst
        }