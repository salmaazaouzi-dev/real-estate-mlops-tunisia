import streamlit as st
import pandas as pd
import sqlite3
import joblib
import folium
from streamlit_folium import st_folium
import os

# 1. Page Configuration
st.set_page_config(
    page_title="Tunisia Real Estate Insights",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Tunisia Real Estate Market Analysis & Price Predictor")
st.markdown("End-to-End MLOps Platform for Tunisian Real Estate Analytics")

# 2. Path Resolution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "real_estate.db")
MODEL_PATH = os.path.join(BASE_DIR, "models", "real_estate_model.pkl")

# 3. Load Model and Data
@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

@st.cache_data
def load_data():
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM tunisia_real_estate", conn)
        conn.close()
        return df
    return pd.DataFrame()

model = load_model()
df = load_data()

# 4. Display KPIs
if not df.empty:
    st.success(f"Database Loaded Successfully! Total Listings: {len(df)}")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Listings", f"{len(df)}")
    col2.metric("Avg Price", f"{df['price_tnd'].mean():,.0f} TND")
    col3.metric("Avg Surface", f"{df['surface_m2'].mean():.0f} m²")
    col4.metric("Avg Price / m²", f"{df['price_per_m2'].mean():,.0f} TND")

st.divider()

# 5. Sidebar Predictor
st.sidebar.header("🔮 Price Predictor")

city_coords = {
    "La Marsa": (36.8782, 10.3247),
    "Ariana": (36.8665, 10.1930),
    "Tunis": (36.8065, 10.1815),
    "Sousse": (35.8256, 10.6411),
    "Hammamet": (36.4000, 10.6167),
    "Sfax": (34.7406, 10.7603),
    "Nabeul": (36.4561, 10.7376),
    "Bizerte": (37.2744, 9.8739),
    "Monastir": (35.7833, 10.8333),
}

selected_city = st.sidebar.selectbox("Select Location", list(city_coords.keys()))
surface_input = st.sidebar.number_input("Surface Area (m²)", min_value=20, max_value=500, value=120)
rooms_input = st.sidebar.slider("Number of Rooms (S+X)", min_value=1, max_value=6, value=3)

if st.sidebar.button("Predict Estimated Price"):
    if model:
        lat, lon = city_coords[selected_city]
        pred = model.predict([[surface_input, rooms_input, lat, lon]])[0]
        st.sidebar.success(f"Estimated Price: **{pred:,.2f} TND**")
    else:
        st.sidebar.error("Model file not found!")

# 6. Dashboard Tabs (Map & Data)
tab1, tab2 = st.tabs(["🗺️ Geospatial Map", "📊 Market Data Explorer"])

with tab1:
    st.subheader("Geospatial Distribution of Real Estate Listings in Tunisia")
    if not df.empty:
        # Create Folium Map centered on Tunisia
        m = folium.Map(location=[36.8065, 10.1815], zoom_start=8)
        
        # Add clean Markers for all listings
        for _, row in df.iterrows():
            popup_text = f"<b>{row['title']}</b><br>Prix: {row['price_tnd']:,.0f} TND<br>Surface: {row['surface_m2']} m²"
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=popup_text,
                tooltip=f"{row['price_tnd']:,.0f} TND",
                icon=folium.Icon(color="blue", icon="info-sign")  # Clean standard icon
            ).add_to(m)
            
        st_folium(m, width=1100, height=500)
with tab2:
    st.subheader("Processed Real Estate Dataset")
    st.dataframe(df, use_container_width=True)