# ⚡ EcoGrid-AI: Energy Analytics & Carbon Emission Predictor

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Library-Scikit_Learn-orange.svg)](https://scikit-learn.org/)
[![Plotly](https://img.shields.io/badge/Visualization-Plotly-green.svg)](https://plotly.com/)

A portfolio project demonstrating AI-based energy analytics and carbon emission prediction. **EcoGrid-AI** monitors power consumption patterns, forecasts carbon metrics using regression models, and provides proactive optimization recommendations for sustainability scenarios.

---

## ✨ Features
* **Real-time Data Processing:** Handles structured industrial energy datasets to track power usage, system efficiency, and emission metrics.
* **AI-Powered Predictive Modeling:** Employs Linear Regression to forecast carbon emissions based on energy load and operational efficiency.
* **Model Evaluation Metrics:** Dynamically calculates and displays scientific metrics ($R^2 Score$, $RMSE$, and $MAE$).
* **Interactive Visualizations:** Built with **Plotly** to provide dynamic, zoomable, and interactive charts for deep data exploration.
* **Smart Recommendations Engine:** Automatically detects peak load hours and estimates potential emission reductions via alternative energy sources like solar power.

---

## 🛠️ Technologies Used
* **Python**: Core programming language.
* **Pandas & NumPy**: Data manipulation and numerical operations.
* **Scikit-Learn**: Machine learning pipeline and regression models.
* **Streamlit**: Interactive web dashboard framework.
* **Plotly**: Advanced interactive data visualization.

---

## 🏗️ Project Architecture
```text
EcoGrid-AI/
│
├── real_energy_data.csv    # Industrial energy dataset (Power consumption & emissions)
├── model.py                # Machine learning training & evaluation pipeline
├── app.py                  # Streamlit interactive web dashboard
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
