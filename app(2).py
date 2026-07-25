import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="AquaGuard AI | Water Pollution & Disease Prediction",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- CUSTOM DESIGN --------------------
st.markdown("""
<style>
    .stApp {
        background:
            radial-gradient(circle at 10% 5%, rgba(0, 180, 216, .18), transparent 26%),
            radial-gradient(circle at 90% 10%, rgba(72, 202, 228, .12), transparent 24%),
            linear-gradient(145deg, #03111d 0%, #071b2b 55%, #04121e 100%);
    }
    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 4rem;
        max-width: 1280px;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(3,20,34,.99), rgba(5,34,51,.97));
        border-right: 1px solid rgba(72,202,228,.18);
    }
    [data-testid="stSidebar"] * { color: #e8f8ff; }
    .hero {
        position: relative;
        overflow: hidden;
        padding: 3.2rem;
        border-radius: 30px;
        background:
            radial-gradient(circle at 90% 15%, rgba(72,202,228,.26), transparent 27%),
            linear-gradient(135deg, rgba(5,54,82,.96), rgba(3,27,45,.92));
        border: 1px solid rgba(72,202,228,.28);
        box-shadow: 0 28px 70px rgba(0,0,0,.28);
        margin-bottom: 1.8rem;
    }
    .hero::after {
        content: "◌";
        position: absolute;
        right: 5%;
        top: -70px;
        font-size: 250px;
        color: rgba(144,224,239,.08);
    }
    .hero h1 {
        font-size: clamp(2.6rem, 5vw, 4.5rem);
        letter-spacing: -0.05em;
        line-height: 1.03;
        color: #f3fcff;
        margin: 0 0 .5rem 0;
    }
    .hero p {
        font-size: 1.05rem;
        opacity: .85;
        max-width: 850px;
    }
    .info-card {
        min-height: 190px;
        padding: 1.45rem;
        border-radius: 22px;
        background: linear-gradient(145deg, rgba(14,49,70,.80), rgba(6,29,45,.74));
        border: 1px solid rgba(72,202,228,.18);
        box-shadow: 0 14px 35px rgba(0,0,0,.16);
        margin-bottom: 1rem;
        transition: transform .25s ease, border-color .25s ease;
    }
    .info-card:hover {
        transform: translateY(-5px);
        border-color: rgba(72,202,228,.48);
    }
    .info-card h3 { color: #f4fcff; }
    .info-card p { color: #a9c5d5; line-height: 1.65; }
    .result-card {
        padding: 2rem;
        border-radius: 24px;
        background:
            radial-gradient(circle at 90% 20%, rgba(72,202,228,.18), transparent 30%),
            linear-gradient(135deg, rgba(7,55,80,.95), rgba(4,31,48,.95));
        border: 1px solid rgba(72,202,228,.34);
        box-shadow: 0 20px 50px rgba(0,0,0,.22);
    }
    div[data-testid="stForm"] {
        background: rgba(5,28,44,.70);
        border: 1px solid rgba(72,202,228,.18);
        border-radius: 24px;
        padding: 1.4rem;
        box-shadow: 0 20px 50px rgba(0,0,0,.14);
    }
    div[data-testid="stMetric"] {
        background: rgba(7,34,51,.75);
        border: 1px solid rgba(72,202,228,.18);
        border-radius: 18px;
        padding: 1rem;
    }
    .stButton > button, .stFormSubmitButton > button {
        border: 0 !important;
        border-radius: 13px !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg,#00b4d8,#48cae4) !important;
        color: #00131f !important;
        box-shadow: 0 10px 28px rgba(0,180,216,.24);
    }
    .footer {
        text-align: center;
        opacity: .65;
        padding-top: 2rem;
        font-size: .9rem;
    }
</style>
""", unsafe_allow_html=True)


# -------------------- LOAD ML ARTIFACTS --------------------
@st.cache_resource
def load_artifacts():
    model = joblib.load("best_water_pollution_disease_model.pkl")
    label_encoders = joblib.load("label_encoders.pkl")
    feature_names = joblib.load("feature_names.pkl")
    return model, label_encoders, feature_names


try:
    model, label_encoders, feature_names = load_artifacts()
except Exception as e:
    st.error(f"Could not load deployment files: {e}")
    st.info("Make sure the model, label_encoders.pkl and feature_names.pkl are in the same GitHub folder as app.py.")
    st.stop()


# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.title("💧 AquaGuard AI")
    st.caption("Water Pollution & Disease Prediction")
    st.divider()

    page = st.radio(
        "Navigation",
        ["🏠 Home", "🔬 Make Prediction", "📊 Model Information", "ℹ️ About Project"]
    )

    st.divider()
    st.markdown("### System Status")
    st.success("ML model loaded")
    st.caption(f"Expected input features: {len(feature_names)}")

    st.divider()
    st.caption("Machine-learning project for educational and analytical purposes.")


# -------------------- HOME --------------------
if page == "🏠 Home":
    st.markdown("""
    <div class="hero">
        <h1>💧 AquaGuard AI<br>Water Intelligence Platform</h1>
        <p>
            Transform water-quality, environmental, public-health and socioeconomic indicators
            into an interactive machine-learning prediction experience — designed for clarity,
            speed and environmental awareness.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>🌊 Water Quality</h3>
            <p>Analyze contamination, pH, turbidity, dissolved oxygen, nitrate, lead and bacteria indicators.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>🤖 Machine Learning</h3>
            <p>The application uses your trained classification model and preserves the feature order used during training.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-card">
            <h3>🌍 Public Health Context</h3>
            <p>Combine environmental, disease, sanitation, healthcare and socioeconomic indicators in one prediction workflow.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### ✨ Why AquaGuard AI?")
    x1, x2, x3, x4 = st.columns(4)
    x1.metric("Model Inputs", len(feature_names))
    x2.metric("Categorical Inputs", "4")
    x3.metric("Prediction", "Instant")
    x4.metric("Platform", "Streamlit")

    st.markdown("---")
    st.subheader("How it works")
    st.write(
        "Open **Make Prediction**, enter the required water-quality and environmental values, "
        "and submit the form. Categorical values are encoded using the saved training encoders "
        "before the model generates its prediction."
    )

    st.info("This application is a machine-learning project and should not be used as a substitute for professional medical or public-health advice.")


# -------------------- PREDICTION --------------------
elif page == "🔬 Make Prediction":
    st.markdown("""
    <div class="hero">
        <h1>🔬 Disease Risk Prediction</h1>
        <p>Complete the fields below. The application will transform the inputs using the saved encoders and send the 23 features to the trained ML model.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("prediction_form"):
        st.subheader("📍 Location & Water Source")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            country = st.selectbox("Country", list(label_encoders["Country"].classes_))
        with c2:
            region = st.selectbox("Region", list(label_encoders["Region"].classes_))
        with c3:
            year = st.number_input("Year", min_value=1900, max_value=2100, value=2025, step=1)
        with c4:
            water_source = st.selectbox("Water Source Type", list(label_encoders["Water Source Type"].classes_))

        st.divider()
        st.subheader("💧 Water Quality Indicators")
        c1, c2, c3 = st.columns(3)
        with c1:
            contaminant = st.number_input("Contaminant Level (ppm)", min_value=0.0, value=0.0)
            ph = st.number_input("pH Level", min_value=0.0, max_value=14.0, value=7.0)
            turbidity = st.number_input("Turbidity (NTU)", min_value=0.0, value=0.0)
        with c2:
            dissolved_oxygen = st.number_input("Dissolved Oxygen (mg/L)", min_value=0.0, value=0.0)
            nitrate = st.number_input("Nitrate Level (mg/L)", min_value=0.0, value=0.0)
            lead = st.number_input("Lead Concentration (µg/L)", min_value=0.0, value=0.0)
        with c3:
            bacteria = st.number_input("Bacteria Count (CFU/mL)", min_value=0.0, value=0.0)
            treatment = st.selectbox("Water Treatment Method", list(label_encoders["Water Treatment Method"].classes_))
            clean_water = st.number_input("Access to Clean Water (%)", min_value=0.0, max_value=100.0, value=50.0)

        st.divider()
        st.subheader("🏥 Disease & Socioeconomic Indicators")
        c1, c2, c3 = st.columns(3)
        with c1:
            cholera = st.number_input("Cholera Cases / 100,000", min_value=0.0, value=0.0)
            typhoid = st.number_input("Typhoid Cases / 100,000", min_value=0.0, value=0.0)
            infant_mortality = st.number_input("Infant Mortality Rate / 1,000", min_value=0.0, value=0.0)
            gdp = st.number_input("GDP per Capita (USD)", min_value=0.0, value=1000.0)
        with c2:
            healthcare = st.number_input("Healthcare Access Index (0-100)", min_value=0.0, max_value=100.0, value=50.0)
            urbanization = st.number_input("Urbanization Rate (%)", min_value=0.0, max_value=100.0, value=50.0)
            sanitation = st.number_input("Sanitation Coverage (%)", min_value=0.0, max_value=100.0, value=50.0)
        with c3:
            rainfall = st.number_input("Rainfall (mm/year)", min_value=0.0, value=1000.0)
            temperature = st.number_input("Temperature (°C)", value=25.0)
            population_density = st.number_input("Population Density (people/km²)", min_value=0.0, value=100.0)

        submitted = st.form_submit_button("🔍 Generate Prediction", use_container_width=True)

    if submitted:
        raw = {
            "Country": country,
            "Region": region,
            "Year": year,
            "Water Source Type": water_source,
            "Contaminant Level (ppm)": contaminant,
            "pH Level": ph,
            "Turbidity (NTU)": turbidity,
            "Dissolved Oxygen (mg/L)": dissolved_oxygen,
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
        }

        try:
            for col in ["Country", "Region", "Water Source Type", "Water Treatment Method"]:
                raw[col] = label_encoders[col].transform([raw[col]])[0]

            input_df = pd.DataFrame([raw])
            input_df = input_df[feature_names]

            prediction = model.predict(input_df)[0]

            st.markdown("### Prediction Result")
            st.markdown(
                f"""
                <div class="result-card">
                    <h2>🎯 Predicted Class: {prediction}</h2>
                    <p>The result was generated using the deployed machine-learning classification model.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.caption("This output is for project/demo purposes and is not medical advice.")

        except Exception as e:
            st.error(f"Prediction failed: {e}")
            st.info(
                "Check that the deployed preprocessing matches model training. "
                "If X_train_clf was scaled before fitting the final model, the fitted scaler must also be saved and applied here."
            )


# -------------------- MODEL INFO --------------------
elif page == "📊 Model Information":
    st.title("📊 Model Information")
    st.write("This page summarizes the deployment configuration currently loaded by the application.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Input Features", len(feature_names))
    c2.metric("Categorical Features", 4)
    c3.metric("Deployment", "Streamlit")

    st.subheader("Categorical Variables")
    st.write("Country, Region, Water Source Type, and Water Treatment Method are transformed using the saved LabelEncoder objects.")

    st.subheader("Feature Order")
    feature_df = pd.DataFrame({
        "No.": range(1, len(feature_names) + 1),
        "Feature": feature_names
    })
    st.dataframe(feature_df, use_container_width=True, hide_index=True)

    st.subheader("Model")
    st.code(type(model).__name__)


# -------------------- ABOUT --------------------
else:
    st.title("ℹ️ About the Project")
    st.write(
        "The Water Pollution & Disease Prediction project explores how water-quality measurements, "
        "environmental conditions, disease prevalence, sanitation, healthcare access and socioeconomic "
        "factors can be used in a machine-learning classification workflow."
    )

    st.subheader("Project Objective")
    st.write(
        "The objective is to demonstrate an end-to-end data science workflow—from data preparation and "
        "categorical encoding to model training, evaluation, hyperparameter optimization and web deployment."
    )

    st.subheader("Technology Stack")
    st.write("🐍 Python  •  🐼 Pandas  •  🤖 Scikit-learn  •  📦 Joblib  •  ⚡ Streamlit  •  🐙 GitHub")

    st.subheader("Core Capabilities")
    a, b, c = st.columns(3)
    a.info("💧 Water-quality analytics")
    b.info("🧠 ML classification")
    c.info("🌍 Environmental context")

    st.warning(
        "Important: Predictions from this educational ML application are not medical diagnoses and should "
        "not be used for clinical or public-health decision-making without appropriate expert validation."
    )


st.markdown(
    '<div class="footer">💧 AquaGuard AI • Water Pollution & Disease Prediction • Machine Learning Project</div>',
    unsafe_allow_html=True
)
