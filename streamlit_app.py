import streamlit as st
from typing import List, Optional
import pandas as pd
from pydantic import BaseModel

st.set_page_config(page_title="Sustainable Farming AI Advisor", layout="wide")
st.title("🌾 Sustainable Farming Multi-Agent AI System")

# Load datasets
@st.cache_data
def load_datasets():
    farmer_data = pd.read_csv("data/farmer_advisor_dataset.csv")
    market_data = pd.read_csv("data/market_researcher_dataset.csv")
    return farmer_data, market_data

farmer_data, market_data = load_datasets()

# Input and Recommendation Models
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

class FarmerAdvisor:
    def __init__(self, farmer_data):
        self.farmer_data = farmer_data

    def analyze_farmer_profile(self, farmer_input: FarmerInput) -> dict:
        return {
            "soil_suitability": {"suitability": "high"},
            "water_efficiency": {"efficiency": "medium"},
            "farm_size_analysis": {"scale": "medium"}
        }

class MarketResearcher:
    def __init__(self, market_data):
        self.market_data = market_data

    def analyze_market_trends(self, location: str, crop_list: List[str]) -> dict:
        return {
            "demand_trends": {"trends": {}, "recommendations": []},
            "price_trends": {"trends": {}, "recommendations": []},
            "profitability": {"scores": {}, "recommendations": []}
        }

def _generate_recommendation(farmer_analysis: dict, market_analysis: dict, farmer_input: FarmerInput) -> Recommendation:
    return Recommendation(
        crop_name="Wheat",
        sustainability_score=0.87,
        profitability_score=0.78,
        water_efficiency_score=0.91,
        expected_yield=1200.0,
        estimated_profit=6500.0,
        water_requirement=480.0,
        carbon_footprint=180.0
    )

# Input form
with st.form("farmer_input_form"):
    st.subheader("🧬 Enter Your Farming Details")
    name = st.text_input("Name")
    location = st.text_input("Location")
    farm_size = st.number_input("Farm Size (in acres)", min_value=0.0, format="%f")
    soil_type = st.selectbox("Soil Type", ["Loamy", "Sandy", "Clay", "Silty", "Peaty", "Chalky"])
    water_availability = st.selectbox("Water Availability", ["Low", "Medium", "High"])
    budget = st.number_input("Budget (in INR)", min_value=0.0, format="%f")
    preferred_crops = st.multiselect("Preferred Crops", ["Wheat", "Rice", "Maize", "Soybean", "Sugarcane", "Cotton"])

    submit = st.form_submit_button("Get Recommendation")

# On submit
if submit:
    with st.spinner("Analyzing your farm profile with AI agents..."):
        farmer_input = FarmerInput(
            name=name,
            location=location,
            farm_size=farm_size,
            soil_type=soil_type,
            water_availability=water_availability,
            budget=budget,
            preferred_crops=preferred_crops or []
        )

        farmer_agent = FarmerAdvisor(farmer_data)
        market_agent = MarketResearcher(market_data)

        farmer_analysis = farmer_agent.analyze_farmer_profile(farmer_input)
        market_analysis = market_agent.analyze_market_trends(farmer_input.location, farmer_input.preferred_crops)

        result = _generate_recommendation(farmer_analysis, market_analysis, farmer_input)

        st.success("✅ Recommendation Received")
        st.markdown("### 🌿 Recommended Crop: ")
        st.write(result.crop_name)
        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        col1.metric("📈 Sustainability Score", f"{result.sustainability_score:.2f}")
        col2.metric("💼 Profitability Score", f"{result.profitability_score:.2f}")
        col3.metric("💧 Water Efficiency", f"{result.water_efficiency_score:.2f}")

        st.markdown("---")
        st.subheader("📊 Additional Details")
        st.write(f"**Expected Yield:** {result.expected_yield} kg")
        st.write(f"**Estimated Profit:** ₹{result.estimated_profit:.2f}")
        st.write(f"**Water Requirement:** {result.water_requirement} litres")
        st.write(f"**Carbon Footprint:** {result.carbon_footprint} CO₂ units")
