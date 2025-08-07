from fpdf import FPDF
import streamlit as st
from PIL import Image
from datetime import datetime

st.set_page_config(layout="wide")
st.title("🔥 Fire Safety Inspection Report Generator")
st.markdown("---")

# Sidebar - Company Info
st.sidebar.header("🏢 Company Info | معلومات الشركة")
company_name = st.sidebar.text_input("Company Name | اسم الشركة", "Safety Lines")
logo_file = st.sidebar.file_uploader("Upload Company Logo | رفع شعار الشركة", type=["png", "jpg", "jpeg"])
footer = st.sidebar.text_area("Footer (Address, Phone...) | تعديل التذييل", "Safety Lines\nAbu Dhabi, UAE\n+971-50-000-0000\nwww.safety-lines.ae")

# Hero image
hero_path = None
if logo_file:
    hero_path = f"uploaded_logo.{logo_file.type.split('/')[-1]}"
    with open(hero_path, "wb") as f:
        f.write(logo_file.read())

# Inspector Signature
inspector_name = st.text_input("Digital Signature | التوقيع", "Arun Vignesh")

# Convert uploaded image to PNG
def ensure_png(image_path):
    try:
        image = Image.open(image_path)
        png_path = image_path + ".png"
        image.save(png_path, format="PNG")
        return png_path
    except Exception as e:
        st.error(f"❌ Image conversion failed: {e}")
        return None

# Generate PDF
if st.button("📄 Export PDF | تصدير تقرير PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("ArialUnicode", "", fname="ArialUnicodeMS.ttf", uni=True)
    pdf.set_font("ArialUnicode", size=12)

    # Add logo image if uploaded
    if hero_path:
        png_path = ensure_png(hero_path)
        if png_path:
            try:
                pdf.image(png_path, x=10, y=10, w=180)
                pdf.ln(65)
            except Exception as e:
                st.warning(f"⚠️ Couldn't add image to PDF: {e}")

    # Report Title & Inspector
    pdf.set_font("ArialUnicode", size=16)
    pdf.cell(200, 10, txt="🔥 Fire Safety Inspection Report | تقرير فحص السلامة من الحرائق", ln=True, align="C")
    pdf.set_font("ArialUnicode", size=12)
    pdf.cell(200, 10, txt=f"Prepared by | أعده: {inspector_name}", ln=True, align="C")
    pdf.ln(10)

    # Company Info
    pdf.set_font("ArialUnicode", size=12)
    pdf.multi_cell(0, 10, f"🏢 Company: {company_name}\n📅 Date: {datetime.today().strftime('%Y-%m-%d')}", align="L")
    pdf.ln(5)

    # Placeholder for checklist
    pdf.set_font("ArialUnicode", size=12)
    pdf.cell(200, 10, txt="🧾 Checklist Sections will be added here...", ln=True, align="L")

    # Footer
    pdf.set_y(-30)
    pdf.set_font("ArialUnicode", size=10)
    pdf.multi_cell(0, 5, footer, align="C")

    # Export PDF
    output_path = "fire_inspection_report.pdf"
    try:
        pdf.output(output_path)
        with open(output_path, "rb") as f:
            st.download_button("⬇️ Download PDF", f, file_name="fire_inspection_report.pdf")
    except Exception as e:
        st.error(f"❌ Failed to generate PDF: {e}")
