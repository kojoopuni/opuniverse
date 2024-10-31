# src/tools/amazon/test_jungle_scout.py
import os
from dotenv import load_dotenv
import logging
from pathlib import Path
from .junglescout_api import JungleScoutAPI
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_jungle_scout_api():
    """Test JungleScout API endpoints with proper error handling and data validation."""
    try:
        # Get the absolute path to the opuniverse directory
        current_dir = Path(__file__).resolve().parent
        root_dir = current_dir.parent.parent.parent.parent.parent
        env_path = root_dir / '.env'
        
        logger.info(f"Looking for .env file at: {env_path}")
        
        # Load .env file
        load_dotenv(env_path)
        
        # Get API key
        api_key = os.getenv('JUNGLE_SCOUT_API_KEY')
        if not api_key:
            logger.error(f"Failed to load API key from: {env_path}")
            raise ValueError("JungleScout API key not found in .env")
            
        logger.info("Successfully loaded JungleScout API key")
        
        # Initialize API
        js_api = JungleScoutAPI(
            api_key=api_key,
            api_name="inupo_goods",
            marketplace="us"
        )
        
        # Test Share of Voice
        logger.info("\nTesting Share of Voice...")
        test_keyword = "hammock"
        sov_data = js_api.get_share_of_voice(test_keyword)
        
        if "data" in sov_data and "attributes" in sov_data["data"]:
            attrs = sov_data["data"]["attributes"]
            
            # Log general metrics
            logger.info(f"\nKeyword: {test_keyword}")
            logger.info(f"30-Day Search Volume: {attrs['estimated_30_day_search_volume']:,}")
            logger.info(f"Product Count: {attrs['product_count']:,}")
            
            # Log top brands by share of voice
            if "brands" in attrs:
                top_brands = sorted(
                    attrs["brands"],
                    key=lambda x: x.get("combined_weighted_sov", 0),
                    reverse=True
                )[:5]
                
                logger.info("\nTop 5 Brands by Share of Voice:")
                for brand in top_brands:
                    logger.info(f"Brand: {brand['brand']}")
                    logger.info(f"Share of Voice: {brand['combined_weighted_sov']:.2%}")
                    logger.info(f"Products: {brand['combined_products']}")
                    logger.info(f"Avg Position: {brand['combined_average_position']:.1f}")
                    if brand.get('combined_average_price'):
                        logger.info(f"Avg Price: ${brand['combined_average_price']:.2f}")
                    logger.info("---")
            
            # Log top ASINs by conversion rate
            if "top_asins" in attrs:
                logger.info("\nTop ASINs by Conversion:")
                for asin in attrs["top_asins"]:
                    logger.info(f"ASIN: {asin['asin']}")
                    if asin.get('name'):
                        logger.info(f"Name: {asin['name']}")
                    if asin.get('brand'):
                        logger.info(f"Brand: {asin['brand']}")
                    logger.info(f"Clicks: {asin['clicks']:,}")
                    logger.info(f"Conversions: {asin['conversions']:,}")
                    logger.info(f"Conversion Rate: {asin['conversion_rate']:.2%}")
                    logger.info("---")
                
                # Log data period if available
                if attrs.get('top_asins_model_start_date') and attrs.get('top_asins_model_end_date'):
                    logger.info(f"\nData Period: {attrs['top_asins_model_start_date']} to {attrs['top_asins_model_end_date']}")
        
        logger.info("✅ Share of Voice test successful")
        
        return {
            "status": "success",
            "message": "Share of Voice test passed",
            "results": {
                "share_of_voice": sov_data,
                "api_usage": sov_data.get('headers', {}).get('X-API-Usage', 'N/A')
            }
        }
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_jungle_scout_api()