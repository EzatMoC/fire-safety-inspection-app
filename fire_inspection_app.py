
import streamlit as st
import json
from datetime import datetime
from fpdf import FPDF
import os
import tempfile

# Load checklist from external file
with open("fire_safety_checklist.json", "r", encoding="utf-8") as f:
    checklist = json.load(f)

st.set_page_config(page_title="Fire & Life Safety Inspection", layout="wide")
st.title("🔥 Fire & Life Safety Inspection Report | تقرير فحص السلامة من الحرائق")

# Sidebar: Company Info
st.sidebar.header("🏢 Company Info | معلومات الشركة")
company_name = st.sidebar.text_input("Company Name | اسم الشركة")
company_logo = st.sidebar.file_uploader("Upload Company Logo | رفع شعار الشركة", type=["png", "jpg"])
company_footer = st.sidebar.text_area("Footer (Address, Phone...) | تذييل التقرير")

# Inspection Info
st.subheader("📋 Inspection Info | بيانات الفحص")
building_name = st.text_input("Building Name | اسم المبنى")
location = st.text_input("Location | الموقع")
inspection_no = st.text_input("Inspection No. | رقم الفحص")
consultant = st.text_input("Consultant | الاستشاري")
contractor = st.text_input("Contractor | المقاول")
site_engineer = st.text_input("Site Engineer | مهندس الموقع")
inspection_date = st.date_input("Inspection Date | تاريخ الفحص", datetime.today())

# Hero Image
st.markdown("### 🏞 Building Overview Photo | صورة المبنى")
hero_photo = st.file_uploader("Upload Overview Photo | رفع صورة عامة", type=["png", "jpg"])

# Checklist
st.markdown("### ✅ Checklist | قائمة الفحص")
answers = {}
photos = {}

for section, questions in checklist.items():
    st.markdown(f"#### 📌 {section}")
    for q in questions:
        col1, col2 = st.columns([2, 1])
        with col1:
            answers[q] = st.radio(q, ["Yes", "No", "N/A"], key=q)
        with col2:
            photos[q] = st.file_uploader(f"📸 {q}", type=["jpg", "png"], key="photo_" + q[:15])

# Notes & Signature
st.subheader("📝 Notes / Signature | ملاحظات / توقيع")
notes = st.text_area("Inspector Notes | ملاحظات المفتش")
inspector_name = st.text_input("Inspector Name | اسم المفتش")
signature = st.text_input("Digital Signature | التوقيع")
submit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(output_path, "rb") as f:
        st.download_button("⬇️ Download Final Report PDF", data=f, file_name="fire_safety_report.pdf", mime="application/pdf")
