import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

st.set_page_config(page_title="Water Pollution & Disease", page_icon="💧", layout="wide")

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "water_disease_model.pkl"

st.title("💧 Water Pollution & Disease Risk Prediction")
st.write("Predict the diarrheal disease risk category from water-quality and public-health indicators.")

if not MODEL_PATH.exists():
    st.error("Model file not found. Run `python train_model.py` first to create water_disease_model.pkl.")
    st.stop()

bundle = joblib.load(MODEL_PATH)
model = bundle["model"]
feature_columns = bundle["feature_columns"]
categorical_options = bundle["categorical_options"]

with st.sidebar:
    st.header("About")
    st.write("ML classification project based on water pollution, environmental and healthcare indicators.")
    st.write("Target: Diarrheal Risk Category — Low, Medium or High.")

st.subheader("Enter Input Values")

c1, c2, c3 = st.columns(3)

with c1:
    country = st.selectbox("Country", categorical_options.get("Country", ["Unknown"]))
    region = st.selectbox("Region", categorical_options.get("Region", ["Unknown"]))
    year = st.number_input("Year", 1990, 2100, 2024)
    water_source = st.selectbox("Water Source Type", categorical_options.get("Water Source Type", ["Unknown"]))
    treatment = st.selectbox("Water Treatment Method", categorical_options.get("Water Treatment Method", ["Unknown"]))
    contaminant = st.number_input("Contaminant Level (ppm)", min_value=0.0, value=5.0)
    ph = st.number_input("pH Level", min_value=0.0, max_value=14.0, value=7.0)

with c2:
    turbidity = st.number_input("Turbidity (NTU)", min_value=0.0, value=5.0)
    oxygen = st.number_input("Dissolved Oxygen (mg/L)", min_value=0.0, value=7.0)
    nitrate = st.number_input("Nitrate Level (mg/L)", min_value=0.0, value=10.0)
    lead = st.number_input("Lead Concentration (µg/L)", min_value=0.0, value=5.0)
    bacteria = st.number_input("Bacteria Count (CFU/mL)", min_value=0, value=100)
    clean_water = st.slider("Access to Clean Water (%)", 0.0, 100.0, 75.0)
    cholera = st.number_input("Cholera Cases / 100,000", min_value=0, value=10)

with c3:
    typhoid = st.number_input("Typhoid Cases / 100,000", min_value=0, value=10)
    infant_mortality = st.number_input("Infant Mortality Rate", min_value=0.0, value=20.0)
    gdp = st.number_input("GDP per Capita (USD)", min_value=0, value=10000)
    healthcare = st.slider("Healthcare Access Index", 0.0, 100.0, 60.0)
    urbanization = st.slider("Urbanization Rate (%)", 0.0, 100.0, 50.0)
    sanitation = st.slider("Sanitation Coverage (%)", 0.0, 100.0, 70.0)
    rainfall = st.number_input("Rainfall (mm/year)", min_value=0, value=1000)
    temperature = st.number_input("Temperature (°C)", value=25.0)
    population_density = st.number_input("Population Density (people/km²)", min_value=0, value=300)

input_data = pd.DataFrame([{
    "Country": country,
    "Region": region,
    "Year": year,
    "Water Source Type": water_source,
    "Contaminant Level (ppm)": contaminant,
    "pH Level": ph,
    "Turbidity (NTU)": turbidity,
    "Dissolved Oxygen (mg/L)": oxygen,
    "Nitrate Level (mg/L)": nitrate,
    "Lead Concentration (µg/L)": lead,
    "Bacteria Count (CFU/mL)": bacteria,
    "Water Treatment Method": treatment,
    "Access to Clean Water (% of Population)": clean_water,
    "Cholera Cases per 100,000 people": cholera,
    "Typhoid Cases per 100,000 people": typhoid,
    "Infant Mortality Rate (per 1,000 live births)": infant_mortality,
    "GDP per Capita (USD)": gdp,
    "Healthcare Access Index (0-100)": healthcare,
    "Urbanization Rate (%)": urbanization,
    "Sanitation Coverage (% of Population)": sanitation,
    "Rainfall (mm per year)": rainfall,
    "Temperature (°C)": temperature,
    "Population Density (people per km²)": population_density,
}])

input_data = input_data.reindex(columns=feature_columns)

if st.button("Predict Disease Risk", type="primary", use_container_width=True):
    prediction = model.predict(input_data)[0]
    st.subheader("Prediction")
    if prediction == "Low":
        st.success(f"Diarrheal Risk: {prediction}")
    elif prediction == "Medium":
        st.warning(f"Diarrheal Risk: {prediction}")
    else:
        st.error(f"Diarrheal Risk: {prediction}")
    st.caption("This prediction is for educational/project purposes and is not medical advice.")
