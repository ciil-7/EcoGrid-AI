import streamlit as st
import pandas as pd
from model import train_energy_model

# إعدادات الصفحة
st.set_page_config(page_title="EcoGrid-AI Dashboard", page_icon="⚡", layout="wide")

st.title("⚡ EcoGrid-AI: Industrial Carbon Footprint & Energy Grid Balancer")
st.markdown("لوحة تحكم ذكية ومتقدمة لرصد استهلاك الطاقة، تحليل انبعاثات الكربون، ومؤشرات الاستدامة الصناعية.")

# زر تشغيل التحليل
if st.button("تشغيل التحليل وتحديث المؤشرات"):
    model = train_energy_model()
    
    try:
        # قراءة البيانات الحقيقية
        df = pd.read_csv("real_energy_data.csv")
        st.success("تم تحليل البيانات الحقيقية بنجاح وعرض المؤشرات!")
        
        # --- حساب المؤشرات الحيوية (KPIs) ---
        total_emissions = df['carbon_emission_tons'].sum()
        avg_efficiency = df['efficiency_score'].mean()
        # حساب نسبة انخفاض افتراضية متوقعة بناءً على تحسين الكفاءة
        expected_reduction = round((100 - avg_efficiency) * 1.5, 2)
        
        # --- عرض المؤشرات في أعمدة متجاورة بتصميم راقي ---
        st.subheader("📊 المؤشرات الرئيسية لأداء الطاقة (KPIs)")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="🌍 إجمالي الانبعاثات", value=f"{total_emissions:.2f} طن")
            
        with col2:
            st.metric(label="📉 نسبة الانخفاض المتوقعة", value=f"{expected_reduction}%", delta="مقارنة بالهدف المستهدف")
            
        with col3:
            st.metric(label="⚡ متوسط كفاءة الطاقة", value=f"{avg_efficiency:.2f}%")
        
        st.markdown("---")
        
        # عرض البيانات في جدول تفصيلي
        data_expander = st.expander("📁 استعراض جدول البيانات الخام للمصنع")
        with data_expander:
            st.dataframe(df, use_container_width=True)
        
        # رسومات بيانية متقدمة
        st.subheader("📈 رسم بياني لمعدلات استهلاك الطاقة والانبعاثات")
        st.line_chart(df.set_index("timestamp")[["energy_consumption_mw", "carbon_emission_tons"]])
        
    except Exception as e:
        st.error(f"حدث خطأ أثناء تحميل البيانات: {e}")

# الشريط الجانبي
st.sidebar.header("عن النظام")
st.sidebar.info("مشروع صناعي ذكي مصمم لتعزيز أهداف الاستدامة ورفع كفاءة الشبكات الكهربائية.")
