import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import qrcode
import datetime
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="HealthSync | Diabetes Analysis", layout="wide")

# Theme Styling
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007BFF; color: white; font-weight: bold; }
    .stDownloadButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #28a745; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🩺 HealthSync Diagnostic Dashboard")

# 2. Compact Feature Definitions
with st.expander("📖 Clinical Parameter Reference"):
    cols = st.columns(3)
    cols[0].write("**HbA1c:** 3-month avg glucose. >6.5% is Diabetic.")
    cols[1].write("**Glucose:** Current mg/dL. >200 is high risk.")
    cols[2].write("**BMI:** Weight/Height ratio. 18.5-25 is healthy.")

st.markdown("---")

# 3. Input Section
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("👤 Patient Profile")
    patient_name = st.text_input("Full Patient Name", placeholder="e.g. Arnav Pandey")
    
    age = st.slider("Age (Years)", 1, 110, 25, step=1)
    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    
    h_ten = st.toggle("Hypertension (High BP history)")
    h_dis = st.toggle("Pre-existing Heart Disease")
    
    hypertension = 1 if h_ten else 0
    heart_disease = 1 if h_dis else 0
    
    smoking = st.selectbox("Smoking History", ["never", "current", "former", "No Info"])

with col2:
    st.subheader("📊 Clinical Measurements")
    bmi = st.slider("BMI (Body Mass Index)", 10.0, 50.0, 22.5, step=0.1)
    hba1c = st.slider("HbA1c Level (%)", 3.0, 15.0, 5.5, step=0.1)
    glucose = st.slider("Blood Glucose (mg/dL)", 50, 400, 100, step=1)

# 4. Processing and Analysis
st.markdown("---")

if st.button("🚀 Run Full Diagnostic Report"):
    if not patient_name:
        st.warning("⚠️ Please enter a patient name to generate the report.")
    else:
        # Integrated Risk Scoring Logic
        risk_score = 0
        if hba1c > 6.5: risk_score += 60
        if glucose > 140: risk_score += 20
        if bmi > 30: risk_score += 15
        if age > 50: risk_score += 5
        risk_score = min(risk_score, 100)

        # --- RESULT ROW ---
        res_col1, res_col2 = st.columns([1, 2])
        
        with res_col1:
            st.subheader(f"Results for {patient_name}")
            if risk_score > 50:
                st.error(f"### High Risk: {risk_score}%")
            elif risk_score > 20:
                st.warning(f"### Moderate Risk: {risk_score}%")
            else:
                st.success(f"### Low Risk: {risk_score}%")
  # --- DYNAMIC QR PDF GENERATOR ---
            
                
                
            # PDF Creation
        
            def create_pdf(name, age, gen, h, g, b, risk):
                # 3rd Option Logic: Dynamic Patient Education Link
                if risk > 50:
                    # Link to Diabetes Management / Doctor Finder
                    qr_url = "https://www.diabetes.org/diabetes/newly-diagnosed"
                else:
                    # Link to Prevention / Healthy Living
                    qr_url = "https://www.cdc.gov/diabetes/prevention/index.html"

                qr = qrcode.make(qr_url)
                qr_path = "temp_qr.png"
                qr.save(qr_path)
                
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 20); pdf.set_text_color(0, 123, 255)
                pdf.cell(200, 20, txt="HealthSync Medical Report", ln=True, align='C')
                pdf.set_font("Arial", size=12); pdf.set_text_color(0,0,0)
                pdf.ln(10)
                pdf.cell(200, 10, txt=f"Date: {datetime.date.today()}", ln=True)
                pdf.cell(200, 10, txt=f"Patient Name: {name}", ln=True)
                pdf.cell(200, 10, txt=f"Metrics: HbA1c {h}%, Glucose {g}mg/dL, BMI {b}", ln=True)
                pdf.ln(10); pdf.set_font("Arial", 'B', 14)
                pdf.cell(200, 12, txt=f"Final Estimated Risk: {risk}%", ln=True, align='C', fill=False)
                pdf.ln(10); pdf.set_font("Arial", size=12)
            
                pdf.image(qr_path, x=145, y=pdf.get_y(), w=35)
                pdf.set_font("Arial", 'B', 9)
                pdf.text(142, pdf.get_y() + 38, "SCAN FOR NEXT STEPS")
                
                
                return pdf.output(dest='S').encode('latin-1')

            pdf_bytes = create_pdf(patient_name, age, gender, hba1c, glucose, bmi, risk_score)
            st.download_button(label="📥 Download PDF Report", data=pdf_bytes, file_name=f"{patient_name}_Report.pdf", mime="application/pdf")

        with res_col2:
            st.subheader("Visual Analysis")
            fig, ax = plt.subplots(1, 3, figsize=(15, 5))
            
            # Graph 1: HbA1c Gauge
            c_h = 'red' if hba1c > 6.5 else 'orange' if hba1c > 5.7 else 'green'
            ax[0].barh(["HbA1c"], [hba1c], color=c_h)
            ax[0].axvline(6.5, color='black', ls='--')
            ax[0].set_title("HbA1c status")

            # Graph 2: Glucose Comparison
            ax[1].stem(["Fasting", "Target", "Current"], [100, 140, glucose])
            ax[1].set_title("Glucose Benchmarks")

            # Graph 3: BMI Pie
            bmi_cats = ['Underweight', 'Healthy', 'Overweight', 'Obese']
            bmi_colors = ['#f1f1f1', '#90ee90', '#ffcc99', '#ff9999']
            ax[2].pie([18.5, 6.5, 5, 10], labels=bmi_cats, colors=bmi_colors, startangle=90)
            ax[2].set_title(f"BMI Category ({bmi})")
            st.pyplot(fig)

        # --- ACTIONABLE ADVICE & WHAT-IF ---
        st.markdown("---")
        adv_col1, adv_col2 = st.columns(2)
        
        with adv_col1:
            st.subheader("📋 Clinical Recommendations")
            if hba1c > 6.5:
                st.write("❌ **Urgent:** Schedule a Fasting Plasma Glucose test.")
                st.write("❌ **Diet:** Significantly reduce refined sugar intake.")
            else:
                st.write("✅ **Maintenance:** Continue current activity levels.")
                st.write("✅ **Lifestyle:** Ensure 7-8 hours of sleep for metabolic health.")

        with adv_col2:
            st.subheader("📉 'What-If' Simulation")
            if bmi > 25:
                new_risk = max(risk_score - 15, 5)
                st.info(f"If BMI is reduced to **24.0**, your risk drops from **{risk_score}%** to **{new_risk}%**.")
            else:
                st.success("Your BMI is optimal. Focus on maintaining muscle mass through protein intake.")

# 6. Footer
st.markdown("---")
st.caption("🚨 Disclaimer: Educational tool only. Consult a doctor for medical advice.")