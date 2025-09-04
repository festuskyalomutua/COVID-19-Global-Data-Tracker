pip install streamlit pandas plotly

# app.py
# 🌍 COVID-19 Global Data Tracker - Streamlit App

import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------
# 1. Page Setup
# -----------------------------------------
st.set_page_config(
    page_title="COVID-19 Global Data Tracker",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 COVID-19 Global Data Tracker")
st.markdown("An interactive dashboard to explore COVID-19 cases, deaths, and vaccinations globally.")

# -----------------------------------------
# 2. Load Dataset
# -----------------------------------------
@st.cache_data
def load_data():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# -----------------------------------------
# 3. Sidebar Controls
# -----------------------------------------
st.sidebar.header("🔎 Filter Data")

# Country selection
countries = df['location'].dropna().unique()
selected_countries = st.sidebar.multiselect(
    "Select countries:",
    options=sorted(countries),
    default=["Kenya", "United States", "India"]
)

# Metric selection
metric = st.sidebar.selectbox(
    "Select metric:",
    ["total_cases", "total_deaths", "people_fully_vaccinated"]
)

# Date selection
min_date = df["date"].min()
max_date = df["date"].max()
date_range = st.sidebar.slider(
    "Select date range:",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# Filter dataset
mask = (df["date"].between(date_range[0], date_range[1])) & (df["location"].isin(selected_countries))
filtered_df = df.loc[mask]

# -----------------------------------------
# 4. Line Chart
# -----------------------------------------
st.subheader(f"📈 {metric.replace('_', ' ').title()} Over Time")
fig_line = px.line(
    filtered_df,
    x="date",
    y=metric,
    color="location",
    title=f"{metric.replace('_', ' ').title()} Over Time"
)
st.plotly_chart(fig_line, use_container_width=True)

# -----------------------------------------
# 5. Choropleth Map (Latest Date)
# -----------------------------------------
st.subheader(f"🌍 Global {metric.replace('_', ' ').title()} (Latest Available Date)")
latest_date = filtered_df["date"].max()
latest_data = df[df["date"] == latest_date]

fig_map = px.choropleth(
    latest_data,
    locations="iso_code",
    color=metric,
    hover_name="location",
    color_continuous_scale="Viridis",
    title=f"Global {metric.replace('_', ' ').title()} on {latest_date.date()}"
)
st.plotly_chart(fig_map, use_container_width=True)

# -----------------------------------------
# 6. Insights Section
# -----------------------------------------
st.subheader("📝 Key Insights")
st.markdown("""
- Countries with higher vaccination rates generally show slower growth in cases.  
- Regional disparities in vaccine access significantly impacted case outcomes.  
- Choropleth maps highlight both **global spread** and **vaccination gaps**.  
""")
