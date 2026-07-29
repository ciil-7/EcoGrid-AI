import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

def train_energy_model():
    print("جاري قراءة البيانات وتدريب نموذج الذكاء الاصطناعي...")
    try:
        df = pd.read_csv("real_energy_data.csv")
    except FileNotFoundError:
        print("تنبيه: لم يتم العثور على ملف البيانات الحقيقية.")
        return None, 0, 0, 0

    X = df[['energy_consumption_mw', 'efficiency_score']]
    y = df['carbon_emission_tons']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    
    # حساب مقاييس الدقة والتقييم
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    print(f"تم تدريب النموذج بنجاح! R² = {r2:.2f}, RMSE = {rmse:.2f}")

    return model, mae, rmse, r2

if __name__ == "__main__":
    train_energy_model()
