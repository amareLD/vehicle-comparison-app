from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from pathlib import Path
import os
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from vehicleanalyst.crew import VehicleanalystCrew

app = FastAPI(title="Vehicle Analyst API", version="1.0.0")

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VehicleAnalysisRequest(BaseModel):
    vehicle1: str
    vehicle2: str

class VehicleAnalysisResponse(BaseModel):
    status: str
    vehicle1: str
    vehicle2: str
    comparison_report: str
    advertisements: dict
    message: str

@app.get("/")
async def root():
    return {"message": "Vehicle Analyst API is running!", "status": "healthy"}

@app.post("/api/v1/analyze-vehicles", response_model=VehicleAnalysisResponse)
async def analyze_vehicles(request: VehicleAnalysisRequest):
    try:
        # Validate input
        if not request.vehicle1.strip() or not request.vehicle2.strip():
            raise HTTPException(status_code=400, detail="Both vehicle models are required")
        
        # Initialize the crew
        crew_instance = VehicleanalystCrew().crew()
        
        # Prepare inputs
        inputs = {
            "vehicle1": request.vehicle1.strip(),
            "vehicle2": request.vehicle2.strip()
        }
        
        # Run the crew
        result = crew_instance.kickoff(inputs=inputs)
        
        # Process results
        return VehicleAnalysisResponse(
            status="success",
            vehicle1=request.vehicle1,
            vehicle2=request.vehicle2,
            comparison_report=str(result),
            advertisements={},  # You can extract specific task outputs here
            message="Analysis completed successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.get("/api/v1/test")
async def test_endpoint():
    return {"message": "Test endpoint working", "data": {"test": True}}