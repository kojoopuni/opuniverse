# src/tools/search/web_search.py
import os
from serpapi import GoogleSearch
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class WebSearchTool:
    """Web search implementation using SerpAPI"""
    
    def __init__(self):
        self.api_key = os.getenv('SERP_API_KEY')
        if not self.api_key:
            raise ValueError("SERP_API_KEY not found in environment variables")
            
    def search(self, query: str) -> Dict[str, Any]:
        """Perform web search using SerpAPI"""
        try:
            search = GoogleSearch({
                "q": query,
                "api_key": self.api_key,
                "engine": "google",
                "num": 10,  # Limit results to conserve quota
                "gl": "us"  # Set to US results
            })
            
            results = search.get_dict()
            
            # Extract and format relevant data
            organic_results = results.get("organic_results", [])
            
            if not organic_results:
                logger.warning("No results found for query")
                return {
                    "status": "success",
                    "results": [],
                    "total_results": 0
                }
            
            formatted_results = [{
                "title": result.get("title"),
                "link": result.get("link"),
                "snippet": result.get("snippet"),
                "position": result.get("position")
            } for result in organic_results]
            
            return {
                "status": "success",
                "results": formatted_results,
                "total_results": len(formatted_results)
            }
            
        except Exception as e:
            logger.error(f"SerpAPI search failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }