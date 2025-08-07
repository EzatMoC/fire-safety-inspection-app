
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

# Export PDF
if st.button("📤 Export PDF | تصدير تقرير PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    if company_logo:
        logo_path = os.path.join(tempfile.gettempdir(), "logo.jpg")
        with open(logo_path, "wb") as f:
            f.write(company_logo.read())
        pdf.image(logo_path, x=10, y=8, w=33)

    pdf.cell(200, 10, txt="Fire & Life Safety Inspection Report", ln=True, align="C")
    pdf.cell(200, 10, txt=company_name, ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Project: {building_name} | Location: {location}", ln=True)
    pdf.cell(200, 10, txt=f"Inspection No.: {inspection_no} | Date: {inspection_date}", ln=True)
    pdf.cell(200, 10, txt=f"Consultant: {consultant} | Contractor: {contractor} | Engineer: {site_engineer}", ln=True)

    if hero_photo:
        hero_path = os.path.join(tempfile.gettempdir(), "hero.jpg")
        with open(hero_path, "wb") as f:
            f.write(hero_photo.read())
        pdf.image(hero_path, x=10, y=pdf.get_y()+5, w=180)
        pdf.ln(65)

    for section, questions in checklist.items():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, txt=section, ln=True)
        pdf.set_font("Arial", size=11)
        for q in questions:
            pdf.multi_cell(0, 10, txt=f"• {q} - Answer: {answers[q]}")
            if photos[q]:
                img_path = os.path.join(tempfile.gettempdir(), f"img_{hash(q)}.jpg")
                with open(img_path, "wb") as f:
                    f.write(photos[q].read())
                try:
                    pdf.image(img_path, x=10, y=pdf.get_y()+5, w=100)
                    pdf.ln(55)
                except:
                    pdf.ln(5)
            else:
                pdf.ln(3)

    pdf.multi_cell(0, 10, txt=f"Notes: {notes}")
    pdf.cell(0, 10, txt=f"Inspector: {inspector_name} | Signature: {signature}", ln=True)
    pdf.cell(0, 10, txt=f"Time Submitted: {submit_time}", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt=company_footer)

    output_path = os.path.join(tempfile.gettempdir(), "final_fire_safety_report.pdf")
    pdf.output(output_path)

    with open(output_path, "rb") as f:
        st.download_button("⬇️ Download Final Report PDF", data=f, file_name="fire_safety_report.pdf", mime="application/pdf")
