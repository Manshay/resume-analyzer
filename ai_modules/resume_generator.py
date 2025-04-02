from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import pdfkit
from datetime import datetime

class ResumeGenerator:
    def __init__(self, template_type):
        self.template_type = template_type
        self.document = Document()
    
    def add_header(self, name, contact_info):
        if self.template_type == "Professional":
            header = self.document.add_paragraph()
            header.alignment = WD_ALIGN_PARAGRAPH.CENTER
            name_run = header.add_run(name)
            name_run.bold = True
            name_run.font.size = Pt(16)
            
            contact_paragraph = self.document.add_paragraph()
            contact_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            contact_run = contact_paragraph.add_run(
                f"{contact_info['email']} | {contact_info['phone']} | {contact_info['location']}"
            )
            if contact_info['linkedin']:
                contact_run.add_text(f" | {contact_info['linkedin']}")
    
    def add_summary(self, summary):
        self.document.add_heading('Professional Summary', level=1)
        self.document.add_paragraph(summary)
    
    def add_experience(self, experiences):
        self.document.add_heading('Work Experience', level=1)
        for exp in experiences:
            p = self.document.add_paragraph()
            p.add_run(f"{exp['company']} - {exp['title']}").bold = True
            p.add_run(f"\n{exp['start']} - {exp['end']}")
            self.document.add_paragraph(exp['responsibilities'])
    
    def add_education(self, education):
        self.document.add_heading('Education', level=1)
        for edu in education:
            p = self.document.add_paragraph()
            p.add_run(f"{edu['institution']} - {edu['degree']}").bold = True
            p.add_run(f"\n{edu['start']} - {edu['end']}")
            if edu['description']:
                self.document.add_paragraph(edu['description'])
    
    def add_skills(self, skills):
        self.document.add_heading('Skills', level=1)
        self.document.add_paragraph(skills)
    
    def generate(self, resume_data):
        self.add_header(resume_data['name'], {
            'email': resume_data['email'],
            'phone': resume_data['phone'],
            'location': resume_data['location'],
            'linkedin': resume_data['linkedin']
        })
        self.add_summary(resume_data['summary'])
        self.add_experience(resume_data['experiences'])
        self.add_education(resume_data['education'])
        self.add_skills(resume_data['skills'])
        
        return self.document