import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Page Configuration
st.set_page_config(
    page_title="EcoGrid-AI: Energy Analytics",
    page_icon="⚡",
    layout="wide"
)

# App Title & Overview
st.title("⚡ EcoGrid-AI: Energy Analytics & Carbon Emission Predictor")
st.markdown("""
A professional industrial-grade AI dashboard designed to monitor energy consumption patterns, 
forecast carbon metrics using machine learning, and provide actionable sustainability insights.
""")

---

# Sidebar: Data Source Configuration
st.sidebar.header("⚙️ Configuration Panel")
data_option = st.sidebar.radio(
    "Choose Data Source:",
    ("Default Industrial Dataset", "Upload Custom CSV File")
)

# Handle Data Loading based on user choice
if data_option == "Upload Custom CSV File":
    uploaded_file = st.sidebar.file_uploader("Upload your energy dataset (CSV)", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.sidebar.success("Custom dataset loaded successfully!")
        except Exception as e:
            st.sidebar.error(f"Error loading file: {e}")
            df = pd.read_csv('real_energy_data.csv')
    else:
        st.sidebar.warning("Awaiting custom file upload. Using default dataset temporarily.")
        df = pd.read_csv('real_energy_data.csv')
else:
    df = pd.read_csv('real_energy_data.csv')

---

# Main Dashboard Layout
st.subheader("📊 Dataset Overview & Preview")
st.dataframe(df.head(), use_container_width=True)

# Basic Data Validation & Feature Selection
# Assuming columns like 'Energy_Load' and 'Carbon_Emissions' exist, with fallbacks or standard names
if 'Energy_Load' in df.columns and 'Carbon_Emissions' in df.columns:
    feature_col = 'Energy_Load'
    target_col = 'Carbon_Emissions'
else:
    # Fallback to first two numerical columns if specific names aren't matched
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(num_cols) >= 2:
        feature_col = num_cols[0]
        target_col = num_cols[1]
    else:
        st.error("The dataset must contain at least two numerical columns for modeling.")
        st.stop()

---

# Machine Learning Pipeline (Linear Regression Baseline)
X = df[[feature_col]]
y = df[target_col]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Evaluation Metrics
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)

---

# KPI Metrics Display
st.subheader("🎯 Model Performance Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("R² Score", f"{r2:.4f}")
col2.metric("RMSE (Tons)", f"{rmse:.2f}")
col3.metric("MAE (Tons)", f"{mae:.2f}")

---

# Interactive Visualizations (Plotly)
st.subheader("📈 Interactive Energy vs. Emission Analysis")
fig = px.scatter(
    df, x=feature_col, y=target_col, 
    title=f"Relationship between {feature_col} and {target_col}",
    labels={feature_col: 'Energy Load (MW)', target_col: 'Carbon Emissions (Tons)'},
    trendline="ols"
)
st.plotly_chart(fig, use_container_width=True)

---

# Smart Recommendations Engine
st.subheader("💡 Proactive AI Recommendations")
max_load_idx = df[feature_col].idxmax()
peak_load_value = df.loc[max_load_idx, feature_col]

st.info(f"""
- **Peak Load Alert:** Maximum energy consumption detected at value `{peak_load_value}`.
- **Optimization Strategy:** Consider shifting non-critical industrial loads to off-peak hours or integrating solar-backed storage to mitigate high carbon emission spikes.
""")

# Footer
st.markdown("---")
st.markdown("🛠️ *EcoGrid-AI developed for industrial sustainability and enterprise-grade portfolio demonstration.*")
