import streamlit as st
import requests
import json

st.set_page_config(page_title="Sustainable Farming AI Advisor", layout="wide")
st.title("🌾 Sustainable Farming Multi-Agent AI System")

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

if submit:
    with st.spinner("Analyzing your farm profile with AI agents..."):
        payload = {
            "name": name,
            "location": location,
            "farm_size": farm_size,
            "soil_type": soil_type,
            "water_availability": water_availability,
            "budget": budget,
            "preferred_crops": preferred_crops
        }

        try:
            response = requests.post("http://localhost:8000/analyze-farming-profile", data=json.dumps(payload))
            if response.status_code == 200:
                result = response.json()

                st.success("✅ Recommendation Received")
                st.markdown("### 🌿 Recommended Crop: ")
                st.write(result['crop_name'])
                st.markdown("---")

                col1, col2, col3 = st.columns(3)
                col1.metric("📈 Sustainability Score", f"{result['sustainability_score']:.2f}")
                col2.metric("💼 Profitability Score", f"{result['profitability_score']:.2f}")
                col3.metric("💧 Water Efficiency", f"{result['water_efficiency_score']:.2f}")

                st.markdown("---")
                st.subheader("📊 Additional Details")
                st.write(f"**Expected Yield:** {result['expected_yield']} kg")
                st.write(f"**Estimated Profit:** ₹{result['estimated_profit']:.2f}")
                st.write(f"**Water Requirement:** {result['water_requirement']} litres")
                st.write(f"**Carbon Footprint:** {result['carbon_footprint']} CO₂ units")

            else:
                st.error(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"Failed to connect to backend API: {e}")
