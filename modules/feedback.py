import streamlit as st

def show_feedback():
    st.title("Feedback")
    
    # Add custom CSS for button centering
    st.markdown("""
        <style>
        div.stButton > button {
            display: block;
            margin: 0 auto;
            width: 200px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.write("We value your feedback! Please let us know how we can improve SmartHire.")
    
    feedback_type = st.selectbox("What would you like to give feedback on?", 
    ["Resume Analyzer", "Resume Builder", "Dashboard", "Overall Experience", "Other"])
    
    rating = st.slider("How would you rate your experience?", 1, 5, 3)
    
    feedback_text = st.text_area("Please share your thoughts or suggestions:")
    
    # Remove columns and use centered button
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback! We appreciate your input.")