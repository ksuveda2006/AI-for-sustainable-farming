# FastAPI-based backend for sustainable farming system
import pandas as pd
from sqlalchemy import create_engine, text
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Sustainable Farming AI System")

# DB config
DATABASE_URL = "sqlite:///../farming.db"
engine = create_engine(DATABASE_URL)

# Load CSVs
try:
    farmer_data = pd.read_csv('../data/farmer_advisor_dataset.csv')
    market_data = pd.read_csv('../data/market_researcher_dataset.csv')
except FileNotFoundError:
    raise RuntimeError("Error: Dataset files not found in /data folder!")

# Request and Response models
class FarmerInput(BaseModel):
    name: str
    location: str
    farm_size: float
    soil_type: str
    water_availability: str
    preferred_crops: Optional[List[str]] = None
    budget: float

class Recommendation(BaseModel):
    crop_name: str
    sustainability_score: float
    profitability_score: float
    water_efficiency_score: float
    expected_yield: float
    estimated_profit: float
    water_requirement: float
    carbon_footprint: float

# Advisor Agent
class FarmerAdvisor:
    def __init__(self, farmer_data):
        self.farmer_data = farmer_data

    def analyze_farmer_profile(self, farmer_input: FarmerInput) -> dict:
        return {
            "soil_suitability": {"suitability": "high"},
            "water_efficiency": {"efficiency": "medium"},
            "farm_size_analysis": {"scale": "medium"}
        }

# Market Agent
class MarketResearcher:
    def __init__(self, market_data):
        self.market_data = market_data

    def analyze_market_trends(self, location: str, crop_list: List[str]) -> dict:
        return {
            "demand_trends": {"trends": {}},
            "price_trends": {"trends": {}},
            "profitability": {"scores": {}}
        }

@app.post("/analyze-farming-profile", response_model=Recommendation)
async def analyze_farming_profile(farmer_input: FarmerInput):
    try:
        farmer_advisor = FarmerAdvisor(farmer_data)
        market_researcher = MarketResearcher(market_data)

        farmer_analysis = farmer_advisor.analyze_farmer_profile(farmer_input)
        market_analysis = market_researcher.analyze_market_trends(
            farmer_input.location,
            farmer_input.preferred_crops or []
        )

        recommendation = _generate_recommendation(
            farmer_analysis, market_analysis, farmer_input
        )

        _store_recommendation(recommendation, farmer_input)
        return recommendation

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Dummy recommendation logic
def _generate_recommendation(farmer_analysis: dict, market_analysis: dict, farmer_input: FarmerInput) -> Recommendation:
    return Recommendation(
        crop_name="Sample Crop",
        sustainability_score=0.85,
        profitability_score=0.75,
        water_efficiency_score=0.90,
        expected_yield=1000.0,
        estimated_profit=5000.0,
        water_requirement=500.0,
        carbon_footprint=200.0
    )

# DB persistence
def _store_recommendation(recommendation: Recommendation, farmer_input: FarmerInput):
    with engine.connect() as conn:
        # Ensure tables exist
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS farmers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, location TEXT, farm_size REAL, 
                soil_type TEXT, water_availability TEXT
            );
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_id INTEGER, crop_id INTEGER, 
                sustainability_score REAL, 
                profitability_score REAL, 
                water_efficiency_score REAL
            );
        """))

        # Insert farmer and recommendation data
        result = conn.execute(text("""
            INSERT INTO farmers (name, location, farm_size, soil_type, water_availability)
            VALUES (:name, :location, :farm_size, :soil_type, :water_availability)
        """), {
            "name": farmer_input.name,
            "location": farmer_input.location,
            "farm_size": farmer_input.farm_size,
            "soil_type": farmer_input.soil_type,
            "water_availability": farmer_input.water_availability
        })
        farmer_id = result.lastrowid

        conn.execute(text("""
            INSERT INTO recommendations (
                farmer_id, crop_id, sustainability_score, 
                profitability_score, water_efficiency_score
            )
            VALUES (:farmer_id, :crop_id, :sustainability_score, 
                    :profitability_score, :water_efficiency_score)
        """), {
            "farmer_id": farmer_id,
            "crop_id": 1,
            "sustainability_score": recommendation.sustainability_score,
            "profitability_score": recommendation.profitability_score,
            "water_efficiency_score": recommendation.water_efficiency_score
        })

        conn.commit()

# Run with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
