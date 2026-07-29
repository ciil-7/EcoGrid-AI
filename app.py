import streamlit as st
import pandas as pd
import plotly.express as px
from model import train_energy_model

# Page Configuration
st.set_page_config(page_title="EcoGrid-AI Dashboard", page_icon="⚡", layout="wide")

st.title("⚡ EcoGrid-AI: Industrial Carbon Footprint & Energy Grid Balancer")
st.markdown("An advanced AI dashboard designed to monitor energy consumption, analyze carbon emissions, and deliver proactive recommendations.")

# Analysis Trigger Button
if st.button("Run AI Analysis & Recommendations"):
    model, mae, rmse, r2 = train_energy_model()
    
    try:
        df = pd.read_csv("real_energy_data.csv")
        st.success("System executed successfully. Data and AI models analyzed!")
        
        # --- AI Recommendations Section ---
        st.subheader("💡 AI Recommendations & Proactive Actions")
        
        peak_row = df.loc[df['energy_consumption_mw'].idxmax()]
        peak_time = str(peak_row['timestamp'])
        peak_energy = peak_row['energy_consumption_mw']
        
        avg_efficiency = df['efficiency_score'].mean()
        solar_reduction_pct = round(max(15.0, 100 - avg_efficiency + 10), 1)
        
        rec_col1, rec_col2 = st.columns(2)
        
        with rec_col1:
            st.warning(f"⚠️ **Peak Load Alert:** \n\n Recommended to **reduce load at {peak_time}** as energy consumption peaked at **{peak_energy} MW** to prevent grid strain.")
            
        with rec_col2:
            st.success(f"☀️ **Sustainability Opportunity:** \n\n Integrating **solar energy could reduce emissions by {solar_reduction_pct}%** and improve overall plant efficiency.")
            
        st.markdown("---")
        
        # --- Model Evaluation Metrics Section ---
        st.subheader("🎯 Model Evaluation Metrics")
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        with metric_col1:
            st.metric(label="R² Score", value=f"{r2:.2f}", delta="Model Fit Quality")
        with metric_col2:
            st.metric(label="Root Mean Squared Error (RMSE)", value=f"{rmse:.2f} tons", delta="Prediction Accuracy", delta_color="inverse")
        with metric_col3:
            st.metric(label="Mean Absolute Error (MAE)", value=f"{mae:.2f} tons", delta="Deviation Rate", delta_color="inverse")
            
        st.markdown("---")
        
        # --- Energy KPIs Section ---
        total_emissions = df['carbon_emission_tons'].sum()
        expected_reduction = round((100 - avg_efficiency) * 1.5, 2)
        
        st.subheader("📊 Energy Performance KPIs")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="Total Carbon Emissions", value=f"{total_emissions:.2f} tons")
        with col2:
            st.metric(label="Expected Reduction Rate", value=f"{expected_reduction}%", delta="Target Comparison")
        with col3:
            st.metric(label="Average Energy Efficiency", value=f"{avg_efficiency:.2f}%")
        
        st.markdown("---")
        
        # --- Advanced Plotly Visualizations ---
        st.subheader("📈 Advanced Visual Analytics")
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            fig_scatter = px.scatter(
                df, 
                x="energy_consumption_mw", 
                y="carbon_emission_tons", 
                size="efficiency_score", 
                color="efficiency_score",
                title="Energy Consumption vs Carbon Emissions",
                labels={"energy_consumption_mw": "Energy Consumption (MW)", "carbon_emission_tons": "Carbon Emissions (tons)"},
                color_continuous_scale="Viridis"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with col_chart2:
            fig_bar = px.bar(
                df, 
                x="timestamp", 
                y="efficiency_score", 
                title="Energy Efficiency Trend Over Time",
                labels={"timestamp": "Timestamp", "efficiency_score": "Efficiency (%)"},
                color="efficiency_score",
                color_continuous_scale="Blues"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
        fig_line = px.line(
            df, 
            x="timestamp", 
            y=["energy_consumption_mw", "carbon_emission_tons"], 
            title="Comprehensive Timeline Comparison",
            labels={"value": "Value", "timestamp": "Timestamp", "variable": "Metric"}
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
        with st.expander("📁 View Raw Plant Dataset"):
            st.dataframe(df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading data: {e}")

# Sidebar
st.sidebar.header("About System")
st.sidebar.info("A smart energy analytics portfolio project integrating machine learning and interactive dashboards.")
