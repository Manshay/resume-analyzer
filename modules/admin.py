import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
import time
import json

# Add to top of file with other exports
__all__ = [
    'show_admin_dashboard',
    'show_enhanced_submissions',
    'show_enhanced_settings',
    'verify_admin',
    'logout'
]

# Constants
DANGER_COLOR = "#FF4B4B"
SUCCESS_COLOR = "#00CC96"
WARNING_COLOR = "#FFA500"

def init_session_state():
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Overview"
    if 'settings' not in st.session_state:
        st.session_state.settings = load_settings()

def load_settings():
    try:
        with open('config/admin_settings.json', 'r') as f:
            return json.load(f)
    except:
        return get_default_settings()

def get_default_settings():
    return {
        "security": {
            "auth_method": "Local",
            "session_timeout": 30,
            "password_expiry": 90
        },
        "email": {
            "smtp_server": "",
            "smtp_port": "",
            "username": "",
            "password": ""
        },
        "api": {
            "openai_key": "",
            "model": "GPT-3.5-turbo",
            "rate_limit": 60
        }
    }

def logout():
    st.session_state.admin_authenticated = False
    st.rerun()

def verify_admin():
    if st.session_state.admin_authenticated:
        return True
        
    st.subheader("Admin Login")
    with st.form("admin_login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            if username == "admin" and password == "password":
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Invalid credentials")
    return False

def show_admin_dashboard():
    init_session_state()
    
    if not verify_admin():
        return

    # Enhanced sidebar with custom CSS
    with st.sidebar:
        st.markdown("""
        <style>
        .sidebar-title {
            text-align: center;
            padding: 15px;
            background-color: #262730;  /* Dark background to match Streamlit's theme */
            color: #ffffff;  /* White text */
            border-radius: 5px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-title">👨‍💼 Admin Panel</div>', unsafe_allow_html=True)
        
        selected = st.radio(
            "",
            ["📊 Overview", "👥 Users", "📑 Submissions", "📈 Analytics", "⚙️ Settings"],
            key="admin_nav_radio"  # Added unique key
        )
        
        # System status indicators
        st.markdown("---")
        st.markdown("### System Status")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("🟢 API: Online")
            st.markdown("🟢 DB: Connected")
        with col2:
            st.markdown("🟡 Cache: 82%")
            st.markdown("🟢 Queue: Ready")
        
        # Logout button with unique key
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True, type="primary", key="admin_logout_btn"):
            logout()

    # Main content with keys for each section
    if "Overview" in selected:
        show_enhanced_overview()
    elif "Users" in selected:
        show_enhanced_users()
    elif "Submissions" in selected:
        show_enhanced_submissions()
    elif "Analytics" in selected:
        show_enhanced_analytics()
    elif "Settings" in selected:
        show_enhanced_settings()

def show_enhanced_overview():
    st.title("Dashboard Overview")
    
    st.markdown("""
    <style>
    .metric-card {
        background-color: #262730;  /* Dark background */
        color: #ffffff;  /* White text */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .metric-card h3 {
        color: #ffffff;
        font-size: 1rem;
        margin-bottom: 10px;
    }
    .metric-card h2 {
        color: #00acee;  /* Light blue for values */
        font-size: 1.8rem;
        margin: 5px 0;
    }
    .metric-card p {
        color: #00cc96;  /* Green for positive metrics */
        font-size: 1rem;
        margin-top: 5px;
    }
    .metric-card p.negative {
        color: #ff4b4b;  /* Red for negative metrics */
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("Total Users", "1,245", "+12%", "👥"),
        ("Active Today", "156", "+8%", "🔵"),
        ("Resumes Analyzed", "876", "+15%", "📄"),
        ("System Health", "98%", "-2%", "💻")
    ]
    
    for col, (label, value, delta, emoji) in zip([col1, col2, col3, col4], metrics):
        is_negative = '-' in delta
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{emoji} {label}</h3>
                <h2>{value}</h2>
                <p class="{'negative' if is_negative else ''}">{delta}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Activity Graphs
    col1, col2 = st.columns(2)
    
    with col1:
        show_activity_graph()
    
    with col2:
        show_resource_usage()
    
    # Recent Activities
    st.markdown("### Recent Activities")
    show_activity_feed()

def show_activity_graph():
    st.subheader("User Activity")
    dates = pd.date_range(start='2024-01-01', end='2024-04-01', freq='D')
    data = pd.DataFrame({
        'Date': dates,
        'Users': np.random.randint(100, 200, size=len(dates)),
        'Analyses': np.random.randint(50, 150, size=len(dates))
    })
    
    fig = px.line(data, x='Date', y=['Users', 'Analyses'],
                  title='Platform Activity')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def show_resource_usage():
    st.subheader("Resource Usage")
    resources = pd.DataFrame({
        'Resource': ['CPU', 'Memory', 'Storage', 'Bandwidth'],
        'Usage': [65, 78, 45, 82]
    })
    
    fig = px.bar(resources, x='Resource', y='Usage',
                 title='System Resources (%)')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def show_activity_feed():
    activities = [
        {"time": "2 mins ago", "event": "New user registration", "type": "user"},
        {"time": "5 mins ago", "event": "Resume analysis completed", "type": "analysis"},
        {"time": "10 mins ago", "event": "System backup completed", "type": "system"},
        {"time": "15 mins ago", "event": "API rate limit warning", "type": "warning"}
    ]
    
    for activity in activities:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.text(activity["time"])
        with col2:
            if activity["type"] == "warning":
                st.warning(activity["event"])
            else:
                st.info(activity["event"])

def show_enhanced_submissions():
    st.title("Resume Submissions")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Pending", "Analyzed", "Flagged"]
        )
    with col2:
        date_range = st.date_input(
            "Date Range",
            value=(datetime.now() - timedelta(days=7), datetime.now())
        )
    with col3:
        search = st.text_input("Search", placeholder="Search by name or ID...")

    # Sample data
    submissions = pd.DataFrame({
        'ID': range(1, 10),
        'Name': ['John Doe', 'Jane Smith', 'Bob Wilson', 'Alice Brown', 
                'Charlie Davis', 'Eva White', 'Frank Miller', 'Grace Lee', 'Henry Ford'],
        'Submission Date': pd.date_range(end=datetime.now(), periods=9).strftime('%Y-%m-%d').tolist(),
        'Status': ['Analyzed', 'Pending', 'Analyzed', 'Flagged', 
                  'Pending', 'Analyzed', 'Pending', 'Flagged', 'Analyzed'],
        'Score': [85, None, 92, 45, None, 78, None, 35, 88],
        'Type': ['Tech', 'Marketing', 'Tech', 'Sales', 'Tech', 
                'Marketing', 'Sales', 'Tech', 'Marketing']
    })
    
    # Apply filters
    if status_filter != "All":
        submissions = submissions[submissions['Status'] == status_filter]
    if search:
        submissions = submissions[submissions['Name'].str.contains(search, case=False)]
    
    # Style the dataframe
    def color_status(val):
        if val == 'Flagged':
            return f'background-color: {DANGER_COLOR}; color: white'
        elif val == 'Analyzed':
            return f'background-color: {SUCCESS_COLOR}; color: white'
        return ''
    
    styled_df = submissions.style.applymap(color_status, subset=['Status'])
    
    # Display submissions table
    st.dataframe(styled_df, use_container_width=True)
    
    # Submission Stats
    st.markdown("### Submission Statistics")
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric("Total Submissions", len(submissions))
    with stat_col2:
        st.metric("Pending Review", len(submissions[submissions['Status'] == 'Pending']))
    with stat_col3:
        st.metric("Analyzed", len(submissions[submissions['Status'] == 'Analyzed']))
    with stat_col4:
        st.metric("Flagged", len(submissions[submissions['Status'] == 'Flagged']))
    
    # Detailed View
    st.markdown("### Detailed Analysis")
    selected_submission = st.selectbox(
        "Select Submission to Review",
        submissions['ID'].tolist(),
        format_func=lambda x: f"ID: {x} - {submissions[submissions['ID']==x]['Name'].iloc[0]}"
    )
    
    if selected_submission:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### Resume Content")
            st.code("""
            JOHN DOE
            Software Engineer
            
            EXPERIENCE
            Senior Developer, Tech Corp
            - Led team of 5 developers
            - Implemented CI/CD pipeline
            
            SKILLS
            Python, JavaScript, AWS
            """, language="text")
            
        with col2:
            st.markdown("#### Analysis Results")
            score = submissions[submissions['ID']==selected_submission]['Score'].iloc[0]
            if score:
                st.progress(score/100)
                st.markdown(f"**Match Score**: {score}%")
            
            status = st.selectbox(
                "Update Status",
                ["Pending", "Analyzed", "Flagged"],
                index=["Pending", "Analyzed", "Flagged"].index(
                    submissions[submissions['ID']==selected_submission]['Status'].iloc[0]
                ),
                key=f"status_{selected_submission}"
            )
            
            if st.button("Update Status", type="primary", key=f"update_status_{selected_submission}"):
                st.success(f"Status updated to {status}")
                
            with st.expander("Add Review Note"):
                st.text_area("Note", key=f"note_{selected_submission}")
                st.button("Save Note", key=f"save_note_{selected_submission}")

def show_enhanced_users():
    st.title("User Management")
    
    # User Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        role_filter = st.selectbox(
            "Filter by Role",
            ["All", "Free", "Premium", "Enterprise"]
        )
    with col2:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Active", "Inactive", "Suspended"]
        )
    with col3:
        search = st.text_input("Search Users")
    
    # Sample user data
    users = pd.DataFrame({
        'ID': range(1, 8),
        'Name': ['John Doe', 'Jane Smith', 'Bob Wilson', 'Alice Brown', 
                'Charlie Davis', 'Eva White', 'Frank Miller'],
        'Role': ['Premium', 'Free', 'Enterprise', 'Free', 
                'Premium', 'Enterprise', 'Free'],
        'Status': ['Active', 'Active', 'Inactive', 'Active', 
                  'Suspended', 'Active', 'Active'],
        'Join Date': pd.date_range(end=datetime.now(), periods=7).strftime('%Y-%m-%d').tolist(),
        'Last Active': pd.date_range(end=datetime.now(), periods=7).strftime('%Y-%m-%d').tolist()
    })
    
    # Display users
    st.dataframe(users, use_container_width=True)
    
    # User Actions
    st.markdown("### User Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Add New User")
        with st.form("new_user"):
            st.text_input("Name", key="new_user_name")
            st.selectbox("Role", ["Free", "Premium", "Enterprise"], key="new_user_role")
            st.text_input("Email", key="new_user_email")
            st.form_submit_button("Add User")
    
    with col2:
        st.markdown("#### Bulk Actions")
        st.multiselect("Select Users", users['Name'].tolist(), key="bulk_users")
        col1, col2 = st.columns(2)
        with col1:
            st.button("Update Role", key="btn_update_role")
        with col2:
            st.button("Deactivate", type="secondary", key="btn_deactivate")

def show_enhanced_analytics():
    st.title("Analytics Dashboard")
    
    # Time period selector
    period = st.selectbox(
        "Time Period",
        ["Last 7 days", "Last 30 days", "Last 90 days", "Custom Range"]
    )
    
    if period == "Custom Range":
        date_range = st.date_input(
            "Select Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now())
        )
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Revenue", "$12,450", "+8.2%")
    with col2:
        st.metric("Active Users", "1,245", "+12.3%")
    with col3:
        st.metric("Premium Conv.", "15.2%", "+2.1%")
    with col4:
        st.metric("Avg. Usage", "25 mins", "+5.3%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### User Growth")
        dates = pd.date_range(start='2024-01-01', end='2024-04-01', freq='D')
        growth_data = pd.DataFrame({
            'Date': dates,
            'Total Users': np.cumsum(np.random.randint(5, 15, size=len(dates))),
            'Premium Users': np.cumsum(np.random.randint(1, 5, size=len(dates)))
        })
        fig = px.line(growth_data, x='Date', y=['Total Users', 'Premium Users'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Usage Distribution")
        usage_data = pd.DataFrame({
            'Feature': ['Resume Analysis', 'Job Search', 'Skills Assessment', 'Resume Builder'],
            'Usage': [45, 30, 15, 10]
        })
        fig = px.pie(usage_data, values='Usage', names='Feature')
        st.plotly_chart(fig, use_container_width=True)

def show_enhanced_settings():
    st.title("Admin Settings")
    
    tabs = st.tabs(["General", "Security", "Email", "API", "Backup"])
    
    with tabs[0]:
        st.markdown("### General Settings")
        st.number_input("Session Timeout (minutes)", value=30, key="timeout")
        st.number_input("Max File Size (MB)", value=10, key="max_file_size")
        st.checkbox("Enable Debug Mode", key="debug_mode")
    
    with tabs[1]:
        st.markdown("### Security Settings")
        st.text_input("Admin Username", key="admin_username")
        st.text_input("New Password", type="password", key="new_password")
        st.text_input("Confirm Password", type="password", key="confirm_password")
        st.selectbox("Authentication Method", ["Local", "OAuth", "LDAP"], key="auth_method")
    
    with tabs[2]:
        st.markdown("### Email Configuration")
        st.text_input("SMTP Server")
        st.text_input("SMTP Port")
        st.text_input("Username")
        st.text_input("Password", type="password")
        st.checkbox("Enable Email Notifications")
    
    with tabs[3]:
        st.markdown("### API Settings")
        st.text_input("OpenAI API Key", type="password")
        st.selectbox("AI Model", ["GPT-4", "GPT-3.5-turbo"])
        st.number_input("Rate Limit (requests/min)", value=60)
    
    with tabs[4]:
        st.markdown("### Backup Settings")
        st.selectbox("Backup Frequency", ["Daily", "Weekly", "Monthly"])
        st.text_input("Backup Location")
        st.number_input("Retain Backups (days)", value=30)
    
    if st.button("Save Settings", type="primary", use_container_width=True, key="save_settings"):
        st.success("Settings saved successfully!")
        st.balloons()