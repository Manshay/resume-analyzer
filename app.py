import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title="SmartHire",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Rest of the imports
from streamlit_option_menu import option_menu
import os
from pathlib import Path

# Import modules
from modules.home import show_home
from modules.analyzer import show_analyzer
from modules.builder import show_builder
from modules.dashboard import show_dashboard
from modules.feedback import show_feedback
from modules.admin import (
    show_admin_dashboard,
    show_enhanced_submissions,
    show_enhanced_settings,
    verify_admin,
    logout
)

# Initialize session state
def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'admin_authenticated' not in st.session_state:  # Added this line
        st.session_state.admin_authenticated = False
    if 'user_type' not in st.session_state:
        st.session_state.user_type = "User"
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"

# Load external CSS
def load_css():
    css_path = Path("styles/styles.css")
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("CSS file not found. Some styles might be missing.")

def show_sidebar():
    with st.sidebar:
        # User type selection
        user_type = option_menu(
            "Select User Type",
            ["User", "Admin"],
            default_index=0 if st.session_state.user_type == "User" else 1,
            orientation="horizontal",
            menu_icon="person",
            key="user_type_select"
        )
        
        # Handle user type change
        if user_type != st.session_state.user_type:
            st.session_state.user_type = user_type
            st.session_state.authenticated = False
            st.session_state.admin_authenticated = False  # Reset admin auth on type change
            st.rerun()
        
        # Show appropriate menu based on user type
        if user_type == "User":
            selected = option_menu(
                "User Menu",
                ["Home", "Resume Analyzer", "Resume Builder", "Dashboard", "Feedback"],
                icons=["house", "clipboard-check", "pencil", "bar-chart-line", "chat-square-text"],
                menu_icon="cast",
                default_index=0,
                orientation="vertical"
            )
        else:
            if not st.session_state.admin_authenticated:  # Changed to admin_authenticated
                verify_admin()
                return None
            
            selected = option_menu(
                "Admin Menu",
                ["Home", "Dashboard", "Submissions", "Settings"],
                icons=["house", "bar-chart-line", "file-earmark-check", "gear"],
                menu_icon="cast",
                default_index=0,
                orientation="vertical"
            )
            
            # Add logout button for admin
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True, type="primary"):
                logout()
                st.rerun()
        
        return selected

def main():
    # Initialize session state and load CSS
    init_session_state()
    load_css()
    
    # Show sidebar and get selected option
    selected = show_sidebar()
    
    # Handle page routing
    try:
        if selected:  # Only process if sidebar selection was successful
            if st.session_state.user_type == "User":
                if selected == "Home":
                    show_home()
                elif selected == "Resume Analyzer":
                    show_analyzer()
                elif selected == "Resume Builder":
                    show_builder()
                elif selected == "Dashboard":
                    show_dashboard()
                elif selected == "Feedback":
                    show_feedback()
            
            elif st.session_state.user_type == "Admin" and st.session_state.admin_authenticated:  # Changed to admin_authenticated
                if selected == "Home":
                    show_home()
                elif selected == "Dashboard":
                    show_admin_dashboard()
                elif selected == "Submissions":
                    show_enhanced_submissions()
                elif selected == "Settings":
                    show_enhanced_settings()
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Details: " + str(e.__class__.__name__))
        if st.session_state.user_type == "Admin":
            st.error("Please check the logs for more details")

if __name__ == "__main__":
    main()