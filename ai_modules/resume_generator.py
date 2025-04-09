from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Twips
import pdfkit
import os
from datetime import datetime

class EnhancedResumeGenerator:
    def __init__(self, template_type):
        self.template_type = template_type
        self.document = Document()
        self._setup_styles()
    
    def _setup_styles(self):
        # Template-specific styles
        styles = {
            "Professional": {
                "colors": {"primary": RGBColor(0, 51, 102), "secondary": RGBColor(128, 128, 128)},
                "fonts": {"heading": "Calibri", "body": "Calibri"},
                "spacing": {"before": Pt(12), "after": Pt(8)}
            },
            "Modern": {
                "colors": {"primary": RGBColor(51, 51, 51), "secondary": RGBColor(0, 102, 204)},
                "fonts": {"heading": "Arial", "body": "Arial"},
                "spacing": {"before": Pt(14), "after": Pt(10)}
            },
            "Creative": {
                "colors": {"primary": RGBColor(76, 175, 80), "secondary": RGBColor(33, 33, 33)},
                "fonts": {"heading": "Georgia", "body": "Helvetica"},
                "spacing": {"before": Pt(14), "after": Pt(10)}
            },
            "Academic": {
                "colors": {"primary": RGBColor(140, 20, 20), "secondary": RGBColor(68, 68, 68)},
                "fonts": {"heading": "Times New Roman", "body": "Times New Roman"},
                "spacing": {"before": Pt(12), "after": Pt(6)}
            },
            "Technical": {
                "colors": {"primary": RGBColor(25, 118, 210), "secondary": RGBColor(66, 66, 66)},
                "fonts": {"heading": "Consolas", "body": "Segoe UI"},
                "spacing": {"before": Pt(10), "after": Pt(8)}
            }
        }
        
        # Apply template styles
        style = styles.get(self.template_type, styles["Professional"])
        
        # Header Style
        header_style = self.document.styles.add_style('CustomHeader', WD_STYLE_TYPE.PARAGRAPH)
        header_style.font.name = style["fonts"]["heading"]
        header_style.font.size = Pt(24)
        header_style.font.color.rgb = style["colors"]["primary"]
        header_style.paragraph_format.space_after = Pt(4)
        
        # Heading Style
        heading_style = self.document.styles.add_style('CustomHeading', WD_STYLE_TYPE.PARAGRAPH)
        heading_style.font.name = style["fonts"]["heading"]
        heading_style.font.size = Pt(16)
        heading_style.font.color.rgb = style["colors"]["primary"]
        heading_style.font.bold = True
        heading_style.paragraph_format.space_before = style["spacing"]["before"]
        heading_style.paragraph_format.space_after = style["spacing"]["after"]
        
        # Body Style
        body_style = self.document.styles.add_style('CustomBody', WD_STYLE_TYPE.PARAGRAPH)
        body_style.font.name = style["fonts"]["body"]
        body_style.font.size = Pt(11)
        body_style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        
        # Subheading Style
        subheading_style = self.document.styles.add_style('CustomSubheading', WD_STYLE_TYPE.PARAGRAPH)
        subheading_style.font.name = style["fonts"]["body"]
        subheading_style.font.size = Pt(12)
        subheading_style.font.color.rgb = style["colors"]["secondary"]
        
        # Set document margins based on template
        sections = self.document.sections
        for section in sections:
            if self.template_type == "Creative":
                section.top_margin = Inches(0.8)
                section.left_margin = Inches(1.0)
            elif self.template_type == "Academic":
                section.top_margin = Inches(1.0)
                section.left_margin = Inches(1.2)
            else:
                section.top_margin = Inches(0.5)
                section.left_margin = Inches(0.7)
            section.bottom_margin = section.top_margin
            section.right_margin = section.left_margin

    def save(self, output_path):
        """Save resume in both DOCX and PDF formats"""
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save DOCX
        docx_path = f"{output_path}.docx"
        self.document.save(docx_path)
        
        # Convert to PDF
        try:
            pdf_path = f"{output_path}.pdf"
            # Configure PDF conversion options
            options = {
                'page-size': 'Letter',
                'margin-top': '0.5in',
                'margin-right': '0.5in',
                'margin-bottom': '0.5in',
                'margin-left': '0.5in',
                'encoding': 'UTF-8'
            }
            
            pdfkit.from_file(docx_path, pdf_path, options=options)
            return {
                'docx_path': docx_path,
                'pdf_path': pdf_path
            }
        except Exception as e:
            print(f"PDF conversion failed: {str(e)}")
            return {
                'docx_path': docx_path,
                'pdf_path': None
            }

    # Update existing methods to use new styles
    def add_header(self, name, contact_info):
        # Template-specific header formatting
        if self.template_type == "Creative":
            self._add_creative_header(name, contact_info)
        elif self.template_type == "Technical":
            self._add_technical_header(name, contact_info)
        else:
            self._add_standard_header(name, contact_info)

    def _add_standard_header(self, name, contact_info):
        header = self.document.add_paragraph(style='CustomHeader')
        header.alignment = WD_ALIGN_PARAGRAPH.CENTER
        name_run = header.add_run(name)
        name_run.bold = True
        
        self._add_horizontal_line()
        
        contact_paragraph = self.document.add_paragraph(style='CustomBody')
        contact_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        contact_text = []
        if contact_info['email']: contact_text.append(contact_info['email'])
        if contact_info['phone']: contact_text.append(contact_info['phone'])
        if contact_info['location']: contact_text.append(contact_info['location'])
        if contact_info['linkedin']: contact_text.append(contact_info['linkedin'])
        if contact_info['portfolio']: contact_text.append(contact_info['portfolio'])
        
        contact_paragraph.add_run(' | '.join(contact_text))
        
        self.document.add_paragraph()  # Add spacing

    def _add_creative_header(self, name, contact_info):
        # Add name with creative styling
        header = self.document.add_paragraph(style='CustomHeader')
        header.alignment = WD_ALIGN_PARAGRAPH.LEFT
        name_run = header.add_run(name.upper())
        name_run.bold = True
        
        # Add contact info in two columns
        table = self.document.add_table(rows=2, cols=2)
        table.style = 'Table Grid'
        table.autofit = True
        
        # Left column
        cell = table.cell(0, 0)
        p = cell.paragraphs[0]
        p.add_run(f"📧 {contact_info['email']}\n")
        p.add_run(f"📱 {contact_info['phone']}")
        
        # Right column
        cell = table.cell(0, 1)
        p = cell.paragraphs[0]
        p.add_run(f"📍 {contact_info['location']}\n")
        if contact_info['linkedin']:
            p.add_run(f"🔗 {contact_info['linkedin']}")

    def _add_technical_header(self, name, contact_info):
        # Add name with monospace font
        header = self.document.add_paragraph(style='CustomHeader')
        header.alignment = WD_ALIGN_PARAGRAPH.LEFT
        name_run = header.add_run(f">>> {name}")
        name_run.bold = True
        
        # Add contact info in code-like format
        contact = self.document.add_paragraph(style='CustomBody')
        contact.add_run("{\n")
        contact.add_run(f'    "email": "{contact_info["email"]}",\n')
        contact.add_run(f'    "phone": "{contact_info["phone"]}",\n')
        contact.add_run(f'    "location": "{contact_info["location"]}",\n')
        if contact_info['linkedin']:
            contact.add_run(f'    "linkedin": "{contact_info["linkedin"]}"\n')
        contact.add_run("}")

    def _add_horizontal_line(self):
        paragraph = self.document.add_paragraph()
        paragraph_format = paragraph.paragraph_format
        paragraph_format.left_indent = Twips(0)
        paragraph_format.space_after = Pt(12)
        run = paragraph.add_run('_' * 100)
        run.font.color.rgb = RGBColor(200, 200, 200)
        run.font.size = Pt(8)

    def add_summary(self, summary):
        self.document.add_heading('Professional Summary', level=1)
        self.document.add_paragraph(summary)
    
    def add_experience(self, experiences):
        heading = self.document.add_heading('Work Experience', level=1)
        heading.style = 'CustomHeading'
        
        if self.template_type == "Creative":
            # Two-column layout for experiences
            for exp in experiences:
                table = self.document.add_table(rows=1, cols=2)
                table.allow_autofit = True
                
                # Left column: Dates and Company
                left_cell = table.cell(0, 0)
                left_cell.width = Inches(2)
                p = left_cell.paragraphs[0]
                p.add_run(f"{exp['start']} -\n{exp['end']}").bold = True
                p.add_run(f"\n{exp['company']}")
                
                # Right column: Title and Responsibilities
                right_cell = table.cell(0, 1)
                p = right_cell.paragraphs[0]
                p.add_run(f"{exp['title']}\n").bold = True
                p.add_run(exp['responsibilities'])
                
                self.document.add_paragraph()  # Spacing between experiences
                
        elif self.template_type == "Technical":
            # Code-style format
            for exp in experiences:
                p = self.document.add_paragraph(style='CustomSubheading')
                p.add_run(f"class {exp['company'].replace(' ', '')}_Role {{\n")
                p.add_run(f"    position: {exp['title']};\n")
                p.add_run(f"    period: {exp['start']} -> {exp['end']};\n")
                p.add_run("    responsibilities: {\n")
                for resp in exp['responsibilities'].split('\n'):
                    if resp.strip():
                        p.add_run(f"        • {resp.strip()}\n")
                p.add_run("    }\n}")
                self.document.add_paragraph()
                
        else:
            # Standard format with enhanced styling
            for exp in experiences:
                p = self.document.add_paragraph(style='CustomSubheading')
                p.add_run(f"{exp['company']} ").bold = True
                p.add_run("| ").italic = True
                p.add_run(f"{exp['title']}").bold = True
                
                date_p = self.document.add_paragraph(style='CustomBody')
                date_p.add_run(f"{exp['start']} - {exp['end']}")
                date_p.paragraph_format.left_indent = Inches(0.25)
                
                resp_p = self.document.add_paragraph(style='CustomBody')
                resp_p.add_run(exp['responsibilities'])
                resp_p.paragraph_format.left_indent = Inches(0.25)
                self.document.add_paragraph()

    def add_education(self, education):
        heading = self.document.add_heading('Education', level=1)
        heading.style = 'CustomHeading'
        
        if self.template_type == "Academic":
            # Detailed academic format
            for edu in education:
                p = self.document.add_paragraph(style='CustomSubheading')
                p.add_run(f"{edu['degree']}\n").bold = True
                p.add_run(f"{edu['institution']}").italic = True
                
                date_p = self.document.add_paragraph(style='CustomBody')
                date_p.add_run(f"{edu['start']} - {edu['end']}")
                
                if edu['description']:
                    desc_p = self.document.add_paragraph(style='CustomBody')
                    desc_p.paragraph_format.left_indent = Inches(0.25)
                    desc_p.add_run(edu['description'])
                self.document.add_paragraph()
        else:
            # Standard format with template-specific styling
            for edu in education:
                p = self.document.add_paragraph(style='CustomSubheading')
                p.add_run(f"{edu['institution']} - {edu['degree']}").bold = True
                p.add_run(f"\n{edu['start']} - {edu['end']}")
                if edu['description']:
                    self.document.add_paragraph(
                        edu['description'], 
                        style='CustomBody'
                    ).paragraph_format.left_indent = Inches(0.25)

    def add_skills(self, skills):
        heading = self.document.add_heading('Skills', level=1)
        heading.style = 'CustomHeading'
        
        if self.template_type == "Technical":
            # Code-style skills presentation
            p = self.document.add_paragraph(style='CustomBody')
            p.add_run("const skills = {\n")
            categories = skills.split(',')
            for i, skill in enumerate(categories):
                p.add_run(f'    "{skill.strip()}"' + 
                         (',' if i < len(categories) - 1 else '') + '\n')
            p.add_run("};")
        
        elif self.template_type == "Creative":
            # Grid layout for skills
            skills_list = [s.strip() for s in skills.split(',')]
            table = self.document.add_table(rows=(len(skills_list) + 1) // 2, cols=2)
            table.allow_autofit = True
            
            i = 0
            for row in table.rows:
                for cell in row.cells:
                    if i < len(skills_list):
                        cell.text = f"▪ {skills_list[i]}"
                    i += 1
        
        else:
            # Enhanced bullet-point list
            skills_list = [s.strip() for s in skills.split(',')]
            p = self.document.add_paragraph(style='CustomBody')
            for skill in skills_list:
                p.add_run(f"• {skill}\n")
    
    def generate(self, resume_data):
        self.add_header(resume_data['name'], {
            'email': resume_data['email'],
            'phone': resume_data['phone'],
            'location': resume_data['location'],
            'linkedin': resume_data['linkedin'],
            'portfolio': resume_data.get('portfolio', '')
        })
        self.add_summary(resume_data['summary'])
        self.add_experience(resume_data['experiences'])
        self.add_education(resume_data['education'])
        self.add_skills(resume_data['skills'])
        
        return self.document