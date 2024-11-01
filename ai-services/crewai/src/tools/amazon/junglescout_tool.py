# src/tools/amazon/junglescout_tool.py

from typing import Dict, Any
import os
from crewai_tools import tool
from .junglescout_api import JungleScoutAPI

# Initialize the API client
api = JungleScoutAPI(
    api_key=os.getenv('JUNGLE_SCOUT_API_KEY'),
    api_name="inupo_goods"
)

@tool("Amazon Market Research")
def analyze_market(keyword: str) -> str:
    """Analyzes Amazon market data for a given keyword using JungleScout.
    
    Args:
        keyword: The product keyword to analyze (e.g., "hammock", "yoga mat")
        
    Returns:
        Detailed market analysis including search volume, top brands, and metrics
    """
    try:
        result = api.get_share_of_voice(keyword)
        
        if "data" not in result or "attributes" not in result["data"]:
            return "No market data available"
            
        attrs = result["data"]["attributes"]
        
        # Format the response
        response = [
            f"\nMarket Analysis for '{keyword}':",
            f"Monthly Search Volume: {attrs['estimated_30_day_search_volume']:,}",
            f"Total Products: {attrs['product_count']:,}"
        ]
        
        if attrs.get('brands'):
            response.append("\nTop Brands by Market Share:")
            sorted_brands = sorted(
                attrs['brands'],
                key=lambda x: x['combined_weighted_sov'],
                reverse=True
            )[:5]
            
            for brand in sorted_brands:
                response.extend([
                    f"- {brand['brand']}:",
                    f"  Share of Voice: {brand['combined_weighted_sov']:.1%}",
                    f"  Products: {brand['combined_products']}",
                    f"  Avg Position: {brand['combined_average_position']:.1f}"
                ])
        
        return "\n".join(response)
        
    except Exception as e:
        return f"Error analyzing market data: {str(e)}"