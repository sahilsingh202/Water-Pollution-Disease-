# 🌊 Water Pollution & Disease Risk Prediction App

An intelligent machine learning-based web application built with Streamlit to predict the risk of diarrheal disease transmission based on water quality and environmental parameters.

## 📋 Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Dataset](#dataset)
- [Model Information](#model-information)
- [UI/UX Features](#uiux-features)
- [Contributing](#contributing)

## 🎯 Features

### 🔮 **Prediction Module**
- Real-time disease risk assessment based on water quality parameters
- 5-parameter input system with intuitive sidebar controls
- Multiple risk categories: Low, Medium, High
- Confidence score visualization with gauge charts
- Risk contribution analysis by factor

### 📈 **Analytics Dashboard**
- **Distribution Analysis**: Visualize feature distributions
- **Correlation Matrix**: Understand relationships between variables
- **Trend Analysis**: Scatter plots with trendlines
- **Model Comparison**: Compare 5 different ML algorithms
- Performance metrics for all trained models

### 📊 **Dataset Explorer**
- Complete dataset statistics and summary
- Data type information and null value detection
- Dataset preview with interactive dataframe
- Quality metrics at a glance

### 💡 **Smart Recommendations**
- Context-aware health recommendations based on risk level
- Actionable insights for water quality management
- Disease prevention strategies

## 📁 Project Structure

```
water-pollution-app/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── setup_instructions.md           # Detailed setup guide
│
├── data/
│   └── water_pollution_disease.csv # Dataset (required)
│
└── assets/
    ├── screenshots/                # UI screenshots
    └── documentation/              # Additional docs
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### Step-by-Step Setup

#### 1. **Clone the Repository** (or extract files)
```bash
cd water-pollution-app
```

#### 2. **Create a Virtual Environment** (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

#### 4. **Prepare the Dataset**
- Place `water_pollution_disease.csv` in the project root directory
- The dataset should contain these columns:
  - `Contaminant_Level`
  - `pH_Level`
  - `Dissolved_Oxygen`
  - `Population_Density`
  - `Diarrhea_Cases`

#### 5. **Run the Application**
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## 📖 Usage Guide

### 🏠 **Home Page**
- Project overview and objectives
- Risk level classification guide
- Key features and variables explained

### 🔮 **Prediction Page**
1. **Set Parameters in Sidebar**:
   - Move sliders to adjust water quality parameters
   - See real-time ranges based on dataset

2. **Click "Predict Risk Level" Button**:
   - Model processes inputs
   - Displays risk classification with confidence

3. **Review Results**:
   - See prediction box with color-coded risk level
   - View input parameters in metric cards
   - Read health recommendations

4. **Analyze Risk Factors**:
   - Check confidence gauge
   - View risk contribution by each factor

### 📈 **Analytics Page**
- **Distribution Tab**: Explore feature distributions
- **Correlations Tab**: View correlation heatmap
- **Trends Tab**: Analyze relationships between variables
- **Model Performance Tab**: Compare ML model accuracy

### 📋 **Dataset Info Page**
- View comprehensive dataset statistics
- Check data quality metrics
- Preview dataset sample

## 📊 Dataset

### Required Columns:
| Column | Type | Description |
|--------|------|-------------|
| `Contaminant_Level` | Float | Concentration of pollutants (mg/L) |
| `pH_Level` | Float | Water acidity/alkalinity (0-14 scale) |
| `Dissolved_Oxygen` | Float | Available oxygen in water (mg/L) |
| `Population_Density` | Float | People per unit area (per km²) |
| `Diarrhea_Cases` | Integer | Number of reported disease cases |

### Data Format:
- CSV file with headers
- No missing values (required)
- Numeric values only

## 🤖 Model Information

### Algorithm: K-Nearest Neighbors (KNN)
**Reason for Selection**: Best performance among tested models

**Hyperparameters**:
- `n_neighbors`: 5
- `weights`: 'distance'
- `metric`: 'euclidean'

### Performance Metrics:
- **Accuracy**: High accuracy on test data
- **Precision**: Reliable positive predictions
- **Recall**: Good disease case detection
- **F1 Score**: Balanced performance

### Alternative Models Included:
1. **Decision Tree Classifier**: Interpretable rules
2. **Logistic Regression**: Linear relationships
3. **Gaussian Naive Bayes**: Probabilistic approach
4. **Linear SVC**: Support Vector Classification

### Feature Preprocessing:
- StandardScaler normalization
- 80-20 train-test split
- Cross-validation included

## 🎨 UI/UX Features

### Design Theme: Water & Health Focused
- **Color Palette**:
  - Deep Blue (#0077BE, #004E89): Water theme
  - Green (#06A77D): Safe/healthy indicators
  - Orange (#F77F00): Warning/caution indicators
  - Red (#D62828): Danger/high-risk indicators

### Interactive Components:
- **Sidebar Navigation**: Easy page switching
- **Slider Inputs**: Smooth parameter adjustment
- **Metric Cards**: Visual data presentation
- **Gauge Charts**: Confidence visualization
- **Color-Coded Boxes**: Instant risk assessment
- **Responsive Layout**: Works on desktop & mobile

### Accessibility:
- Clear emoji indicators for quick understanding
- High contrast colors for visibility
- Descriptive tooltips on all inputs
- Large, readable typography

## 📱 Browser Compatibility
- Chrome/Chromium (Recommended)
- Firefox
- Safari
- Edge

## ⚙️ Configuration

### Streamlit Config (optional)
Create `~/.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#0077be"
backgroundColor = "#f0f8ff"
secondaryBackgroundColor = "#e8f4f8"
textColor = "#333333"

[client]
showErrorDetails = true
```

## 🔧 Troubleshooting

### Issue: "Dataset not found"
**Solution**: Ensure `water_pollution_disease.csv` is in the project root

### Issue: Slow predictions
**Solution**: Dataset size is manageable; check system resources

### Issue: Port already in use
**Solution**: 
```bash
streamlit run app.py --server.port 8502
```

### Issue: Module import errors
**Solution**: Verify requirements installation
```bash
pip install -r requirements.txt --upgrade
```

## 📈 Deployment Options

### Local Deployment
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Push code to GitHub
2. Visit https://share.streamlit.io
3. Deploy directly from repository

### Docker Deployment
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]
```

## 📚 Educational Value

This project demonstrates:
- **Data Analysis**: EDA techniques
- **Machine Learning**: Multiple algorithms comparison
- **Web Development**: Streamlit framework
- **UI/UX Design**: User-centered interface
- **Data Visualization**: Plotly & Matplotlib
- **Python Best Practices**: Clean, documented code

## 🎓 Learning Outcomes

Students working with this project will learn:
- How to build production-ready ML applications
- Streamlit framework for rapid prototyping
- Data preprocessing and normalization
- Model selection and evaluation
- Interactive data visualization
- Professional code structure and documentation

## 📝 License

This project is part of an academic capstone and is provided for educational purposes.

## 👨‍💼 Author

**Sahil Kumar**  
Branch: CSE  
Enrollment No: 90320802725

## 🤝 Support

For issues, questions, or suggestions:
1. Check the troubleshooting section
2. Review code comments for implementation details
3. Consult the dataset documentation

## 🔗 References

- [Streamlit Documentation](https://docs.streamlit.io)
- [Scikit-learn Guide](https://scikit-learn.org/stable/)
- [Plotly Charts](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/)

---

**Happy Predicting! 🌊✨**
