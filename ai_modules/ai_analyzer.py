import PyPDF2
import docx
import spacy
from sklearn.feature_extraction.text import CountVectorizer
import re

class ResumeAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
    def extract_text(self, uploaded_file):
        file_type = uploaded_file.type
        if file_type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        else:
            doc = docx.Document(uploaded_file)
            text = " ".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    
    def calculate_ats_score(self, resume_text, job_desc):
        # Calculate keyword matching
        vectorizer = CountVectorizer()
        try:
            matrix = vectorizer.fit_transform([resume_text.lower(), job_desc.lower()])
            matches = matrix[0].toarray()[0] & matrix[1].toarray()[0]
            score = (sum(matches) / len(vectorizer.get_feature_names_out())) * 100
        except:
            score = 70  # Default score if no job description
        return min(round(score), 100)
    
    def analyze_format(self, text):
        # Check for common sections
        sections = ['experience', 'education', 'skills', 'projects']
        section_score = sum([1 for section in sections if section in text.lower()]) / len(sections)
        
        # Check for contact information
        contact_patterns = [r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # email
                          r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b']  # phone
        contact_score = sum([1 for pattern in contact_patterns if re.search(pattern, text)]) / len(contact_patterns)
        
        return round((section_score + contact_score) / 2 * 100)
    
    def extract_skills(self, text, job_desc):
        # Common technical skills
        common_skills = set(['python', 'java', 'javascript', 'sql', 'aws', 'docker', 'react', 'node.js'])
        
        # Extract skills from resume
        resume_skills = set([token.text.lower() for token in self.nlp(text) 
                           if token.text.lower() in common_skills])
        
        # Extract required skills from job description
        job_skills = set([token.text.lower() for token in self.nlp(job_desc) 
                         if token.text.lower() in common_skills]) if job_desc else common_skills
        
        matched = resume_skills.intersection(job_skills)
        missing = job_skills - resume_skills
        additional = resume_skills - job_skills
        
        return {
            'Matched': len(matched),
            'Missing': len(missing),
            'Additional': len(additional)
        }
    
    def get_suggestions(self, ats_score, format_score, skills_data):
        suggestions = []
        
        if ats_score < 80:
            suggestions.append("Add more relevant keywords from the job description")
        if format_score < 85:
            suggestions.append("Improve resume structure with clear section headings")
        if skills_data['Missing'] > 0:
            suggestions.append(f"Add missing skills required for the role")
        
        return suggestions