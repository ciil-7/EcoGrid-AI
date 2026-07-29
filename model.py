import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def train_energy_model():
    print("جاري قراءة البيانات الحقيقية للمصنع...")
    try:
        # قراءة البيانات الحقيقية التي أضفناها
        df = pd.read_csv("real_energy_data.csv")
    except FileNotFoundError:
        print("تنبيه: لم يتم العثور على ملف البيانات الحقيقية.")
        return None

    # تحديد المدخلات والمخرجات
    X = df[['energy_consumption_mw', 'efficiency_score']]
    y = df['carbon_emission_tons']

    # تقسيم البيانات للتدريب والاختبار
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # بناء نموذج الانحدار الخطي
    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)

    print(f"تم تدريب النموذج بنجاح على البيانات الحقيقية!")
    print(f"نسبة الخطأ في النموذج (MSE): {mse:.2f}")

    return model

if __name__ == "__main__":
    train_energy_model()
