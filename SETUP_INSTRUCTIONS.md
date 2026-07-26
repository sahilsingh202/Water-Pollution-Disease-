# 🚀 Detailed Setup & Configuration Guide

## Quick Start (5 minutes)

### 1. Install Python Packages
```bash
pip install -r requirements.txt
```

### 2. Add Your Dataset
Place `water_pollution_disease.csv` in the project root folder

### 3. Run the App
```bash
streamlit run app.py
```

Access at: **http://localhost:8501**

---

## 📦 System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python Version**: 3.8 - 3.11
- **RAM**: Minimum 2GB (4GB recommended)
- **Disk Space**: 500MB minimum

## 🔐 Virtual Environment Setup

### Windows
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### macOS/Linux
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 📥 Dataset Setup

### Expected CSV Format
```csv
Contaminant_Level,pH_Level,Dissolved_Oxygen,Population_Density,Diarrhea_Cases
45.2,7.1,6.5,1250,150
52.1,6.8,5.2,1600,210
...
```

### Dataset Validation
- No missing values
- All numeric columns
- At least 50 records recommended
- Column names must match exactly

## 🎨 Customization

### Change Color Theme
Edit the CSS in `app.py` (lines 54-110):
```python
# Change these hex codes to your colors
--water-blue: #0077be;
--deep-blue: #004e89;
--polluted: #d62828;
--warning: #f77f00;
--safe: #06a77d;
```

### Adjust Risk Categories
Modify `show_prediction_page()` function to change:
- Risk thresholds
- Recommendations text
- Risk level names

### Change Sidebar Width
Add to `.streamlit/config.toml`:
```toml
[client]
showSidebarNavigation = true

[logger]
level = "info"
```

## 🌐 Running Locally

### Standard Method
```bash
streamlit run app.py
```

### With Custom Port
```bash
streamlit run app.py --server.port 8502
```

### Headless Mode (No Browser)
```bash
streamlit run app.py --logger.level=debug --client.showErrorDetails=true
```

## ☁️ Deployment Options

### Option 1: Streamlit Cloud (Recommended)
1. Push to GitHub repository
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Choose repository, branch, main file
4. Deploy instantly!

### Option 2: Heroku Deployment
```bash
# Create Procfile
echo "web: streamlit run app.py" > Procfile

# Create setup.sh
cat > setup.sh << EOF
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = \$PORT
enableCORS = false
" > ~/.streamlit/config.toml
EOF

# Add buildpack
heroku buildpacks:add heroku/python
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-apt

# Deploy
git push heroku main
```

### Option 3: Docker
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t water-pollution-app .
docker run -p 8501:8501 water-pollution-app
```

### Option 4: PythonAnywhere
1. Upload files to PythonAnywhere
2. Create web app with Python 3.10
3. Set working directory
4. Use WSGI configuration for Streamlit

## 📊 Performance Optimization

### For Large Datasets (>10k rows)
```python
# Add to app.py
@st.cache_resource(ttl=3600)  # Cache for 1 hour
def load_data():
    return pd.read_csv('data.csv')
```

### Reduce Model Training Time
```python
# Use smaller dataset sample for testing
df_sample = df.sample(n=5000, random_state=42)
```

## 🐛 Debugging

### Enable Debug Mode
Add to beginning of `app.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Streamlit Logs
```bash
streamlit run app.py --logger.level=debug
```

### Test Individual Functions
```python
# Create test.py
from app import load_data, train_model

df = load_data()
model, scaler, y = train_model(df)
print("Model trained successfully!")
```

## 📝 Logging Configuration

Create `.streamlit/config.toml`:
```toml
[logger]
level = "info"
messageFormat = "%(asctime)s - %(message)s"

[client]
showErrorDetails = true
showSidebarNavigation = true

[server]
runOnSave = true
headless = false
enableCORS = true
```

## 🔐 Environment Variables

Create `.env` file:
```env
# Data path
DATA_PATH=./data/water_pollution_disease.csv

# Model settings
MODEL_RANDOM_STATE=42
TEST_SIZE=0.2

# App settings
APP_THEME=light
DEBUG_MODE=false
```

Load in `app.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()
DATA_PATH = os.getenv('DATA_PATH', 'water_pollution_disease.csv')
```

## 🧪 Testing

Create `test_app.py`:
```python
import unittest
import pandas as pd
import numpy as np
from app import load_data, train_model, get_risk_color

class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.df = load_data()
    
    def test_data_loaded(self):
        self.assertIsNotNone(self.df)
        self.assertGreater(len(self.df), 0)
    
    def test_risk_color(self):
        color = get_risk_color('Low Risk')
        self.assertEqual(color, '#06a77d')

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python -m pytest test_app.py
```

## 📚 File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Main application (800+ lines) |
| `requirements.txt` | Python dependencies |
| `README.md` | Project documentation |
| `SETUP_INSTRUCTIONS.md` | This file |
| `water_pollution_disease.csv` | Dataset (required) |

## 🚨 Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install streamlit --upgrade
```

### Issue: Port 8501 already in use
```bash
# Find process using port
lsof -i :8501  # macOS/Linux
netstat -ano | findstr :8501  # Windows

# Use different port
streamlit run app.py --server.port 8502
```

### Issue: Dataset encoding problems
```python
# In app.py, modify load_data():
df = pd.read_csv('water_pollution_disease.csv', encoding='utf-8')
```

### Issue: Slow app on first load
```python
# Add caching to load_data()
@st.cache_resource
def load_data():
    return pd.read_csv('water_pollution_disease.csv')
```

## 🎯 Next Steps

1. ✅ Install requirements
2. ✅ Add dataset
3. ✅ Run app locally
4. ✅ Test all features
5. ✅ Deploy to cloud
6. ✅ Share with users

## 💬 Support

- **Streamlit Docs**: https://docs.streamlit.io
- **Scikit-learn**: https://scikit-learn.org
- **Plotly**: https://plotly.com/python
- **GitHub Issues**: Create issue in repo

---

**Ready to predict? Run: `streamlit run app.py` 🚀**
