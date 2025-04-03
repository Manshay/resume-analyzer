import streamlit as st
from ai_modules.ai_analyzer import ResumeAnalyzer

def show_analyzer():
    st.title("Resume Analyzer")
    st.write("Upload your resume to get a detailed analysis and score.")
    
    # Stack elements vertically as requested
    job_role = st.text_input("Job Role You're Applying For")
    
    job_desc = st.text_area("Job Description")
    
    st.write("Upload your resume (PDF, DOC, DOCX)")
    uploaded_file = st.file_uploader("Max size: 100MB", type=["pdf", "doc", "docx"], accept_multiple_files=False)
    
    if uploaded_file is not None:
        # Display file info
        file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": f"{uploaded_file.size / 1024:.2f} KB"}
        st.write(file_details)
        
        if st.button("Analyze Resume"):
            with st.spinner("Analyzing your resume..."):
                # Initialize analyzer
                analyzer = ResumeAnalyzer()
                
                # Extract text from resume
                resume_text = analyzer.extract_text(uploaded_file)
                
                # Calculate scores and analyze
                ats_score = analyzer.calculate_ats_score(resume_text, job_desc)
                format_score = analyzer.analyze_format(resume_text)
                skills_data = analyzer.extract_skills(resume_text, job_desc)
                suggestions = analyzer.get_suggestions(ats_score, format_score, skills_data)
                
                st.success("Analysis complete!")
                
                # Create tabs for different analysis aspects
                tab1, tab2, tab3, tab4 = st.tabs(["ATS Score", "Format Analysis", "Skills Match", "Suggestions"])
                
                with tab1:
                    st.subheader("ATS Compatibility Score")
                    st.metric(label="Overall Score", value=f"{ats_score}%")
                    st.write("Score based on keyword matching with job description")
                
                with tab2:
                    st.subheader("Format Analysis")
                    st.metric(label="Format Score", value=f"{format_score}%")
                    st.write("Score based on resume structure and content")
                
                with tab3:
                    st.subheader("Skills Match")
                    st.write("Skills matching with job description:")
                    st.bar_chart(skills_data)
                
                with tab4:
                    st.subheader("Suggestions for Improvement")
                    st.markdown("\n".join([f"- {suggestion}" for suggestion in suggestions]))