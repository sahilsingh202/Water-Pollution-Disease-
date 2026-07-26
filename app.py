"""
Water Pollution & Disease Risk Prediction App
A Streamlit-based ML application for predicting diarrheal disease risk
based on water quality and environmental parameters.
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Water Pollution & Disease Predictor",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS FOR WATER POLLUTION THEME
# ============================================================================
st.markdown("""
<style>
    /* Main theme colors - water and disease related */
    :root {
        --water-blue: #0077be;
        --deep-blue: #004e89;
        --polluted: #d62828;
        --warning: #f77f00;
        --safe: #06a77d;
        --light-bg: #f0f8ff;
    }
    
    /* Main container styling */
    .main {
        background-color: #f0f8ff;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #e8f4f8;
        border-right: 3px solid #0077be;
    }
    
    /* Metric card styling */
    .metric-card {
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #0077be;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    /* Header styling */
    .header-main {
        background: linear-gradient(135deg, #0077be 0%, #004e89 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    
    /* Prediction box styling */
    .prediction-box-safe {
        background: linear-gradient(135deg, #06a77d 0%, #0d7a5f 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        border: 3px solid #06a77d;
        box-shadow: 0 4px 8px rgba(6, 168, 125, 0.3);
    }
    
    .prediction-box-warning {
        background: linear-gradient(135deg, #f77f00 0%, #d66a2a 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        border: 3px solid #f77f00;
        box-shadow: 0 4px 8px rgba(247, 127, 0, 0.3);
    }
    
    .prediction-box-danger {
        background: linear-gradient(135deg, #d62828 0%, #a02020 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        border: 3px solid #d62828;
        box-shadow: 0 4px 8px rgba(214, 40, 40, 0.3);
    }
    
    /* Info box */
    .info-box {
        background-color: #e3f2fd;
        border-left: 4px solid #2196F3;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    /* Feature importance styling */
    .feature-importance {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 15px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD DATA AND MODEL
# ============================================================================
@st.cache_resource
def load_data():
    """Load the water pollution dataset"""
    try:
        df = pd.read_csv('water_pollution_disease.csv')
        return df
    except FileNotFoundError:
        st.error("Dataset not found. Please ensure 'water_pollution_disease.csv' is in the app directory.")
        return None

@st.cache_resource
def train_model(df):
    """Train the ML model using the best performing algorithm"""
    if df is None:
        return None, None, None
    
    # Prepare data for classification
    X = df[['Contaminant_Level', 'pH_Level', 'Dissolved_Oxygen', 'Population_Density']]
    
    # Create disease risk categories
    y = pd.qcut(df['Diarrhea_Cases'], q=3, labels=['Low Risk', 'Medium Risk', 'High Risk'])
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train best model (KNN as per notebook)
    best_model = KNeighborsClassifier(n_neighbors=5, weights='distance', metric='euclidean')
    best_model.fit(X_scaled, y)
    
    return best_model, scaler, y

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def get_risk_color(risk_level):
    """Return color based on risk level"""
    colors = {
        'Low Risk': '#06a77d',
        'Medium Risk': '#f77f00',
        'High Risk': '#d62828'
    }
    return colors.get(risk_level, '#0077be')

def get_risk_emoji(risk_level):
    """Return emoji based on risk level"""
    emojis = {
        'Low Risk': '✅',
        'Medium Risk': '⚠️',
        'High Risk': '🚨'
    }
    return emojis.get(risk_level, '❓')

def create_prediction_box(risk_level, confidence):
    """Create styled prediction box"""
    emoji = get_risk_emoji(risk_level)
    color = get_risk_color(risk_level)
    
    if risk_level == 'Low Risk':
        box_class = 'prediction-box-safe'
    elif risk_level == 'Medium Risk':
        box_class = 'prediction-box-warning'
    else:
        box_class = 'prediction-box-danger'
    
    html_content = f"""
    <div class="{box_class}">
        <h2 style="margin: 0; font-size: 2.5em;">{emoji} {risk_level}</h2>
        <p style="margin: 10px 0 0 0; font-size: 1.2em;">Confidence: {confidence:.1%}</p>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

def get_recommendations(risk_level, contaminant_level, ph_level):
    """Get health recommendations based on risk level"""
    recommendations = {
        'Low Risk': [
            '✓ Water quality is acceptable',
            '✓ Continue regular water monitoring',
            '✓ Maintain good hygiene practices',
            '✓ Safe for consumption with standard precautions'
        ],
        'Medium Risk': [
            '⚠ Water quality requires attention',
            '⚠ Increase monitoring frequency',
            '⚠ Use water purification methods',
            '⚠ Educate community about water safety',
            '⚠ Consider boiling water before consumption'
        ],
        'High Risk': [
            '🚨 Urgent water quality intervention needed',
            '🚨 Implement emergency water treatment',
            '🚨 Provide safe drinking water alternatives',
            '🚨 Launch public health awareness campaign',
            '🚨 Do NOT consume water without treatment'
        ]
    }
    return recommendations.get(risk_level, [])

# ============================================================================
# MAIN APPLICATION
# ============================================================================
def main():
    # Load data and train model
    df = load_data()
    
    # Header
    st.markdown("""
    <div class="header-main">
        <h1>🌊 Water Pollution & Disease Risk Predictor</h1>
        <p>Advanced ML-Based Risk Assessment for Water Quality & Public Health</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    page = st.sidebar.radio(
        "📊 Navigation Menu",
        ["🏠 Home", "🔮 Prediction", "📈 Analytics", "📋 Dataset Info"],
        key="nav_radio"
    )
    
    if page == "🏠 Home":
        show_home_page(df)
    elif page == "🔮 Prediction":
        show_prediction_page(df)
    elif page == "📈 Analytics":
        show_analytics_page(df)
    elif page == "📋 Dataset Info":
        show_dataset_info_page(df)

def show_home_page(df):
    """Home page with project overview"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### About This Project
        
        This intelligent system analyzes water pollution levels and environmental factors
        to predict the risk of diarrheal disease transmission in communities.
        
        #### 🎯 Key Features:
        - **Real-time Risk Assessment**: Predict disease risk based on water quality parameters
        - **Multi-Model Analysis**: Compares 5+ machine learning algorithms
        - **Comprehensive Analytics**: Visualize water quality trends and disease patterns
        - **Actionable Insights**: Get recommendations based on risk levels
        
        #### 📊 Variables Analyzed:
        - **Contaminant Level**: Concentration of pollutants in water (mg/L)
        - **pH Level**: Acidity/alkalinity of water (0-14 scale)
        - **Dissolved Oxygen**: Available oxygen in water (mg/L)
        - **Population Density**: People per unit area
        - **Diarrhea Cases**: Target variable for prediction
        """)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>📈 Dataset Overview</h4>
            <p><strong>Total Records:</strong> {}</p>
            <p><strong>Features:</strong> 5</p>
            <p><strong>Target:</strong> Diarrhea Cases</p>
            <p><strong>Model Type:</strong> Classification</p>
        </div>
        """.format(len(df) if df is not None else "N/A"), unsafe_allow_html=True)
    
    # Risk Level Guide
    st.markdown("---")
    st.subheader("📋 Risk Level Classification Guide")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="prediction-box-safe">
            <h3>✅ Low Risk</h3>
            <p>Water quality is good. Minimal disease risk.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="prediction-box-warning">
            <h3>⚠️ Medium Risk</h3>
            <p>Water quality needs monitoring. Take precautions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="prediction-box-danger">
            <h3>🚨 High Risk</h3>
            <p>Urgent action needed. Significant disease risk.</p>
        </div>
        """, unsafe_allow_html=True)

def show_prediction_page(df):
    """Prediction page with sidebar inputs"""
    st.subheader("🔮 Disease Risk Prediction")
    
    # Load model
    model, scaler, y_train = train_model(df)
    
    if model is None:
        st.error("Could not load model. Please check the dataset.")
        return
    
    # Sidebar inputs
    st.sidebar.markdown("### ⚙️ Input Parameters")
    st.sidebar.markdown("---")
    
    # Get feature ranges for sliders
    contaminant_range = (
        df['Contaminant_Level'].min(),
        df['Contaminant_Level'].max()
    )
    ph_range = (df['pH_Level'].min(), df['pH_Level'].max())
    oxygen_range = (
        df['Dissolved_Oxygen'].min(),
        df['Dissolved_Oxygen'].max()
    )
    density_range = (
        df['Population_Density'].min(),
        df['Population_Density'].max()
    )
    
    # Input sliders with water theme
    contaminant = st.sidebar.slider(
        "💧 Contaminant Level (mg/L)",
        float(contaminant_range[0]),
        float(contaminant_range[1]),
        float(contaminant_range[0] + (contaminant_range[1] - contaminant_range[0]) / 2),
        help="Higher values indicate more water pollution"
    )
    
    ph = st.sidebar.slider(
        "🧪 pH Level",
        float(ph_range[0]),
        float(ph_range[1]),
        7.0,
        help="7 = neutral, <7 = acidic, >7 = alkaline"
    )
    
    oxygen = st.sidebar.slider(
        "🫁 Dissolved Oxygen (mg/L)",
        float(oxygen_range[0]),
        float(oxygen_range[1]),
        float(oxygen_range[0] + (oxygen_range[1] - oxygen_range[0]) / 2),
        help="Higher values indicate better water quality"
    )
    
    density = st.sidebar.slider(
        "👥 Population Density (per km²)",
        float(density_range[0]),
        float(density_range[1]),
        float(density_range[0] + (density_range[1] - density_range[0]) / 2),
        help="Higher density increases disease transmission risk"
    )
    
    # Predict button
    st.sidebar.markdown("---")
    if st.sidebar.button("🎯 Predict Risk Level", use_container_width=True, type="primary"):
        # Prepare input
        input_data = np.array([[contaminant, ph, oxygen, density]])
        input_scaled = scaler.transform(input_data)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        
        # Get prediction probabilities
        distances, indices = model.kneighbors(input_scaled)
        neighbors_labels = y_train.iloc[indices[0]].values
        unique, counts = np.unique(neighbors_labels, return_counts=True)
        confidence = counts.max() / len(neighbors_labels)
        
        # Display main prediction
        st.markdown("---")
        st.subheader("🎯 Prediction Results")
        
        create_prediction_box(prediction, confidence)
        
        # Display input parameters
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h4>💧 Contaminant Level</h4>
                <h3>{contaminant:.2f} mg/L</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h4>🧪 pH Level</h4>
                <h3>{ph:.2f}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h4>🫁 Dissolved Oxygen</h4>
                <h3>{oxygen:.2f} mg/L</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h4>👥 Population Density</h4>
                <h3>{density:.2f}/km²</h3>
            </div>
            """, unsafe_allow_html=True)
        
        # Health Recommendations
        st.markdown("---")
        st.subheader("💡 Health Recommendations")
        
        recommendations = get_recommendations(prediction, contaminant, ph)
        
        for rec in recommendations:
            st.write(rec)
        
        # Risk analysis
        st.markdown("---")
        st.subheader("📊 Risk Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=confidence * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Model Confidence"},
                delta={'reference': 80},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': get_risk_color(prediction)},
                    'steps': [
                        {'range': [0, 33], 'color': "#e8f4f8"},
                        {'range': [33, 66], 'color': "#c5e1e8"},
                        {'range': [66, 100], 'color': "#a3ccdb"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Risk factors visualization
            risk_factors = pd.DataFrame({
                'Factor': ['Contaminant', 'pH', 'Oxygen', 'Density'],
                'Normalized Value': [
                    (contaminant - contaminant_range[0]) / (contaminant_range[1] - contaminant_range[0]),
                    abs(ph - 7) / 7,  # Distance from neutral
                    (oxygen_range[1] - oxygen) / (oxygen_range[1] - oxygen_range[0]),
                    (density - density_range[0]) / (density_range[1] - density_range[0])
                ]
            })
            
            fig = px.bar(
                risk_factors,
                x='Factor',
                y='Normalized Value',
                color='Normalized Value',
                color_continuous_scale=['#06a77d', '#f77f00', '#d62828'],
                title="Risk Contribution by Factor",
                labels={'Normalized Value': 'Risk Contribution (0-1)'}
            )
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

def show_analytics_page(df):
    """Analytics page with visualizations"""
    if df is None:
        st.error("Dataset not available.")
        return
    
    st.subheader("📈 Water Quality & Disease Analytics")
    
    # Tabs for different analytics
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Distribution", 
        "🔗 Correlations", 
        "📈 Trends",
        "🎯 Model Performance"
    ])
    
    with tab1:
        st.markdown("### Feature Distributions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.histogram(
                df,
                x='Contaminant_Level',
                nbins=30,
                title='Contaminant Level Distribution',
                color_discrete_sequence=['#0077be']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.histogram(
                df,
                x='pH_Level',
                nbins=30,
                title='pH Level Distribution',
                color_discrete_sequence=['#0077be']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.histogram(
                df,
                x='Dissolved_Oxygen',
                nbins=30,
                title='Dissolved Oxygen Distribution',
                color_discrete_sequence=['#0077be']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.histogram(
                df,
                x='Population_Density',
                nbins=30,
                title='Population Density Distribution',
                color_discrete_sequence=['#0077be']
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Correlation Analysis")
        
        # Correlation heatmap
        corr_matrix = df[['Contaminant_Level', 'pH_Level', 'Dissolved_Oxygen', 
                          'Population_Density', 'Diarrhea_Cases']].corr()
        
        fig = px.imshow(
            corr_matrix,
            labels=dict(x="Features", y="Features", color="Correlation"),
            x=['Contaminant', 'pH', 'Oxygen', 'Density', 'Disease'],
            y=['Contaminant', 'pH', 'Oxygen', 'Density', 'Disease'],
            color_continuous_scale='RdBu',
            zmin=-1, zmax=1,
            title='Feature Correlation Matrix'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Relationship Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.scatter(
                df,
                x='Contaminant_Level',
                y='Diarrhea_Cases',
                trendline='ols',
                title='Contaminant Level vs Disease Cases',
                labels={'Diarrhea_Cases': 'Disease Cases', 'Contaminant_Level': 'Contaminant (mg/L)'},
                color_discrete_sequence=['#d62828']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(
                df,
                x='Dissolved_Oxygen',
                y='Diarrhea_Cases',
                trendline='ols',
                title='Dissolved Oxygen vs Disease Cases',
                labels={'Diarrhea_Cases': 'Disease Cases', 'Dissolved_Oxygen': 'Oxygen (mg/L)'},
                color_discrete_sequence=['#06a77d']
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### ML Model Comparison")
        
        # Train multiple models for comparison
        X = df[['Contaminant_Level', 'pH_Level', 'Dissolved_Oxygen', 'Population_Density']]
        y = pd.qcut(df['Diarrhea_Cases'], q=3, labels=['Low Risk', 'Medium Risk', 'High Risk'])
        
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        models = {
            'KNN': KNeighborsClassifier(n_neighbors=5),
            'Decision Tree': DecisionTreeClassifier(),
            'Logistic Regression': LogisticRegression(max_iter=1000),
            'Gaussian NB': GaussianNB(),
            'Linear SVC': LinearSVC(max_iter=2000)
        }
        
        results = []
        for name, model in models.items():
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            
            results.append({
                'Model': name,
                'Accuracy': accuracy_score(y_test, y_pred),
                'Precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
                'Recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
                'F1 Score': f1_score(y_test, y_pred, average='weighted', zero_division=0)
            })
        
        results_df = pd.DataFrame(results).sort_values('Accuracy', ascending=False)
        
        fig = px.bar(
            results_df.melt(id_vars='Model', var_name='Metric', value_name='Score'),
            x='Model',
            y='Score',
            color='Metric',
            barmode='group',
            title='Model Performance Comparison',
            labels={'Score': 'Score', 'Model': 'Machine Learning Model'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(results_df, use_container_width=True)

def show_dataset_info_page(df):
    """Dataset information page"""
    if df is None:
        st.error("Dataset not available.")
        return
    
    st.subheader("📋 Dataset Information")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Total Records", value=len(df))
    
    with col2:
        st.metric(label="Total Features", value=len(df.columns))
    
    with col3:
        st.metric(label="Missing Values", value=df.isnull().sum().sum())
    
    with col4:
        st.metric(label="Duplicate Rows", value=df.duplicated().sum())
    
    # Dataset statistics
    st.markdown("---")
    st.subheader("📊 Statistical Summary")
    
    st.dataframe(df.describe(), use_container_width=True)
    
    # Data types
    st.markdown("---")
    st.subheader("🔍 Data Types")
    
    dtype_info = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes.values,
        'Non-Null Count': df.count().values,
        'Null Count': df.isnull().sum().values
    })
    
    st.dataframe(dtype_info, use_container_width=True)
    
    # First few rows
    st.markdown("---")
    st.subheader("👀 Dataset Preview")
    
    st.dataframe(df.head(10), use_container_width=True)

if __name__ == "__main__":
    main()
