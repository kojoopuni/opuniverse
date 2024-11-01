# src/crews/amazon/amazon_memory_store.py

from ..memory_store import BaseMemoryStore
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class AmazonMemoryStore(BaseMemoryStore):
    """Amazon-specific memory store implementation"""
    
    def __init__(self, storage_dir: str = "memory"):
        super().__init__(storage_dir)
        
        # Amazon-specific categories
        self.categories = {
            "market_research": self.storage_dir / "amazon_market_research.json",
            "competition": self.storage_dir / "amazon_competition.json",
            "products": self.storage_dir / "amazon_products.json",
            "pricing": self.storage_dir / "amazon_pricing.json",
            "suppliers": self.storage_dir / "amazon_suppliers.json",
            "listings": self.storage_dir / "amazon_listings.json",
            "trends": self.storage_dir / "amazon_trends.json"
        }
        
        self._initialize_storage()

    def store_market_insight(self, keyword: str, data: Dict[str, Any]):
        """Store Amazon market research data from Share of Voice API"""
        processed_data = {
            "timestamp": datetime.now().isoformat(),
            "search_volume": data["data"]["attributes"]["estimated_30_day_search_volume"],
            "product_count": data["data"]["attributes"]["product_count"],
            "top_brands": self._extract_top_brands(data["data"]["attributes"]["brands"]),
            "competition_level": self._calculate_competition_level(data["data"]["attributes"]["brands"]),
            "raw_data": data
        }
        self._store_data("market_research", keyword, processed_data)

    def store_competition_analysis(self, keyword: str, data: Dict[str, Any]):
        """Store competition analysis results"""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "market_leaders": self._identify_market_leaders(data["data"]["attributes"]["brands"]),
            "market_gaps": self._identify_market_gaps(data["data"]["attributes"]["brands"]),
            "raw_data": data
        }
        self._store_data("competition", keyword, analysis)

    def store_product_validation(self, product_id: str, data: Dict[str, Any]):
        """Store product validation results"""
        validation = {
            "timestamp": datetime.now().isoformat(),
            "validation_score": data.get("validation_score"),
            "profit_potential": data.get("profit_potential"),
            "risk_factors": data.get("risk_factors"),
            "raw_data": data
        }
        self._store_data("products", product_id, validation)

    def _extract_top_brands(self, brands: List[Dict]) -> List[Dict]:
        """Extract top 5 brands by market share"""
        return sorted(
            brands,
            key=lambda x: x["combined_weighted_sov"],
            reverse=True
        )[:5]

    def _calculate_competition_level(self, brands: List[Dict]) -> str:
        """Calculate competition level based on Share of Voice distribution"""
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

    def _identify_market_gaps(self, brands: List[Dict]) -> List[Dict]:
        """Identify potential market gaps based on price and competition"""
        price_ranges = {
            "budget": {"min": 0, "max": 30},
            "mid_range": {"min": 30, "max": 100},
            "premium": {"min": 100, "max": float('inf')}
        }
        
        gaps = []
        for price_segment, range_vals in price_ranges.items():
            segment_brands = [
                b for b in brands 
                if range_vals["min"] <= b["combined_average_price"] < range_vals["max"]
            ]
            
            total_sov = sum(b["combined_weighted_sov"] for b in segment_brands)
            
            if total_sov < 0.2:  # Less than 20% market share indicates a gap
                gaps.append({
                    "price_segment": price_segment,
                    "current_share": total_sov,
                    "price_range": range_vals,
                    "competitors": len(segment_brands)
                })
        
        return gaps

    def get_market_insight(self, keyword: str) -> Optional[Dict[str, Any]]:
        """Retrieve market research data"""
        return self._get_data("market_research", keyword)

    def get_competition_analysis(self, keyword: str) -> Optional[Dict[str, Any]]:
        """Retrieve competition analysis"""
        return self._get_data("competition", keyword)

    def get_product_validation(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve product validation data"""
        return self._get_data("products", product_id)