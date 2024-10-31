# src/tools/amazon/junglescout_api.py
from typing import Dict, Any, Optional, List
import logging
import requests
from datetime import datetime
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class BrandMetrics(BaseModel):
    """
    Model for brand performance metrics in Amazon search results.
    
    Attributes:
        brand: Brand name
        combined_products: Total products (organic + sponsored)
        combined_weighted_sov: Overall share of voice (weighted)
        combined_basic_sov: Basic share of voice
        combined_average_position: Average position in search results
        combined_average_price: Average price across all products
        organic_products: Number of organic listings
        organic_weighted_sov: Share of voice for organic listings
        organic_basic_sov: Basic share for organic listings
        organic_average_position: Average organic position
        organic_average_price: Average price of organic listings
        sponsored_products: Number of sponsored listings
        sponsored_weighted_sov: Share of voice for sponsored listings
        sponsored_basic_sov: Basic share for sponsored listings
        sponsored_average_position: Average sponsored position
        sponsored_average_price: Average price of sponsored listings
    """
    brand: str
    combined_products: int
    combined_weighted_sov: float
    combined_basic_sov: float
    combined_average_position: float
    combined_average_price: float
    organic_products: int
    organic_weighted_sov: float
    organic_basic_sov: float
    organic_average_position: Optional[float]
    organic_average_price: Optional[float]
    sponsored_products: int
    sponsored_weighted_sov: float
    sponsored_basic_sov: float
    sponsored_average_position: Optional[float]
    sponsored_average_price: Optional[float]

class TopAsin(BaseModel):
    """
    Model for top performing ASINs data.
    
    Attributes:
        asin: Amazon Standard Identification Number
        name: Product name (optional)
        brand: Brand name (optional)
        clicks: Number of clicks received
        conversions: Number of conversions
        conversion_rate: Conversion rate (conversions/clicks)
    """
    asin: str
    name: Optional[str]
    brand: Optional[str]
    clicks: int
    conversions: int
    conversion_rate: float

class ShareOfVoiceAttributes(BaseModel):
    """
    Model for Share of Voice response attributes.
    
    Attributes:
        estimated_30_day_search_volume: Monthly search volume
        exact_suggested_bid_median: Suggested PPC bid
        product_count: Number of products analyzed
        updated_at: Last data refresh timestamp
        brands: List of brand performance metrics
        top_asins: List of top performing ASINs
        top_asins_model_start_date: Start date for top ASINs data
        top_asins_model_end_date: End date for top ASINs data
    """
    estimated_30_day_search_volume: int
    exact_suggested_bid_median: Optional[float]
    product_count: int
    updated_at: str
    brands: List[BrandMetrics]
    top_asins: List[TopAsin]
    top_asins_model_start_date: Optional[str]
    top_asins_model_end_date: Optional[str]

class JungleScoutAPI:
    """
    JungleScout API client for Amazon marketplace research and analysis.
    
    This client provides access to:
    - Share of Voice analysis
    - Keyword research
    - Sales estimates
    - Product database
    - Historical data
    """

    def __init__(self, api_key: str, api_name: str = "inupo_goods", marketplace: str = "us"):
        """
        Initialize the API client.
        
        Args:
            api_key: Your JungleScout API key
            api_name: Your API client identifier
            marketplace: Target marketplace (us, uk, de, etc.)
        """
        self.api_key = api_key
        self.api_name = api_name
        self.marketplace = marketplace.lower()
        self.base_url = "https://developer.junglescout.com"
        self.headers = {
            "Authorization": f"{api_name}:{api_key}",
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.junglescout.v1+json",
            "X-API-Type": "junglescout"
        }

    def get_share_of_voice(self, keyword: str) -> Dict[str, Any]:
        """
        Get Share of Voice data for a keyword search on Amazon.
        
        This endpoint provides:
        - Brand control for first 3 pages of search results
        - Organic and sponsored performance metrics
        - PPC bid suggestions
        - 30-day search volume
        - Top 3 ASINs conversion rates (past week)
        
        Args:
            keyword: The keyword to analyze
            
        Returns:
            Dict containing share of voice metrics and brand performance data
        """
        try:
            endpoint = f"{self.base_url}/api/share_of_voice"
            params = {
                "marketplace": self.marketplace,
                "keyword": keyword
            }
            
            response = self._make_request("GET", endpoint, params=params)
            
            # Process and validate response
            if "data" in response and "attributes" in response["data"]:
                try:
                    attributes = ShareOfVoiceAttributes(**response["data"]["attributes"])
                    
                    # Log summary metrics
                    logger.info(f"\nKeyword: {keyword}")
                    logger.info(f"30-Day Search Volume: {attributes.estimated_30_day_search_volume:,}")
                    if attributes.exact_suggested_bid_median:
                        logger.info(f"Suggested Bid: ${attributes.exact_suggested_bid_median:.2f}")
                    logger.info(f"Product Count: {attributes.product_count:,}")
                    
                    # Log top brands by share of voice
                    top_brands = sorted(
                        attributes.brands, 
                        key=lambda x: x.combined_weighted_sov, 
                        reverse=True
                    )[:5]
                    
                    logger.info("\nTop 5 Brands by Share of Voice:")
                    for brand in top_brands:
                        logger.info(f"Brand: {brand.brand}")
                        logger.info(f"Share of Voice: {brand.combined_weighted_sov:.2%}")
                        logger.info(f"Products: {brand.combined_products}")
                        logger.info(f"Avg Position: {brand.combined_average_position:.1f}")
                        logger.info("---")
                    
                except Exception as e:
                    logger.error(f"Error processing response: {str(e)}")
                
            return response
            
        except Exception as e:
            logger.error(f"Share of voice error: {str(e)}")
            raise

    def _make_request(self, method: str, endpoint: str, params: Dict = None, json: Dict = None) -> Dict[str, Any]:
        """
        Make API request with error handling and logging.
        
        Args:
            method: HTTP method (GET, POST)
            endpoint: API endpoint URL
            params: Query parameters
            json: JSON request body
            
        Returns:
            Dict containing API response data
            
        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        try:
            logger.info(f"Making request to: {endpoint}")
            logger.info(f"Headers: {self.headers}")
            logger.info(f"Params: {params}")
            logger.info(f"JSON data: {json}")
            
            response = requests.request(
                method=method,
                url=endpoint,
                headers=self.headers,
                params=params,
                json=json
            )
            
            logger.info(f"Response Status: {response.status_code}")
            logger.info(f"Response Headers: {response.headers}")
            
            if response.status_code != 200:
                logger.error(f"Response Text: {response.text}")
                
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request error: {str(e)}")
            raise