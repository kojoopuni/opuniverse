# src/n8n/nodes/amazon_research_node.py
from typing import Dict, Any
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tools.amazon.amz_market_research_tool import AmazonMarketResearchTool
from tools.amazon.amz_supplier_research_tool import AmazonSupplierResearchTool

logger = logging.getLogger(__name__)

class NodeInput(BaseModel):
    operation: str
    parameters: Dict[str, Any]
    jungle_scout_api_key: str

class AmazonResearchNode:
    def __init__(self):
        self.app = FastAPI()
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.post("/webhook/amazon-research")
        async def handle_webhook(input_data: NodeInput):
            try:
                return await self.execute(input_data.dict())
            except Exception as e:
                logger.error(f"Webhook error: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
    
    async def execute(self, params: Dict) -> Dict[str, Any]:
        """n8n node execution method"""
        try:
            # Initialize tools with API key
            self.market_research = AmazonMarketResearchTool(
                params['jungle_scout_api_key']
            )
            self.supplier_research = AmazonSupplierResearchTool(
                params['jungle_scout_api_key']
            )
            
            operation = params.get('operation')
            if operation == 'market_research':
                return await self._handle_market_research(params)
            elif operation == 'supplier_research':
                return await self._handle_supplier_research(params)
            else:
                raise ValueError(f"Unknown operation: {operation}")
                
        except Exception as e:
            logger.error(f"Node execution error: {str(e)}")
            raise
            
    async def _handle_market_research(self, params: Dict) -> Dict[str, Any]:
        """Handle market research operations"""
        try:
            keyword = params['parameters'].get('keyword')
            if not keyword:
                raise ValueError("Keyword is required for market research")
                
            return self.market_research._run(keyword)
        except Exception as e:
            logger.error(f"Market research error: {str(e)}")
            raise
            
    async def _handle_supplier_research(self, params: Dict) -> Dict[str, Any]:
        """Handle supplier research operations"""
        try:
            keyword = params['parameters'].get('keyword')
            if not keyword:
                raise ValueError("Keyword is required for supplier research")
                
            return self.supplier_research._run(keyword)
        except Exception as e:
            logger.error(f"Supplier research error: {str(e)}")
            raise

# Initialize node
amazon_research_node = AmazonResearchNode()
app = amazon_research_node.app
