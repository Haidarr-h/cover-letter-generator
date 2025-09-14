from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def generate_pdf(content: str) -> BytesIO:
  buffer = BytesIO()
  doc = SimpleDocTemplate(buffer)
  styles = getSampleStyleSheet()
  
  custom_style = ParagraphStyle(
    "Custom",
    parent=styles["Normal"],
    leftIndent=20,
    alignment=TA_JUSTIFY
  )
  
  story = []
  
  for para in content.split("\n\n"):
    story.append(Paragraph(para.replace("\n", "<br/>"), custom_style))
    story.append(Spacer(1,12))
  
  doc.build(story)
  buffer.seek(0)
  return buffer

def generate_doc(content: str) -> BytesIO:
  buffer = BytesIO()
  doc = Document()
  
  for para in content.split("\n\n"):
    p = doc.add_paragraph(para)
    
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    p.paragraph_format.first_line_indent = Inches(0.3)
    
    p.paragraph_format.space_after = Pt(12)
  
  doc.save(buffer)
  buffer.seek(0)
  return buffer