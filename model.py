import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def train_energy_model():
    print("جاري قراءة البيانات الممحاكاة...")
    try:
        # قراءة البيانات التي أنشأها المحاكي
        df = pd.read_csv("energy_data.csv")
    except FileNotFoundError:
        print("تنبيه: لم يتم العثور على ملف البيانات، يرجى تشغيل المحاكي أولاً.")
        return

    # تحديد المدخلات والمخرجات للذكاء الاصطناعي
    # نريد التنبؤ بانبعاثات الكربون بناءً على استهلاك الطاقة وكفاءة النظام
    X = df[['energy_consumption_mw', 'efficiency_score']]
    y = df['carbon_emission_tons']

    # تقسيم البيانات إلى بيانات تدريب وبيانات اختبار
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # بناء نموذج الانحدار الخطي (Linear Regression)
    model = LinearRegression()
    model.fit(X_train, y_train)

    # اختبار نموذج الذكاء الاصطناعي
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)

    print(f"تم تدريب نموذج الذكاء الاصطناعي بنجاح!")
    print(f"نسبة الخطأ في النموذج (MSE): {mse:.2f}")

    return model

if __name__ == "__main__":
    train_energy_model()
