from docx2pdf import convert
import streamlit as st
from ai_modules.resume_generator import EnhancedResumeGenerator
import tempfile
import os

def convert_to_pdf(docx_path, pdf_path):
    try:
        convert(docx_path, pdf_path)
        return True
    except Exception as e:
        st.warning("PDF conversion requires Microsoft Word to be installed. Providing DOCX format only.")
        return False

def show_builder():
    st.title("Resume Builder")
    
    # Template selection
    template = st.selectbox(
        "Choose a Template",
        ["Professional", "Creative", "Academic", "Technical"],
        help="Select a template style for your resume"
    )
    
    # Create tabs for different sections with increased spacing
    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Personal Info", "Professional Summary", "Experience", "Education", "Skills"])
    
    with tab1:
        st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
        st.subheader("Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
        with col2:
            location = st.text_input("Location")
            linkedin = st.text_input("LinkedIn URL (optional)")
            portfolio = st.text_input("Portfolio/Website (optional)")
    
    with tab2:
        st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
        st.subheader("Professional Summary")
        summary = st.text_area("Write a brief professional summary (2-3 sentences)")
    
    with tab3:
        st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
        st.subheader("Work Experience")
        st.write("Add your work experience")
        
        # Dynamic form for multiple work experiences
        num_experiences = st.number_input("Number of work experiences", min_value=0, max_value=10, value=1)
        
        experiences = []
        for i in range(num_experiences):
            st.markdown(f"### Experience {i+1}")
            st.markdown('<div class="subsection-spacer"></div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                company = st.text_input(f"Company Name", key=f"company_{i}")
                title = st.text_input(f"Job Title", key=f"title_{i}")
            with col2:
                start_date = st.text_input(f"Start Date (MM/YYYY)", key=f"start_{i}")
                end_date = st.text_input(f"End Date (MM/YYYY or 'Present')", key=f"end_{i}")
            
            responsibilities = st.text_area(f"Key Responsibilities and Achievements", key=f"resp_{i}")
            experiences.append({
                "company": company, 
                "title": title, 
                "start": start_date, 
                "end": end_date, 
                "responsibilities": responsibilities
            })
            st.markdown('<hr class="experience-divider">', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
        st.subheader("Education")
        # Similar dynamic form for education
        num_edu = st.number_input("Number of education entries", min_value=0, max_value=5, value=1)
        
        education = []
        for i in range(num_edu):
            st.markdown(f"### Education {i+1}")
            st.markdown('<div class="subsection-spacer"></div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                institution = st.text_input(f"Institution Name", key=f"edu_name_{i}")
                degree = st.text_input(f"Degree", key=f"edu_{i}")
            with col2:
                edu_start = st.text_input(f"Start Date (MM/YYYY)", key=f"edu_start_{i}")
                edu_end = st.text_input(f"End Date (MM/YYYY or 'Present')", key=f"edu_end_{i}")
            
            description = st.text_area(f"Description (Optional)", key=f"edu_desc_{i}")
            education.append({
                "institution": institution, 
                "degree": degree, 
                "start": edu_start, 
                "end": edu_end, 
                "description": description
            })
            st.markdown('<hr class="education-divider">', unsafe_allow_html=True)
    
    with tab5:
        st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
        st.subheader("Skills")
        skills = st.text_area("List your skills (separated by commas)")
    
    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
    if st.button("Generate Resume"):
        with st.spinner("Generating your resume..."):
            try:
                # Validate inputs
                if not name or not email or not phone or not location:
                    st.error("Please fill in all required personal information fields.")
                    return
                
                # Collect all resume data in correct format
                resume_data = {
                    "personal_info": {
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "location": location,
                        "linkedin": linkedin,
                        "portfolio": portfolio
                    },
                    "summary": summary,
                    "experience": experiences,
                    "education": education,
                    "skills": skills
                }
                
                # Generate resume
                generator = EnhancedResumeGenerator(template)
                success = generator.generate(resume_data)
                
                if not success:
                    st.error("Failed to generate resume. Please check your inputs.")
                    return
                
                # Create temporary directory
                with tempfile.TemporaryDirectory() as tmp_dir:
                    # Save DOCX
                    safe_name = name.replace(' ', '_').replace('/', '_')
                    docx_path = os.path.join(tmp_dir, f"{safe_name}_resume.docx")
                    generator.document.save(docx_path)
                    
                    # Try PDF conversion
                    pdf_path = os.path.join(tmp_dir, f"{safe_name}_resume.pdf")
                    pdf_conversion_success = convert_to_pdf(docx_path, pdf_path)
                    
                    # Read DOCX file
                    with open(docx_path, 'rb') as docx_file:
                        docx_bytes = docx_file.read()
                    
                    # Read PDF if conversion was successful
                    pdf_bytes = None
                    if pdf_conversion_success and os.path.exists(pdf_path):
                        with open(pdf_path, 'rb') as pdf_file:
                            pdf_bytes = pdf_file.read()
                
                st.success("✅ Resume generated successfully!")
                
                # Download buttons
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="⬇️ Download DOCX",
                        data=docx_bytes,
                        file_name=f"{safe_name}_resume.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                
                if pdf_bytes:
                    with col2:
                        st.download_button(
                            label="⬇️ Download PDF",
                            data=pdf_bytes,
                            file_name=f"{safe_name}_resume.pdf",
                            mime="application/pdf"
                        )
                    
                    # Show PDF preview
                    st.subheader("📄 Resume Preview")
                    st.pdf_viewer(pdf_bytes)
                else:
                    st.info("💡 PDF preview not available. Please download the DOCX file to view your resume.")
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                import traceback
                st.error(traceback.format_exc())