import random
import time
import pandas as pd

def generate_plant_data():
    """
    توليد بيانات افتراضية لمصنع طاقة وانبعاثات الكربون
    """
    data = []
    print("بدء محاكي بيانات مصنع الطاقة والـ Carbon Footprint...")
    
    for i in range(10): # توليد 10 عينات تجريبية كمثال
        energy_consumption = round(random.uniform(150.0, 500.0), 2) # استهلاك الطاقة بالمجاواط
        carbon_emission = round(energy_consumption * 0.45 + random.uniform(-10, 10), 2) # انبعاثات الكربون
        efficiency_score = round(random.uniform(85.0, 99.5), 2) # كفاءة النظام
        
        record = {
            "timestamp": pd.Timestamp.now() + pd.Timedelta(minutes=i),
            "energy_consumption_mw": energy_consumption,
            "carbon_emission_tons": carbon_emission,
            "efficiency_score": efficiency_score
        }
        data.append(record)
    
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    df = generate_plant_data()
    print("\n عينة من البيانات المולدة بنجاح:")
    print(df)
    
    # حفظ البيانات في ملف CSV لنستخدمه في النماذج القادمة
    df.to_csv("energy_data.csv", index=False)
    print("\n تم حفظ البيانات بنجاح في ملف energy_data.csv!")
