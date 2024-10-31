# src/agents/amazon/listing_optimizer.py
class ListingOptimizerAgent(Agent):
    """Listing Optimization Specialist focusing on conversion rate optimization"""
    
    def __init__(self, name: str = "Alexandra Rivera", **kwargs):
        super().__init__(
            name=name,
            role="Listing Optimization Expert",
            goal="""Maximize product visibility and conversion rates through data-driven 
            listing optimization and strategic keyword implementation""",
            backstory="""Former Amazon A9 Algorithm Specialist with deep expertise in 
            search ranking factors and buyer psychology. Optimized over 5,000 listings 
            achieving 156% average increase in conversion rates. Expert in keyword 
            optimization, content strategy, and A/B testing methodologies.""",
            tools=[JungleScoutAPI(), GPT4API()],
            verbose=True,
            allow_delegation=True
        )

    def optimize_listing(self, product_data: Dict, market_data: Dict) -> Dict[str, Any]:
        """Optimize product listing for maximum visibility and conversion"""
        keywords = self._analyze_keywords(market_data)
        return {
            "optimized_title": self._create_title(product_data, keywords),
            "bullet_points": self._create_bullets(product_data, keywords),
            "description": self._create_description(product_data, keywords)
        }