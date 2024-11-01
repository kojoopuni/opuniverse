# src/agents/amazon/market_researcher.py

from typing import Dict, Any, List
from crewai import Agent
from langchain.tools import BaseTool
from tools.amazon.junglescout_api import JungleScoutAPI

class MarketResearchAgent(Agent):
    """Market Research Specialist focusing on Amazon product opportunities"""
    
    def __init__(self, name: str = "Dr. Sarah Chen", **kwargs):
        # Initialize JungleScout API with proper tool attributes
        jungle_scout = JungleScoutAPI(
            api_key=kwargs.get('api_key'),
            api_name="inupo_goods"
        )
        jungle_scout.name = "jungle_scout_api"
        jungle_scout.description = "Tool for analyzing Amazon market data using JungleScout's Share of Voice API"
        
        super().__init__(
            name=name,
            role="Market Intelligence Specialist",
            goal="""Identify profitable market opportunities with >30% margins by analyzing 
            market share, competition levels, and search volumes. Focus on products with 
            proven demand and sustainable competitive advantages.""",
            backstory="""Former data scientist with Ph.D. in Market Analytics and 8 years 
            of experience in e-commerce research. Developed proprietary frameworks for 
            evaluating market opportunities that have led to over 200 successful product 
            launches. Expert in analyzing Share of Voice data, competitor metrics, and 
            market trends to identify underserved niches with high profit potential. 
            Specializes in identifying market gaps and opportunities in competitive 
            landscapes through advanced data analysis and pattern recognition.""",
            tools=[jungle_scout],
            verbose=True,
            allow_delegation=True,
            **kwargs
        )

    def analyze_market_opportunity(self, keyword: str) -> Dict[str, Any]:
        """Analyze market opportunity using Share of Voice data"""
        response = self.tools[0].get_share_of_voice(keyword)
        data = response["data"]["attributes"]
        
        return {
            "keyword": keyword,
            "market_size": data["estimated_30_day_search_volume"],
            "competition_level": self._analyze_competition(data["brands"]),
            "opportunity_score": self._calculate_opportunity_score(
                data["estimated_30_day_search_volume"],
                self._analyze_competition(data["brands"])
            ),
            "market_leaders": self._identify_market_leaders(data["brands"])
        }

    def _analyze_competition(self, brands: List[Dict]) -> str:
        """Analyze competition level based on brand metrics"""
        top_brands = sorted(
            brands,
            key=lambda x: x["combined_weighted_sov"],
            reverse=True
        )[:3]
        
        total_sov = sum(b["combined_weighted_sov"] for b in top_brands)
        
        if total_sov > 0.7:
            return "high"
        elif total_sov > 0.4:
            return "medium"
        return "low"

    def _calculate_opportunity_score(self, market_size: int, competition: str) -> float:
        """Calculate opportunity score based on market size and competition"""
        base_score = min(market_size / 100000, 1.0)  # Normalize market size
        
        competition_multiplier = {
            "low": 1.0,
            "medium": 0.7,
            "high": 0.4
        }
        
        return base_score * competition_multiplier[competition]

    def _identify_market_leaders(self, brands: List[Dict]) -> List[Dict]:
        """Identify market leaders and their strengths"""
        return [{
            "brand": brand["brand"],
            "market_share": brand["combined_weighted_sov"],
            "avg_price": brand["combined_average_price"],
            "position": brand["combined_average_position"]
        } for brand in sorted(
            brands,
            key=lambda x: x["combined_weighted_sov"],
            reverse=True
        )[:5]]

    def validate_market(self, keyword: str) -> Dict[str, Any]:
        """Validate market opportunity"""
        response = self.tools[0].get_share_of_voice(keyword)
        data = response["data"]["attributes"]
        
        metrics = {
            "search_volume": data["estimated_30_day_search_volume"],
            "competition_score": sum(
                b["combined_weighted_sov"] 
                for b in sorted(
                    data["brands"],
                    key=lambda x: x["combined_weighted_sov"],
                    reverse=True
                )[:3]
            ),
            "price_range": self._analyze_price_range(data["brands"]),
            "market_leaders": self._identify_market_leaders(data["brands"])
        }
        
        is_valid = (
            metrics["search_volume"] > 10000 and
            metrics["competition_score"] < 0.7
        )
        
        return {
            "is_valid": is_valid,
            "metrics": metrics,
            "reasons": self._get_validation_reasons(metrics)
        }

    def _analyze_price_range(self, brands: List[Dict]) -> Dict[str, float]:
        """Analyze price distribution in the market"""
        prices = [b["combined_average_price"] for b in brands if b["combined_average_price"]]
        return {
            "min": min(prices),
            "max": max(prices),
            "average": sum(prices) / len(prices)
        }

    def _get_validation_reasons(self, metrics: Dict[str, Any]) -> List[str]:
        """Get detailed validation reasons based on metrics"""
        reasons = []
        
        if metrics["search_volume"] > 10000:
            reasons.append(f"Strong search volume: {metrics['search_volume']} monthly searches")
        else:
            reasons.append(f"Insufficient search volume: {metrics['search_volume']} monthly searches")
            
        if metrics["competition_score"] < 0.7:
            reasons.append("Manageable competition level with opportunity for entry")
        else:
            reasons.append("Market highly concentrated among top brands")
            
        price_range = metrics["price_range"]
        reasons.append(
            f"Price range: ${price_range['min']:.2f} - ${price_range['max']:.2f} "
            f"(avg: ${price_range['average']:.2f})"
        )
        
        return reasons