import streamlit as st
import os
from datetime import datetime
from fpdf import FPDF
from PIL import Image
import base64

# 1. Config
st.set_page_config(layout="wide", page_title="Fire Safety Inspection")
st.title("🔥 Fire Safety & Building Inspection | الفحص الهندسي")

# 2. Sidebar: Company Info
st.sidebar.header("🏢 Company Info | معلومات الشركة")
company_name = st.sidebar.text_input("Company Name | اسم الشركة", "Safety Lines")
company_logo = st.sidebar.file_uploader("Upload Company Logo | رفع شعار الشركة", type=["png", "jpg", "jpeg"])
footer_info = st.sidebar.text_area("Footer (Address, Phone...) | تعديل التذييل", "Safety Lines\nAbu Dhabi, UAE\n+971-50-000-0000\nwww.safety-lines.ae\ninfo@safety-lines.ae")

# 3. Hero Image
hero_img = st.file_uploader("📸 Upload Building Hero Image | صورة المبنى", type=["png", "jpg", "jpeg"])

# 4. Inspection Info
st.subheader("📋 Inspection Info | بيانات الفحص")
inspector_name = st.text_input("Inspector Name | اسم المفتش")
date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"**Date & Time:** {date_time}")

# 5. Checklists from extracted PDF content (example structure)
questions = [
    "Is the fire alarm system operational?",
    "Are fire extinguishers inspected and tagged?",
    "Are emergency exits clearly marked?",
    "Is the sprinkler system in working condition?",
    "Is the evacuation plan posted and readable?",
    # Add remaining 70+ questions from PDF...
]

answers = {}
photos = {}

st.subheader("✅ Inspection Checklist | قائمة الفحص")

for i, q in enumerate(questions):
    col1, col2 = st.columns([3, 1])
    with col1:
        answers[q] = st.radio(f"{i+1}. {q}", ["Compliant", "Non-Compliant", "N/A"], key=q)
    with col2:
        photos[q] = st.file_uploader("📷 Photo", type=["jpg", "jpeg", "png"], key=f"photo_{i}")

# 6. Signature & Export
st.subheader("🖊️ Signature & Export | التوقيع والتصدير")
signature = st.text_input("Digital Signature | التوقيع", inspector_name)

if st.button("📄 Export PDF | تصدير تقرير PDF"):
    class PDF(FPDF):
        def header(self):
            if company_logo is not None:
                logo_path = "company_logo.png"
                with open(logo_path, "wb") as f:
                    f.write(company_logo.read())
                self.image(logo_path, 10, 8, 33)
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, f"Fire Safety Inspection Report | تقرير الفحص", border=False, ln=True, align="C")
            self.ln(10)

        def footer(self):
            self.set_y(-30)
            self.set_font("Arial", size=8)
            for line in footer_info.split("\n"):
                self.cell(0, 5, line, ln=True, align="C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Company: {company_name}", ln=True)
    pdf.cell(0, 10, f"Inspector: {inspector_name}", ln=True)
    pdf.cell(0, 10, f"Date & Time: {date_time}", ln=True)
    pdf.cell(0, 10, f"Digital Signature: {signature}", ln=True)

    if hero_img:
        hero_path = "hero_image.png"
        with open(hero_path, "wb") as f:
            f.write(hero_img.read())
        pdf.image(hero_path, x=10, y=None, w=180)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Inspection Checklist", ln=True)

    for i, q in enumerate(questions):
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, f"{i+1}. {q}")
        pdf.cell(0, 10, f"Answer: {answers[q]}", ln=True)
        if photos[q]:
            img_path = f"photo_{i}.jpg"
            with open(img_path, "wb") as f:
                f.write(photos[q].read())
            pdf.image(img_path, w=100)

    output_path = "inspection_report.pdf"
    pdf.output(output_path)

    with open(output_path, "rb") as f:
        st.download_button(
            label="📥 Download Report",
            data=f,
            file_name=f"Fire_Inspection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )

