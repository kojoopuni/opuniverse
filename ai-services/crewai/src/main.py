from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelne)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Define our CrewAI modes
class CrewAIMode(Enum):
    """
    Enum to distinguish between Enterprise and Self-hosted modes
    """
    ENTERPRISE = "enterprise"
    SELF_HOSTED = "self_hosted"

# Define our request/response models
class CrewConfig(BaseModel):
    """
    Pydantic model for crew configuration
    
    Attributes:
        mode: Specifies whether to use Enterprise or Self-hosted mode
        config: Dictionary containing crew configuration details
        name: Optional name for the crew
    """
    mode: CrewAIMode
    config: Dict[str, Any]
    name: Optional[str] = None

class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str
    version: str
    mode: str

class RootResponse(BaseModel):
    """Response model for root endpoint"""
    service: str
    documentation: str
    health: str

class CrewResponse(BaseModel):
    """Response model for crew creation endpoint"""
    status: str
    mode: str
    crew_id: str
    details: Dict[str, Any]

# Initialize FastAPI app with metadata
app = FastAPI(
    title="CrewAI Service",
    description="Dual-mode CrewAI service supporting both Enterprise and Self-hosted operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=RootResponse)
async def root():
    """Root endpoint with service information"""
    return {
        "service": "Opuniverse AI Orchestration",
        "documentation": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify service status
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "mode": "dual"
    }

@app.post("/crews/create", response_model=CrewResponse)
async def create_crew(crew_config: CrewConfig):
    """
    Create a new crew based on specified mode and configuration
    
    Args:
        crew_config: CrewConfig object containing mode and configuration
    
    Returns:
        Dict containing crew creation status and details
    
    Raises:
        HTTPException: If crew creation fails
    """
    try:
        logger.info(f"Creating crew in {crew_config.mode} mode")
        
        if crew_config.mode == CrewAIMode.ENTERPRISE:
            # Import here to avoid circular imports
            from enterprise_bridge.service import EnterpriseCrewService
            service = EnterpriseCrewService()
        else:
            from self_hosted.service import SelfHostedCrewService
            service = SelfHostedCrewService()
            
        result = await service.create_crew(crew_config.config)
        
        logger.info(f"Successfully created crew in {crew_config.mode} mode")
        return {
            "status": "success",
            "mode": crew_config.mode.value,
            "crew_id": result.get("crew_id"),
            "details": result
        }
        
    except Exception as e:
        logger.error(f"Error creating crew: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Enable auto-reload during development
    )