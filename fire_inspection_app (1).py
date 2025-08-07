
import streamlit as st
from fpdf import FPDF
from PIL import Image
import os

st.set_page_config(page_title="🔥 Fire Safety Inspection", layout="wide")

# Sidebar Info
st.sidebar.markdown("🏢 **Company Info | معلومات الشركة**")
company_name = st.sidebar.text_input("Company Name | اسم الشركة", "Safety Lines")
company_logo = st.sidebar.file_uploader("Upload Company Logo | رفع شعار الشركة", type=["png", "jpg", "jpeg"])
footer = st.sidebar.text_area("Footer (Address, Phone...) | تعديل التقرير", "Safety Lines\nAbu Dhabi, UAE\n+971-50-000-0000\nwww.safety-lines.ae")

# Main Info
st.title("🔥 Fire Safety Inspection Report | تقرير فحص السلامة من الحرائق")
inspector_name = st.text_input("Digital Signature | التوقيع", "")

# Placeholder questions
questions = [
    "Is the fire alarm functional?",
    "Are all extinguishers in place and inspected?",
    "Are emergency exits clear and lit?",
    "Are fire drills conducted regularly?",
    "Are sprinklers tested and functional?"
]

responses = {}
st.subheader("Inspection Checklist | قائمة التحقق")
for question in questions:
    responses[question] = st.radio(question, ["Yes", "No", "N/A"], horizontal=True)

# Ensure PNG for FPDF
def ensure_png(image_file):
    if image_file and image_file.type != "image/png":
        image = Image.open(image_file)
        png_path = f"/tmp/{image_file.name}.png"
        image.save(png_path, format="PNG")
        return png_path
    elif image_file:
        return f"/tmp/{image_file.name}"
    return None

# Export PDF
if st.button("📄 Export PDF | تصدير تقرير"):
    class UnicodePDF(FPDF):
        def __init__(self):
            super().__init__()
            self.add_font("Noto", "", "NotoNaskhArabic-Regular.ttf", uni=True)
            self.set_font("Noto", size=12)

    pdf = UnicodePDF()
    pdf.add_page()

    # Logo
    logo_path = ensure_png(company_logo)
    if logo_path:
        pdf.image(logo_path, x=10, y=8, w=30)
        pdf.ln(20)

    # Header
    pdf.set_font("Noto", size=14)
    pdf.cell(0, 10, txt="تقرير فحص السلامة من الحرائق 🔥 Fire Safety Inspection Report", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Noto", size=12)
    pdf.cell(0, 10, txt=f"اسم الشركة | Company Name: {company_name}", ln=True)
    pdf.cell(0, 10, txt=f"التوقيع | Signature: {inspector_name}", ln=True)
    pdf.ln(10)

    # Responses
    for q, r in responses.items():
        pdf.multi_cell(0, 10, f"{q} — {r}")

    pdf.ln(10)
    pdf.multi_cell(0, 10, footer)

    output_path = "/tmp/fire_inspection_report.pdf"
    pdf.output(output_path)
    with open(output_path, "rb") as f:
        st.download_button("⬇️ Download PDF", f, file_name="fire_inspection_report.pdf")
