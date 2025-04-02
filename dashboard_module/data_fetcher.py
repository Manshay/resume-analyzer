import requests
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobDataAPI:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('JSEARCH_API_KEY')
        if not self.api_key:
            raise ValueError("JSEARCH_API_KEY not found in .env file")
        
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
        self.base_url = "https://jsearch.p.rapidapi.com"
    
    def analyze_market(self, query: str, location: str = None) -> dict:
        try:
            jobs_data = self._fetch_jobs(query, location)
            if not jobs_data:
                return self._default_analysis()
            
            job_types_analysis = self._analyze_job_types(jobs_data)
            
            return {
                "market_overview": self._analyze_market_overview(jobs_data),
                "skills_demand": self._analyze_skills_demand(jobs_data),
                "salary_insights": self._analyze_salary_data(jobs_data),
                "job_types": job_types_analysis  # This contains employment_types and work_location
            }
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return self._default_analysis()
    
    def _fetch_jobs(self, query: str, location: str) -> list:
        try:
            search_query = f"{query}"
            if location.lower() != "remote":
                search_query += f" in {location}"
            
            params = {
                "query": search_query,
                "page": "1",
                "num_pages": "1",
                "date_posted": "today",  # Get recent postings
                "remote_jobs_only": "true" if location.lower() == "remote" else "false"
            }
            
            response = requests.get(
                f"{self.base_url}/search",
                headers=self.headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            # Debug logging
            print(f"API Query: {search_query}")
            print(f"Total results: {len(data.get('data', []))}")
            
            return data.get('data', [])
        except Exception as e:
            print(f"API request failed: {e}")
            return []
    
    def _analyze_market_overview(self, jobs: list) -> dict:
        total_jobs = len(jobs)
        recent_jobs = len([j for j in jobs if self._is_recent(j.get('job_posted_at_datetime_utc', ''))])
        remote_jobs = len([j for j in jobs if j.get('remote_jobs_url')])
        
        return {
            "total_jobs": total_jobs,
            "recent_jobs": recent_jobs,
            "remote_jobs": remote_jobs,
            "hiring_companies": len(set(j.get('employer_name', '') for j in jobs))
        }
    
    def _analyze_skills_demand(self, jobs: list) -> dict:
        skills_count = {}
        for job in jobs:
            description = job.get('job_description', '').lower()
            found_skills = self._extract_skills(description)
            for skill in found_skills:
                skills_count[skill] = skills_count.get(skill, 0) + 1
        
        return dict(sorted(skills_count.items(), key=lambda x: x[1], reverse=True)[:10])
    
    def _analyze_salary_data(self, jobs: list) -> dict:
        salaries = []
        for job in jobs:
            # Extract salary info from JSearch API response
            if job.get('job_max_salary') and job.get('job_min_salary'):
                avg_salary = (float(job['job_max_salary']) + float(job['job_min_salary'])) / 2
                salaries.append(avg_salary)
            elif job.get('job_max_salary'):
                salaries.append(float(job['job_max_salary']))
            elif job.get('job_min_salary'):
                salaries.append(float(job['job_min_salary']))
        
        if not salaries:
            return {"average": 0, "range": {"min": 0, "max": 0}}
            
        return {
            "average": sum(salaries) / len(salaries),
            "range": {
                "min": min(salaries),
                "max": max(salaries)
            }
        }
    
    def _analyze_job_types(self, jobs: list) -> dict:
        # Initialize counters
        types = {
            'Full-time': 0,
            'Part-time': 0,
            'Contract': 0,
            'Internship': 0,
            'Permanent': 0,
            'Freelance': 0,
            'Other': 0
        }
        
        work_location = {
            'remote': 0,
            'hybrid': 0,
            'onsite': 0
        }
        
        total_jobs = len(jobs)
        
        for job in jobs:
            # Employment Type Analysis
            job_type = job.get('job_employment_type', '').upper()
            job_desc = job.get('job_description', '').lower()
            
            # Categorize job type
            if 'FULL' in job_type or 'FT' in job_type:
                types['Full-time'] += 1
            elif 'PART' in job_type or 'PT' in job_type:
                types['Part-time'] += 1
            elif 'CONTRACT' in job_type or 'TEMP' in job_type:
                types['Contract'] += 1
            elif 'INTERN' in job_type:
                types['Internship'] += 1
            elif 'PERMANENT' in job_type:
                types['Permanent'] += 1
            elif 'FREELANCE' in job_type:
                types['Freelance'] += 1
            else:
                types['Other'] += 1
            
            # Work Location Analysis
            if 'remote' in job_desc or job.get('remote_jobs_url'):
                work_location['remote'] += 1
            elif 'hybrid' in job_desc:
                work_location['hybrid'] += 1
            else:
                work_location['onsite'] += 1
        
        # Remove empty categories
        types = {k: v for k, v in types.items() if v > 0}
        work_location = {k: v for k, v in work_location.items() if v > 0}
        
        return {
            'employment_types': types,
            'work_location': work_location,
            'total_jobs': total_jobs,
            'analysis_date': datetime.now().strftime('%Y-%m-%d')
        }
    
    def _extract_skills(self, text: str) -> list:
        skills = [
            'python', 'java', 'javascript', 'sql', 'aws', 'azure',
            'react', 'node.js', 'docker', 'kubernetes', 'machine learning',
            'ai', 'data science', 'cloud', 'devops', 'git'
        ]
        return [skill for skill in skills if skill in text]
    
    def _is_recent(self, date_str: str) -> bool:
        if not date_str:
            return False
        try:
            posted_date = datetime.strptime(date_str[:10], '%Y-%m-%d')
            return (datetime.now() - posted_date).days <= 7
        except:
            return False
    
    def _default_analysis(self) -> dict:
        return {
            "market_overview": {
                "total_jobs": 0,
                "recent_jobs": 0,
                "remote_jobs": 0,
                "hiring_companies": 0
            },
            "skills_demand": {},
            "salary_insights": {
                "average": 0,
                "range": {"min": 0, "max": 0}
            },
            "job_types": {
                "employment_types": {"Other": 0},
                "work_location": {
                    "remote": 0,
                    "hybrid": 0,
                    "onsite": 0
                },
                "total_jobs": 0,
                "analysis_date": datetime.now().strftime('%Y-%m-%d')
            }
        }
    
    def verify_api_connection(self):
        try:
            test_response = requests.get(
                f"{self.base_url}/search",
                headers=self.headers,
                params={"query": "python developer", "page": "1", "num_pages": "1"},
                timeout=10
            )
            test_response.raise_for_status()
            data = test_response.json()
            if data.get('data'):
                logger.info("API connection successful!")
                logger.info(f"Sample job: {data['data'][0]}")
                return True
            return False
        except Exception as e:
            logger.error(f"API connection failed: {e}")
            return False