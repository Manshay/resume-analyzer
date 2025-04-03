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
        if not job_desc:
            return None
            
        # Preprocess text
        def preprocess_text(text):
            # Convert to lowercase and remove special characters
            text = re.sub(r'[^\w\s]', ' ', text.lower())
            # Remove extra whitespace
            text = ' '.join(text.split())
            return text
        
        try:
            # Preprocess both texts
            resume_processed = preprocess_text(resume_text)
            job_processed = preprocess_text(job_desc)
            
            # Initialize vectorizer with better parameters
            vectorizer = CountVectorizer(
                stop_words='english',  # Remove common English words
                ngram_range=(1, 2),    # Consider both single words and bigrams
                min_df=1,              # Include all terms
                binary=True            # Convert counts to binary
            )
            
            # Create document matrix
            matrix = vectorizer.fit_transform([resume_processed, job_processed])
            
            # Get feature names
            feature_names = vectorizer.get_feature_names_out()
            
            # Calculate weighted scores
            resume_vector = matrix[0].toarray()[0]
            job_vector = matrix[1].toarray()[0]
            
            # Find matching terms
            matches = resume_vector & job_vector
            match_terms = [term for term, match in zip(feature_names, matches) if match]
            
            # Calculate weighted score
            total_weight = 0
            matched_weight = 0
            
            for term in feature_names:
                # Assign higher weight to technical skills and important keywords
                weight = 2.0 if len(term.split()) > 1 else 1.0  # Bigrams get higher weight
                idx = vectorizer.vocabulary_.get(term)
                
                if job_vector[idx]:  # If term is in job description
                    total_weight += weight
                    if resume_vector[idx]:  # If term is also in resume
                        matched_weight += weight
            
            # Calculate final score
            if total_weight > 0:
                score = (matched_weight / total_weight) * 100
                
                # Bonus points for good coverage
                coverage_bonus = min(10, (len(match_terms) / len(feature_names)) * 20)
                score = min(100, score + coverage_bonus)
                
                return round(score)
            
            return 0
            
        except Exception as e:
            st.error(f"Error calculating ATS score: {str(e)}")
            return None
    
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
        # Define comprehensive skill categories
        skills_categories = {
            'programming': {
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php',
                'swift', 'kotlin', 'rust', 'golang', 'scala', 'perl'
            },
            'web': {
                'html', 'css', 'react', 'angular', 'vue', 'node.js', 'django', 'flask',
                'spring', 'express.js', 'jquery', 'bootstrap', 'sass', 'webpack'
            },
            'database': {
                'sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'redis', 'elasticsearch',
                'dynamodb', 'cassandra', 'sqlite', 'neo4j'
            },
            'cloud': {
                'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins',
                'circleci', 'ansible', 'puppet', 'chef'
            },
            'ai_ml': {
                'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras',
                'scikit-learn', 'pandas', 'numpy', 'opencv', 'nlp'
            },
            'soft_skills': {
                'leadership', 'communication', 'teamwork', 'problem solving', 
                'critical thinking', 'time management', 'project management'
            }
        }

        try:
            # Process text with spaCy for better token recognition
            doc_resume = self.nlp(text.lower())
            doc_job = self.nlp(job_desc.lower()) if job_desc else None

            results = {
                'by_category': {},
                'matched_skills': set(),
                'missing_skills': set(),
                'additional_skills': set()
            }

            # Analyze skills by category
            for category, skills in skills_categories.items():
                # Find skills in resume
                resume_skills = set()
                for skill in skills:
                    if any(skill in sent.text.lower() for sent in doc_resume.sents):
                        resume_skills.add(skill)

                # Find skills in job description
                job_skills = set()
                if doc_job:
                    for skill in skills:
                        if any(skill in sent.text.lower() for sent in doc_job.sents):
                            job_skills.add(skill)

                # Calculate matches
                matched = resume_skills & job_skills
                missing = job_skills - resume_skills
                additional = resume_skills - job_skills

                # Update overall results
                results['matched_skills'].update(matched)
                results['missing_skills'].update(missing)
                results['additional_skills'].update(additional)

                # Store category results
                results['by_category'][category] = {
                    'matched': list(matched),
                    'missing': list(missing),
                    'additional': list(additional),
                    'score': round((len(matched) / len(job_skills) * 100) if job_skills else 100)
                }

            return {
                'Matched': len(results['matched_skills']),
                'Missing': len(results['missing_skills']),
                'Additional': len(results['additional_skills']),
                'MatchedSkills': sorted(list(results['matched_skills'])),
                'MissingSkills': sorted(list(results['missing_skills'])),
                'AdditionalSkills': sorted(list(results['additional_skills'])),
                'Categories': results['by_category']
            }

        except Exception as e:
            st.error(f"Error extracting skills: {str(e)}")
            return {
                'Matched': 0, 'Missing': 0, 'Additional': 0,
                'MatchedSkills': [], 'MissingSkills': [], 'AdditionalSkills': [],
                'Categories': {}
            }

    def get_suggestions(self, ats_score, format_score, skills_data):
        suggestions = []
        
        # ATS Score Suggestions
        if ats_score is not None:
            if ats_score < 60:
                suggestions.append("🔴 Critical: Your resume needs significant keyword optimization")
            elif ats_score < 80:
                suggestions.append("🟡 Important: Add more relevant keywords from the job description")
            
        # Format Score Suggestions
        if format_score < 70:
            suggestions.append("🔴 Critical: Improve resume structure with clear section headings")
        elif format_score < 85:
            suggestions.append("🟡 Important: Consider adding missing standard resume sections")
        
        # Skills Suggestions
        if skills_data['Missing'] > 0:
            missing_skills = skills_data.get('MissingSkills', [])
            if missing_skills:
                suggestions.append(f"🔵 Skills: Consider adding these key skills: {', '.join(missing_skills[:3])}")
        
        # Category-specific suggestions
        for category, data in skills_data.get('Categories', {}).items():
            if data.get('missing') and len(data['missing']) > 0:
                category_name = category.replace('_', ' ').title()
                suggestions.append(f"📌 {category_name}: Missing {len(data['missing'])} relevant skills")
        
        # General Improvement Suggestions
        if not suggestions:
            suggestions.append("✅ Your resume looks good! Consider adding more achievements and metrics")
        else:
            suggestions.append("💡 Tip: Quantify achievements with metrics where possible")
        
        return suggestions