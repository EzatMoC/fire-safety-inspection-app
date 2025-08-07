import streamlit as st
from fpdf import FPDF
from PIL import Image
import os
import datetime

# Custom FPDF class for Unicode (Arabic) support
class UnicodePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_page()
        self.add_font("Noto", "", "NotoNaskhArabic-Regular.ttf", uni=True)
        self.set_font("Noto", size=12)

    def header(self):
        self.set_font("Noto", size=16)
        self.cell(0, 10, 'تقرير فحص السلامة من الحريق', ln=True, align='C')
        self.ln(10)

    def add_section_title(self, title):
        self.set_font("Noto", size=14)
        self.set_text_color(0, 0, 128)
        self.cell(0, 10, title, ln=True, align='R')
        self.set_text_color(0, 0, 0)

    def add_question_answer(self, question, answer):
        self.multi_cell(0, 10, f'{question} : {answer}', align='R')

# Streamlit App UI
st.set_page_config(page_title="Fire Safety Inspection", layout="wide")
st.title("📋 Fire Safety Inspection App")

st.sidebar.header("🏢 Company Info | معلومات الشركة")
company_name = st.sidebar.text_input("اسم الشركة | Company Name", "Safety Lines")
logo = st.sidebar.file_uploader("رفع شعار الشركة | Upload Company Logo", type=["png", "jpg", "jpeg"])
footer = st.sidebar.text_area("تعديل (Address, Phone...) | Footer", "Safety Lines\nAbu Dhabi, UAE\n+971-50-000-0000\nwww.safety-lines.ae")

st.markdown("### 🔥 Checklist | قائمة الفحص")
questions = [
    "هل مخارج الطوارئ واضحة ومضيئة؟",
    "هل يتم إجراء تدريبات الإخلاء بانتظام؟",
    "هل أنظمة الرش تعمل؟"
]
answers = {}
for q in questions:
    answers[q] = st.radio(q, ["Yes", "No", "N/A"], horizontal=True)

signature = st.text_input("🖊️ التوقيع | Digital Signature")

if st.button("🧾 تصدير تقرير | Export PDF"):
    pdf = UnicodePDF()

    # Add logo
    if logo:
        logo_path = os.path.join("temp_logo.png")
        with open(logo_path, "wb") as f:
            f.write(logo.read())
        try:
            pdf.image(logo_path, x=10, y=8, w=40)
        except RuntimeError:
            st.error("❌ Logo must be a valid PNG or JPG file.")

    pdf.ln(30)
    pdf.set_font("Noto", size=12)
    pdf.cell(0, 10, f"اسم الشركة: {company_name}", ln=True, align='R')
    pdf.cell(0, 10, f"تاريخ الفحص: {datetime.datetime.now().strftime('%Y-%m-%d')}", ln=True, align='R')
    pdf.ln(5)

    pdf.add_section_title("نتائج الفحص:")
    for q, a in answers.items():
        pdf.add_question_answer(q, a)

    pdf.ln(10)
    pdf.add_section_title("ملاحظات إضافية:")
    pdf.multi_cell(0, 10, footer, align='R')

    pdf.ln(10)
    pdf.add_section_title("التوقيع:")
    pdf.cell(0, 10, signature, ln=True, align='R')

    output_path = "inspection_report.pdf"
    pdf.output(output_path)

    with open(output_path, "rb") as f:
        st.download_button("⬇️ تحميل التقرير | Download PDF Report", f, file_name=output_path)

    st.success("✅ تم تصدير التقرير بنجاح!")
