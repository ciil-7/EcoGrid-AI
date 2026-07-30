import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
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

st.markdown("---")

# Sidebar: Data Source & Model Configuration
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

# Model Selection Option in Sidebar
st.sidebar.markdown("### 🤖 Model Benchmarking")
selected_model_name = st.sidebar.selectbox(
    "Choose ML Model:",
    ("Linear Regression (Baseline)", "Random Forest Regressor (Advanced)", "Compare Both Models")
)

# Main Dashboard Layout
st.subheader("📊 Dataset Overview & Preview")
st.dataframe(df.head(), use_container_width=True)

# Feature Selection
if 'Energy_Load' in df.columns and 'Carbon_Emissions' in df.columns:
    feature_col = 'Energy_Load'
    target_col = 'Carbon_Emissions'
else:
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(num_cols) >= 2:
        feature_col = num_cols[0]
        target_col = num_cols[1]
    else:
        st.error("The dataset must contain at least two numerical columns for modeling.")
        st.stop()

# Machine Learning Pipeline & Training
X = df[[feature_col]]
y = df[target_col]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize Models
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_pred = lr_model.predict(X_test)

rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)

st.markdown("---")

# Display Metrics Based on Selection
if selected_model_name == "Linear Regression (Baseline)":
    st.subheader("🎯 Model Performance: Linear Regression")
    r2 = r2_score(y_test, lr_pred)
    rmse = np.sqrt(mean_squared_error(y_test, lr_pred))
    mae = mean_absolute_error(y_test, lr_pred)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("R² Score", f"{r2:.4f}")
    col2.metric("RMSE (Tons)", f"{rmse:.2f}")
    col3.metric("MAE (Tons)", f"{mae:.2f}")

elif selected_model_name == "Random Forest Regressor (Advanced)":
    st.subheader("🎯 Model Performance: Random Forest Regressor")
    r2 = r2_score(y_test, rf_pred)
    rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
    mae = mean_absolute_error(y_test, rf_pred)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("R² Score", f"{r2:.4f}")
    col2.metric("RMSE (Tons)", f"{rmse:.2f}")
    col3.metric("MAE (Tons)", f"{mae:.2f}")

else: # Compare Both Models
    st.subheader("⚖️ Model Benchmarking Comparison")
    
    lr_r2 = r2_score(y_test, lr_pred)
    lr_rmse = np.sqrt(mean_squared_error(y_test, lr_pred))
    lr_mae = mean_absolute_error(y_test, lr_pred)
    
    rf_r2 = r2_score(y_test, rf_pred)
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
    rf_mae = mean_absolute_error(y_test, rf_pred)
    
    comparison_df = pd.DataFrame({
        "Model": ["Linear Regression", "Random Forest Regressor"],
        "R² Score": [lr_r2, rf_r2],
        "RMSE": [lr_rmse, rf_rmse],
        "MAE": [lr_mae, rf_mae]
    })
    st.dataframe(comparison_df.style.highlight_max(axis=0, subset=["R² Score"]), use_container_width=True)

st.markdown("---")

# Interactive Visualizations (Plotly)
st.subheader("📈 Interactive Energy vs. Emission Analysis")
fig = px.scatter(
    df, x=feature_col, y=target_col, 
    title=f"Relationship between {feature_col} and {target_col}",
    labels={feature_col: 'Energy Load (MW)', target_col: 'Carbon Emissions (Tons)'},
    trendline="ols" if selected_model_name != "Random Forest Regressor (Advanced)" else None
)
st.plotly_chart(fig, use_container_width=True)

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
