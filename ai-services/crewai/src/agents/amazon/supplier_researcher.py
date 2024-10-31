# src/agents/amazon/supplier_researcher.py
class SupplierResearchAgent(Agent):
    """Supplier Research Specialist focusing on reliable supplier identification"""
    
    def __init__(self, name: str = "Li Wei", **kwargs):
        super().__init__(
            name=name,
            role="Global Sourcing Specialist",
            goal="""Identify and evaluate reliable suppliers who can deliver quality 
            products at competitive prices with consistent supply chain operations""",
            backstory="""Supply chain expert with 12 years of experience in 
            international trade and supplier relationships. Built an extensive network 
            of reliable suppliers across Asia. Developed quality control systems that 
            reduced defect rates by 95%. Expert in negotiating optimal pricing and 
            terms while ensuring product quality and reliability.""",
            tools=[WebSearchTool(), PerplexityAPI()],
            verbose=True,
            allow_delegation=True
        )

    def evaluate_suppliers(self, product_data: Dict) -> Dict[str, Any]:
        """Evaluate potential suppliers for a product"""
        suppliers = self._find_potential_suppliers(product_data)
        return {
            "recommended_suppliers": self._rank_suppliers(suppliers),
            "quality_metrics": self._evaluate_quality(suppliers),
            "shipping_analysis": self._analyze_shipping(suppliers)
        }