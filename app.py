import streamlit as st
import pandas as pd
import plotly.express as px
from model import train_energy_model

# إعدادات الصفحة
st.set_page_config(page_title="EcoGrid-AI Dashboard", page_icon="⚡", layout="wide")

st.title("⚡ EcoGrid-AI: Industrial Carbon Footprint & Energy Grid Balancer")
st.markdown("لوحة تحكم ذكية ومتقدمة لرصد استهلاك الطاقة، تحليل انبعاثات الكربون، وتقديم توصيات استباقية للذكاء الاصطناعي.")

# زر تشغيل التحليل
if st.button("تشغيل التحليل والتوصيات الذكية"):
    model, mae, rmse, r2 = train_energy_model()
    
    try:
        df = pd.read_csv("real_energy_data.csv")
        st.success("تم تشغيل النظام وتحليل البيانات وتقديم التوصيات بنجاح!")
        
        # --- قسم التوصيات الذكية (AI Recommendations) ---
        st.subheader("💡 التوصيات الذكية والإجراءات الاستباقية (AI Recommendations)")
        
        # إيجاد ساعة الذروة (أعلى استهلاك للطاقة)
        peak_row = df.loc[df['energy_consumption_mw'].idxmax()]
        peak_time = str(peak_row['timestamp'])
        peak_energy = peak_row['energy_consumption_mw']
        
        # حساب نسبة توفير مقترحة للطاقة الشمسية بناءً على كفاءة النظام
        avg_efficiency = df['efficiency_score'].mean()
        solar_reduction_pct = round(max(15.0, 100 - avg_efficiency + 10), 1)
        
        rec_col1, rec_col2 = st.columns(2)
        
        with rec_col1:
            st.warning(f"⚠️ **تنبيه الأحمال العالية:** \n\n يوصى بـ **تقليل الحمل في الساعة {peak_time}** حيث بلغ استهلاك الطاقة قمة بواقع **{peak_energy} MW** لتجنب الضغط على الشبكة.")
            
        with rec_col2:
            st.success(f"☀️ **فرصة الاستدامة البديلة:** \n\n الاعتماد جزئياً على **الطاقة الشمسية قد تقلل الانبعاثات بنسبة {solar_reduction_pct}%** وتحسن مؤشر الكفاءة العامة للمصنع.")
            
        st.markdown("---")
        
        # --- قسم مقاييس دقة نموذج الذكاء الاصطناعي (Model Metrics) ---
        st.subheader("🎯 مقاييس دقة نموذج الذكاء الاصطناعي (Model Evaluation Metrics)")
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        with metric_col1:
            st.metric(label="معامل التحديد ($R^2 Score$)", value=f"{r2:.2f}", delta="جودة مطابقة النموذج")
        with metric_col2:
            st.metric(label="جذر متوسط مربع الخطأ ($RMSE$)", value=f"{rmse:.2f} طن", delta="دقة التنبؤات", delta_color="inverse")
        with metric_col3:
            st.metric(label="متوسط الخطأ المطلق ($MAE$)", value=f"{mae:.2f} طن", delta="معدل الانحراف", delta_color="inverse")
            
        st.markdown("---")
        
        # --- المؤشرات الحيوية للمصنع (KPIs) ---
        total_emissions = df['carbon_emission_tons'].sum()
        expected_reduction = round((100 - avg_efficiency) * 1.5, 2)
        
        st.subheader("📊 المؤشرات الرئيسية لأداء الطاقة (KPIs)")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="🌍 إجمالي الانبعاثات", value=f"{total_emissions:.2f} طن")
        with col2:
            st.metric(label="📉 نسبة الانخفاض المتوقعة", value=f"{expected_reduction}%", delta="مقارنة بالهدف المستهدف")
        with col3:
            st.metric(label="⚡ متوسط كفاءة الطاقة", value=f"{avg_efficiency:.2f}%")
        
        st.markdown("---")
        
        # --- رسوم Plotly التفاعلية ---
        st.subheader("📈 التحليلات البصرية المتقدمة (Plotly)")
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            fig_scatter = px.scatter(
                df, 
                x="energy_consumption_mw", 
                y="carbon_emission_tons", 
                size="efficiency_score", 
                color="efficiency_score",
                title="العلاقة بين استهلاك الطاقة وانبعاثات الكربون",
                labels={"energy_consumption_mw": "استهلاك الطاقة (MW)", "carbon_emission_tons": "انبعاثات الكربون (طن)"},
                color_continuous_scale="Viridis"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with col_chart2:
            fig_bar = px.bar(
                df, 
                x="timestamp", 
                y="efficiency_score", 
                title="مؤشر كفاءة الطاقة عبر الزمن",
                labels={"timestamp": "الوقت", "efficiency_score": "كفاءة الطاقة (%)"},
                color="efficiency_score",
                color_continuous_scale="Blues"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
        fig_line = px.line(
            df, 
            x="timestamp", 
            y=["energy_consumption_mw", "carbon_emission_tons"], 
            title="مقارنة زمنية شاملة لاستهلاك الطاقة وانبعاثات الكربون",
            labels={"value": "القيمة", "timestamp": "الوقت", "variable": "المؤشر"}
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
        with st.expander("📁 استعراض جدول البيانات الخام للمصنع"):
            st.dataframe(df, use_container_width=True)
        
    except Exception as e:
        st.error(f"حدث خطأ أثناء تحميل البيانات: {e}")

# الشريط الجانبي
st.sidebar.header("عن النظام")
st.sidebar.info("مشروع صناعي ذكي متكامل يدمج التوصيات الاستباقية وتعلم الآلة لخدمة قطاع الطاقة.")
