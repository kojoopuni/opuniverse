# src/tools/amazon/junglescout_tool.py
# COMPLETE SCRIPT

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
    """Analyzes Amazon market data with specialized metrics for product selection.
    
    Args:
        keyword: The product keyword to analyze (e.g., "hammock")
    """
    try:
        # Ensure keyword is a string
        if not isinstance(keyword, str):
            keyword = str(keyword)
            
        # Call the API with just the keyword
        result = api.get_share_of_voice(keyword)
        
        if "data" not in result or "attributes" not in result["data"]:
            return "No market data available"
            
        attrs = result["data"]["attributes"]
        
        # Format comprehensive analysis
        response = [
            f"\nAdvanced Market Analysis for '{keyword}':",
            
            "\n1. Market Size and Demand:",
            f"- Monthly Search Volume: {attrs['estimated_30_day_search_volume']:,}",
            f"- Total Products: {attrs['product_count']:,}",
            f"- Market Saturation: {len(attrs.get('brands', [])) / attrs['product_count']:.2%}",
            
            "\n2. Competitive Landscape:",
            "Top Brands Performance:"
        ]
        
        # Add detailed brand analysis
        for brand in sorted(attrs.get('brands', [])[:5], key=lambda x: x['combined_weighted_sov'], reverse=True):
            market_dominance = (brand['combined_weighted_sov'] * 100) / brand['combined_average_position']
            response.extend([
                f"\n{brand['brand']}:",
                f"- Market Share: {brand['combined_weighted_sov']:.1%}",
                f"- Products: {brand['combined_products']}",
                f"- Average Position: {brand['combined_average_position']:.1f}",
                f"- Market Dominance Score: {market_dominance:.2f}"
            ])
        
        return "\n".join(response)
        
    except Exception as e:
        return f"Error analyzing market data: {str(e)}"