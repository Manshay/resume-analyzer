import streamlit as st
from dashboard_module.data_fetcher import JobDataAPI
import plotly.express as px
import pandas as pd

@st.cache_data(ttl=1800)
def fetch_market_data(query: str, location: str) -> dict:
    api = JobDataAPI()
    # Format query to match JSearch API expectations
    formatted_query = query.lower().replace(" ", "-")
    if location.lower() == "remote":
        formatted_location = "remote"
    else:
        formatted_location = location
    
    # Add debug logging
    st.write(f"Fetching data for: {formatted_query} in {formatted_location}")
    
    data = api.analyze_market(formatted_query, formatted_location)
    
    # Debug API response
    if data["market_overview"]["total_jobs"] == 0:
        st.warning("No jobs found. Checking API response...")
        raw_data = api._fetch_jobs(formatted_query, formatted_location)
        st.write("API Response Sample:", raw_data[:2] if raw_data else "No data")
    
    return data

def show_dashboard():
    st.title("Job Market Insights Dashboard")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        job_role = st.selectbox(
            "Job Role",
            ["Software Engineer", "Data Scientist", "DevOps Engineer", 
             "Full Stack Developer", "Machine Learning Engineer"]
        )
    with col2:
        location = st.selectbox(
            "Location",
            ["United States", "Remote", "Europe", "Asia"]
        )
    
    try:
        with st.spinner("Analyzing job market..."):
            market_data = fetch_market_data(job_role, location)
        
        # Market Overview
        st.header("Market Overview")
        overview = market_data["market_overview"]
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Jobs", overview["total_jobs"])
        with col2:
            st.metric("Recent Postings", overview["recent_jobs"])
        with col3:
            st.metric("Remote Jobs", overview["remote_jobs"])
        with col4:
            st.metric("Hiring Companies", overview["hiring_companies"])
        
        # Skills Demand
        st.header("Skills in Demand")
        if market_data["skills_demand"]:
            skills_df = pd.DataFrame(
                market_data["skills_demand"].items(),
                columns=["Skill", "Demand"]
            )
            fig = px.bar(skills_df, x="Skill", y="Demand",
                        title="Most Requested Skills")
            st.plotly_chart(fig)
        else:
            st.info("No skills data available")
        
        # Salary Insights
        st.header("Salary Insights")
        salary_data = market_data["salary_insights"]
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average Salary", f"${salary_data['average']:,.0f}")
        with col2:
            st.metric("Salary Range", 
                     f"${salary_data['range']['min']:,.0f} - ${salary_data['range']['max']:,.0f}")
        
        # Employment Analysis
        st.header("Employment Analysis")
        col1, col2 = st.columns(2)
        
        # Remove duplicate job types visualization and use only the detailed analysis
        job_types = market_data["job_types"]
        total_jobs = overview["total_jobs"]  # Use total_jobs from market_overview
        
        with col1:
            st.subheader("Employment Types")
            if job_types.get("employment_types"):
                emp_types_df = pd.DataFrame(
                    list(job_types["employment_types"].items()),
                    columns=["Type", "Count"]
                ).sort_values("Count", ascending=False)
                
                fig1 = px.pie(
                    emp_types_df,
                    values="Count",
                    names="Type",
                    title=f"Employment Types Distribution"
                )
                st.plotly_chart(fig1)
                
                # Show percentages
                st.markdown("#### Distribution")
                for job_type, count in job_types["employment_types"].items():
                    percentage = round((count / total_jobs) * 100, 1) if total_jobs > 0 else 0
                    st.write(f"- {job_type}: {count} ({percentage}%)")
            else:
                st.info("No employment type data available")
        
        with col2:
            st.subheader("Work Location")
            if job_types.get("work_location"):
                work_loc_df = pd.DataFrame(
                    list(job_types["work_location"].items()),
                    columns=["Location", "Count"]
                )
                fig2 = px.pie(
                    work_loc_df,
                    values="Count",
                    names="Location",
                    title="Work Location Distribution"
                )
                st.plotly_chart(fig2)
                
                # Show percentages
                st.markdown("#### Distribution")
                for location_type, count in job_types["work_location"].items():
                    percentage = round((count / total_jobs) * 100, 1) if total_jobs > 0 else 0
                    st.write(f"- {location_type.title()}: {count} ({percentage}%)")
            else:
                st.info("No work location data available")
                
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
        st.info("Please check your API credentials and try again.")
        # Add debug information
        st.write("Debug Info:", str(e.__class__.__name__))

if __name__ == "__main__":
    show_dashboard()