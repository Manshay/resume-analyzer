import streamlit as st

def show_home():
    st.markdown('<div class="welcome-section">Welcome to SmartHire!</div>', unsafe_allow_html=True)

    # Main container for better responsiveness
    container = st.container()
    
    with container:
        # First row
        row1_col1, row1_col2 = st.columns([1, 1])
        
        with row1_col1:
            st.markdown("""
            <div class="card">
                <i class="fas fa-upload"></i>
                <div class="card-title">Resume Analyzer</div>
                <div class="card-desc">
                    Get a detailed analysis and score of your resume. <br>Upload your resume and let SmartHire's AI-powered system give you insights and suggestions for improvement.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with row1_col2:
            st.markdown("""
            <div class="card">
                <i class="fas fa-pencil-alt"></i>
                <div class="card-title">Resume Builder</div>
                <div class="card-desc">
                    Create a stunning resume effortlessly with SmartHire's intuitive builder. <br>Enter your details, and let the tool generate a polished resume ready for job applications.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Second row
        row2_col1, row2_col2 = st.columns([1, 1])
        
        with row2_col1:
            st.markdown("""
            <div class="card">
                <i class="fas fa-chart-line"></i>
                <div class="card-title">Dashboard</div>
                <div class="card-desc">
                    Stay updated with the latest job trends and insights. <br>The dashboard provides data-driven trends to guide your career decisions and job search.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with row2_col2:
            st.markdown("""
            <div class="card">
                <i class="fas fa-comments"></i>
                <div class="card-title">Feedback</div>
                <div class="card-desc">
                    Share your experience and provide feedback. <br>Your thoughts will help us improve and create better services for job applicants and recruiters.
                </div>
            </div>
            """, unsafe_allow_html=True)