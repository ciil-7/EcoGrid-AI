import streamlit as st
import pandas as pd
from model import train_energy_model

st.set_page_config(page_title="EcoGrid-AI Dashboard", page_icon="⚡", layout="wide")

st.title("⚡ EcoGrid-AI: Industrial Carbon Footprint & Energy Grid Balancer")
st.markdown("منصة ذكية متقدمة لرصد استهلاك الطاقة وتحليل انبعاثات الكربون للمنشآت الكبرى.")

# زر لتشغيل النموذج وتوليد البيانات
if st.button("تشغيل محاكاة وتحليل البيانات الآن"):
    model = train_energy_model()
    
    try:
        df = pd.read_csv("energy_data.csv")
        st.success("تم تحديث البيانات والنموذج بنجاح!")
        
        # عرض البيانات في جدول
        st.subheader("📊 جدول البيانات المسجلة للمصنع")
        st.dataframe(df, use_container_width=True)
        
        # رسم بياني لاستهلاك الطاقة
        st.subheader("📈 رسم بياني لمعدلات استهلاك الطاقة (MW)")
        st.line_chart(df.set_index("timestamp")["energy_consumption_mw"])
        
    except Exception as e:
        st.error(fحدث خطأ أثناء تحميل البيانات: {e}")

st.sidebar.header("عن النظام")
st.sidebar.info("مشروع احترافي مصمم خصيصاً لدعم قطاعات الطاقة والاستدامة بكفاءة عالية واحترافية تامة.")
