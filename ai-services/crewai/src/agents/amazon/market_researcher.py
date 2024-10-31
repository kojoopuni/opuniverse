# src/agents/amazon/market_researcher.py
from crewai import Agent
from typing import Dict, Any
from tools.amazon.junglescout_api import JungleScoutAPI

class MarketResearchAgent(Agent):
    """
    Market Research Specialist focusing on Amazon product opportunities.
    Uses JungleScout Share of Voice data for deep market analysis.
    """
    
    def __init__(self, name: str = "Dr. Sarah Chen", **kwargs):
        super().__init__(
            name=name,
            role="Market Intelligence Specialist",
            goal="""Identify profitable market opportunities with >30% margins by analyzing 
            market share, competition levels, and search volumes""",
            backstory="""Former data scientist with Ph.D. in Market Analytics and 8 years 
            of experience in e-commerce research. Developed proprietary frameworks for 
            evaluating market opportunities that have led to over 200 successful product 
            launches. Expert in analyzing Share of Voice data, competitor metrics, and 
            market trends to identify underserved niches with high profit potential.""",
            tools=[JungleScoutAPI()],
            verbose=True,
            allow_delegation=True
        )

    def analyze_market_opportunity(self, keyword: str) -> Dict[str, Any]:
        """Analyze market opportunity using Share of Voice data"""
        sov_data = self.tools["jungle_scout"].get_share_of_voice(keyword)
        
        market_size = sov_data["data"]["attributes"]["estimated_30_day_search_volume"]
        competition = self._analyze_competition(sov_data["data"]["attributes"]["brands"])
        
        return {
            "keyword": keyword,
            "market_size": market_size,
            "competition_level": competition,
            "opportunity_score": self._calculate_opportunity_score(market_size, competition)
        }

    def _analyze_competition(self, brands_data: List[Dict]) -> str:
        """Analyze competition level based on brand metrics"""
        top_brands = sorted(
            brands_data,
            key=lambda x: x["combined_weighted_sov"],
            reverse=True
        )[:5]
        
        total_sov = sum(b["combined_weighted_sov"] for b in top_brands)
        
        if total_sov > 0.8:
            return "high"
        elif total_sov > 0.6:
            return "medium"
        return "low"