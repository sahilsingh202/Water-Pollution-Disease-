# 🚀 Quick Reference Card

## Installation (2 minutes)
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Dataset Setup
- Place `water_pollution_disease.csv` in project root
- Columns: Contaminant_Level, pH_Level, Dissolved_Oxygen, Population_Density, Diarrhea_Cases
- Run `python validate_data.py` to check

## App Structure
```
🏠 Home          → Project overview & risk guide
🔮 Prediction    → Enter parameters, get risk prediction
📈 Analytics     → Visualize data & model comparison
📋 Dataset Info  → Dataset statistics & preview
```

## Navigation
- Use **sidebar radio buttons** to switch between pages
- Use **sliders** in sidebar to adjust prediction parameters
- Click **"Predict Risk Level"** button to make prediction

## Input Parameters (Sidebar)
1. **💧 Contaminant Level** (mg/L): 0-100+
2. **🧪 pH Level**: 0-14 scale
3. **🫁 Dissolved Oxygen** (mg/L): 0-15
4. **👥 Population Density** (per km²): 100-5000+

## Risk Levels
- **✅ Low Risk** (Green): Safe water, minimal disease risk
- **⚠️ Medium Risk** (Orange): Water needs monitoring
- **🚨 High Risk** (Red): Urgent intervention needed

## Files Included

| File | Purpose |
|------|---------|
| `app.py` | Main application |
| `requirements.txt` | Dependencies |
| `validate_data.py` | Data validation |
| `README.md` | Full documentation |
| `SETUP_INSTRUCTIONS.md` | Detailed setup |
| `PROJECT_SUMMARY.md` | Project overview |
| `.streamlit_config.toml` | Theme config |

## Common Commands

**Start app**
```bash
streamlit run app.py
```

**Validate data**
```bash
python validate_data.py
```

**Auto-fix dataset**
```bash
python validate_data.py --fix
```

**Custom port**
```bash
streamlit run app.py --server.port 8502
```

**Clear cache**
```bash
streamlit cache clear
```

## Machine Learning Models

| Model | Type | Best Use |
|-------|------|----------|
| KNN | Distance-based | Primary (selected) |
| Decision Tree | Rule-based | Interpretability |
| Logistic Regression | Linear | Baseline |
| Gaussian NB | Probabilistic | Fast |
| Linear SVC | Boundary-based | Performance |

## Troubleshooting

**Dataset not found**
- Ensure file is in project root
- Run `python validate_data.py`

**Port already in use**
- Use `streamlit run app.py --server.port 8502`

**Module errors**
- Run `pip install -r requirements.txt --upgrade`

**Slow app**
- Add `@st.cache_resource` to load_data()
- Reduce dataset size for testing

## Features at a Glance

✅ Real-time risk prediction  
✅ 5 ML algorithm comparison  
✅ Interactive data visualizations  
✅ Smart health recommendations  
✅ Professional water-themed UI  
✅ Complete dataset analytics  
✅ Production-ready code  
✅ Comprehensive documentation  

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `R` | Rerun app |
| `C` | Clear cache |
| `H` | Hide menu |

## Performance Tips

- Keep dataset under 100k rows
- Use caching for large datasets
- Cache ML model after training
- Close other apps for faster performance

## Customization

**Change colors in app.py (lines 50-62)**
```python
--water-blue: #0077be;  # Primary color
--safe: #06a77d;        # Safe indicator
--warning: #f77f00;     # Warning indicator
--polluted: #d62828;    # Danger indicator
```

**Modify risk thresholds in function get_recommendations()**

**Add more ML models in show_analytics_page() analytics section**

## Deployment

**Streamlit Cloud**
- Push to GitHub → share.streamlit.io → Deploy

**Docker**
```bash
docker build -t water-app .
docker run -p 8501:8501 water-app
```

**Heroku**
```bash
heroku create app-name
git push heroku main
```

## Testing

Create test file and run:
```bash
python validate_data.py
streamlit run app.py
```

Then test in browser:
1. Change slider values
2. Click Predict button
3. Switch pages
4. Check Analytics tab

## API Endpoints (if deployed)
- GET `/` - Home page
- GET `/?page=Prediction` - Prediction page
- GET `/?page=Analytics` - Analytics page
- POST `/predict` - Make prediction

## Data Format Validation

```python
# In validate_data.py
columns = ['Contaminant_Level', 'pH_Level', 'Dissolved_Oxygen', 
           'Population_Density', 'Diarrhea_Cases']
dtypes = float, float, float, float, int  # Expected types
```

## Environment Variables (Optional)

Create `.env`:
```env
DATA_PATH=./data/water_pollution_disease.csv
DEBUG_MODE=false
APP_THEME=light
```

## Browser Compatibility

✅ Chrome/Chromium (Recommended)  
✅ Firefox  
✅ Safari  
✅ Edge  

## Memory Requirements

- Minimum: 2GB RAM
- Recommended: 4GB RAM
- Dataset: 500MB max

## Support

📖 **Read First**: README.md  
🔧 **Setup Help**: SETUP_INSTRUCTIONS.md  
📊 **Project Info**: PROJECT_SUMMARY.md  
🐛 **Issues**: Check troubleshooting sections  

## Next Steps

1. ✅ Install requirements: `pip install -r requirements.txt`
2. ✅ Add dataset: Place CSV in root folder
3. ✅ Validate: `python validate_data.py`
4. ✅ Run: `streamlit run app.py`
5. ✅ Explore: Navigate through all pages
6. ✅ Deploy: Choose hosting option

## Quick Health Check

```bash
# 1. Check Python version
python --version  # Should be 3.8+

# 2. Check dependencies
pip list | grep streamlit

# 3. Check dataset
python validate_data.py

# 4. Run app
streamlit run app.py

# 5. Open browser
# http://localhost:8501
```

---

**You're ready! Start predicting water pollution & disease risk! 🌊✨**
