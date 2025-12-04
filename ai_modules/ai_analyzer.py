import logging
import re
from datetime import datetime
import numpy as np
import PyPDF2
import docx
import spacy
from sklearn.feature_extraction.text import CountVectorizer
import streamlit as st

logger = logging.getLogger(__name__)

class ResumeAnalyzer:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception:
            # fallback: create blank english model if not available
            self.nlp = spacy.blank("en")

    def extract_text(self, uploaded_file):
        """
        Accepts a file-like UploadedFile (Streamlit) and returns extracted text.
        """
        try:
            file_type = getattr(uploaded_file, "type", "")
            # PDF
            if file_type == "application/pdf" or str(uploaded_file.name).lower().endswith(".pdf"):
                reader = PyPDF2.PdfReader(uploaded_file)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            else:
                # DOCX / other
                doc = docx.Document(uploaded_file)
                text = " ".join([p.text for p in doc.paragraphs])
            return text or ""
        except Exception as e:
            logger.exception("Failed to extract text")
            st.error(f"Error extracting text from file: {e}")
            return ""

    def calculate_ats_score(self, resume_text, job_desc):
        if not job_desc:
            return None

        def preprocess_text(text):
            text = re.sub(r"[^\w\s]", " ", (text or "").lower())
            text = " ".join(text.split())
            return text

        try:
            resume_processed = preprocess_text(resume_text)
            job_processed = preprocess_text(job_desc)

            vectorizer = CountVectorizer(
                stop_words="english",
                ngram_range=(1, 2),
                min_df=1,
                binary=True
            )

            matrix = vectorizer.fit_transform([resume_processed, job_processed]).toarray()
            feature_names = vectorizer.get_feature_names_out()

            resume_vector = np.asarray(matrix[0], dtype=int)
            job_vector = np.asarray(matrix[1], dtype=int)

            # boolean matches
            matches = (resume_vector > 0) & (job_vector > 0)
            match_terms = [term for term, match in zip(feature_names, matches) if match]

            total_weight = 0.0
            matched_weight = 0.0

            # Use vocabulary_ map to get indices safely
            vocab = vectorizer.vocabulary_
            for term, idx in vocab.items():
                if idx is None or idx >= len(job_vector):
                    continue
                if job_vector[idx] > 0:
                    weight = 2.0 if len(term.split()) > 1 else 1.0
                    total_weight += weight
                    if resume_vector[idx] > 0:
                        matched_weight += weight

            score = 0.0
            if total_weight > 0:
                score = (matched_weight / total_weight) * 100.0

                # coverage bonus scaled safely
                if len(feature_names) > 0:
                    coverage_bonus = min(10.0, (len(match_terms) / len(feature_names)) * 20.0)
                    score = min(100.0, score + coverage_bonus)

            return int(round(score))
        except Exception as e:
            logger.exception("Error calculating ATS score")
            st.error(f"Error calculating ATS score: {e}")
            return None

    def analyze_format(self, text):
        try:
            text_lower = (text or "").lower()
            sections = ["experience", "education", "skills", "projects"]
            section_score = sum(1 for s in sections if s in text_lower) / len(sections)

            contact_patterns = [
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"
            ]
            contact_score = sum(1 for p in contact_patterns if re.search(p, text, flags=re.IGNORECASE)) / len(contact_patterns)

            final = round(((section_score + contact_score) / 2.0) * 100.0)
            return final
        except Exception as e:
            logger.exception("Error analyzing format")
            st.error(f"Error analyzing format: {e}")
            return 0

    def extract_skills(self, text, job_desc):
        skills_categories = {
            "programming": {
                "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "php",
                "swift", "kotlin", "rust", "golang", "scala", "perl"
            },
            "web": {
                "html", "css", "react", "angular", "vue", "node.js", "django", "flask",
                "spring", "express.js", "jquery", "bootstrap", "sass", "webpack"
            },
            "database": {
                "sql", "mysql", "postgresql", "mongodb", "oracle", "redis", "elasticsearch",
                "dynamodb", "cassandra", "sqlite", "neo4j"
            },
            "cloud": {
                "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "jenkins",
                "circleci", "ansible", "puppet", "chef"
            },
            "ai_ml": {
                "machine learning", "deep learning", "tensorflow", "pytorch", "keras",
                "scikit-learn", "pandas", "numpy", "opencv", "nlp"
            },
            "soft_skills": {
                "leadership", "communication", "teamwork", "problem solving",
                "critical thinking", "time management", "project management"
            }
        }

        try:
            resume_text = (text or "").lower()
            job_text = (job_desc or "").lower()

            results = {
                "by_category": {},
                "matched_skills": set(),
                "missing_skills": set(),
                "additional_skills": set()
            }

            for category, skills in skills_categories.items():
                resume_skills = {s for s in skills if s in resume_text}
                job_skills = {s for s in skills if s in job_text} if job_desc else set()

                matched = resume_skills & job_skills
                missing = job_skills - resume_skills
                additional = resume_skills - job_skills

                results["matched_skills"].update(matched)
                results["missing_skills"].update(missing)
                results["additional_skills"].update(additional)

                score = 100 if not job_skills else int(round((len(matched) / len(job_skills)) * 100))
                results["by_category"][category] = {
                    "matched": sorted(list(matched)),
                    "missing": sorted(list(missing)),
                    "additional": sorted(list(additional)),
                    "score": score
                }

            return {
                "Matched": len(results["matched_skills"]),
                "Missing": len(results["missing_skills"]),
                "Additional": len(results["additional_skills"]),
                "MatchedSkills": sorted(list(results["matched_skills"])),
                "MissingSkills": sorted(list(results["missing_skills"])),
                "AdditionalSkills": sorted(list(results["additional_skills"])),
                "Categories": results["by_category"]
            }
        except Exception as e:
            logger.exception("Error extracting skills")
            st.error(f"Error extracting skills: {e}")
            return {
                "Matched": 0, "Missing": 0, "Additional": 0,
                "MatchedSkills": [], "MissingSkills": [], "AdditionalSkills": [],
                "Categories": {}
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
        if format_score is not None:
            if format_score < 70:
                suggestions.append("🔴 Critical: Improve resume structure with clear section headings")
            elif format_score < 85:
                suggestions.append("🟡 Important: Consider adding missing standard resume sections")

        # Skills Suggestions
        if skills_data and skills_data.get("Missing", 0) > 0:
            missing_skills = skills_data.get("MissingSkills", [])
            if missing_skills:
                suggestions.append(f"🔵 Skills: Consider adding these key skills: {', '.join(missing_skills[:3])}")

        # Category-specific suggestions
        categories = skills_data.get("Categories", {}) if skills_data else {}
        for category, data in categories.items():
            missing_list = data.get("missing") or data.get("missing", []) or data.get("Missing", []) or data.get("missing", [])
            # handle presence of different key casings; fallback to 'missing' stored earlier
            if isinstance(data, dict):
                missing_count = len(data.get("missing", data.get("missing", [])))
                if missing_count > 0:
                    category_name = category.replace("_", " ").title()
                    suggestions.append(f"📌 {category_name}: Missing {missing_count} relevant skills")

        # General Improvement Suggestions
        if not suggestions:
            suggestions.append("✅ Your resume looks good! Consider adding more achievements and metrics")
        else:
            suggestions.append("💡 Tip: Quantify achievements with metrics where possible")

        return suggestions