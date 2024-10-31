# src/tools/amazon/amz_market_research_tool.py
from crewai_tools import BaseTool
from typing import Dict, Any
import logging
from .jungle_scout_api import JungleScoutAPI

logger = logging.getLogger(__name__)

class AmazonMarketResearchTool(BaseTool):
    name: str = "Amazon Market Research"
    description: str = """
    Advanced Amazon marketplace analyzer using JungleScout data to identify:
    - High-demand products (>500 monthly sales)
    - Low competition niches (<100 reviews on top listings)
    - Profit margin potential (>30%)
    - US-based supplier opportunities
    - Keyword optimization potential
    """
    
    def __init__(self, jungle_scout_api_key: str):
        super().__init__()
        self.js_api = JungleScoutAPI(jungle_scout_api_key)
        
    def _run(self, keyword: str) -> Dict[str, Any]:
        """
        Main execution method integrating JungleScout data
        """
        try:
            # Get comprehensive market analysis
            market_data = self.js_api.find_dropshipping_opportunities(keyword)
            
            # Use available Growth Accelerator features
            keyword_data = self.js_api.keyword_scout(keyword)
            supplier_data = self.js_api.search_suppliers({"keyword": keyword})
            
            return {
                "market_analysis": {
                    "demand": market_data["market_analysis"]["demand"],
                    "competition": market_data["market_analysis"]["competition"],
                    "profitability": market_data["market_analysis"]["profitability"]
                },
                "keyword_insights": {
                    "search_volume": keyword_data.get("search_volume"),
                    "trending_keywords": keyword_data.get("trending_keywords"),
                    "ranking_difficulty": keyword_data.get("ranking_difficulty")
                },
                "supplier_options": {
                    "us_suppliers": supplier_data.get("us_suppliers"),
                    "shipping_times": supplier_data.get("shipping_times"),
                    "reliability_metrics": supplier_data.get("reliability_metrics")
                },
                "recommendations": self._generate_recommendations(
                    market_data, keyword_data, supplier_data
                )
            }
        except Exception as e:
            logger.error(f"Error in market research: {str(e)}")
            raise
            
    def _generate_recommendations(
        self,
        market_data: Dict[str, Any],
        keyword_data: Dict[str, Any],
        supplier_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate actionable recommendations"""
        try:
            return {
                "market_opportunity": self._assess_opportunity(market_data),
                "keyword_strategy": self._develop_keyword_strategy(keyword_data),
                "supplier_recommendations": self._evaluate_suppliers(supplier_data),
                "action_items": self._create_action_items(
                    market_data, keyword_data, supplier_data
                )
            }
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            raise