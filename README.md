# 🏠 Tunisia Real Estate MLOps Platform

[https://real-estate-mlops-tunisia-jmbw4ismca5q6krcev8wy7.streamlit.app](https://real-estate-mlops-tunisia-jmbw4ismca5q6krcev8wy7.streamlit.app)


An end-to-end MLOps architecture for web scraping, data engineering, automated modeling, geospatial visualization, and real-time price predictions across major Tunisian regions.

🚀 **Live Interactive Dashboard:** [Tunisia Real Estate App](https://real-estate-mlops-tunisia-jmbw4ismca5q6krcev8wy7.streamlit.app)

---

## 🛠️ System Architecture

1. **Data Pipeline & Cleaning:** Automated Python scripts to fetch, parse, and normalize real estate listings (`scraper/clean_data.py`).
2. **Database Layer:** Structured SQLite database storage storing cleaned property attributes (`database/real_estate.db`).
3. **Machine Learning Model:** Trained regression pipeline predicting home values based on surface area, room configuration, and geographic coordinates (`models/train_model.py`).
4. **Cloud Interactive Dashboard:** Streamlit application featuring live location-based predictions and dynamic geospatial Folium mapping (`dashboard/app.py`).
5. **REST API Endpoint:** FastAPI web server exposing prediction endpoints for programmatic integration (`api/main.py`).

---

## ⚡ Quick Start (Local Setup)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
