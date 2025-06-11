# SmartHire: AI-Enhanced Resume Analysis System 📄

## 📌 Overview
SmartHire is a comprehensive web application that combines resume analysis, building, and management capabilities with AI-powered insights. Built using Python and Streamlit, it offers both user and admin interfaces for a complete resume management solution.

## ✨ Features

### For Users
- **Resume Analysis** 📊
  - AI-powered resume scanning
  - Keyword matching
  - Skills assessment
  - ATS compatibility check

- **Resume Builder** 📝
  - Multiple professional templates
  - Real-time preview
  - Export to PDF/DOCX

- **Personal Dashboard** 📈
  - Track submissions
  - View analytics
  - Progress monitoring

### For Admins
- **Admin Dashboard** 🎛️
  - User management
  - System analytics
  - Performance metrics

## 🛠️ Technology Stack
- Python 3.12
- Streamlit
- Python-docx
- AI/ML Libraries

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Manshay/resume-analyzer.git

# Navigate to project directory
cd resume-analyzer

# Create virtual environment
python -m venv venv

# Activate virtual environment
# For Windows:
venv\Scripts\activate
# For Unix/MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 📂 Project Structure
```
resume-analyzer/
├── ai_modules/
│   ├── ai_analyzer.py
│   └── resume_generator.py
├── modules/
│   ├── analyzer.py
│   ├── builder.py
│   ├── dashboard.py
│   └── feedback.py
├── styles/
│   └── styles.css
├── assets/
│   └── images/
├── app.py
├── requirements.txt
└── README.md
```

## 👥 User Types
1. **Regular Users**
   - Resume analysis
   - Resume building
   - Progress tracking

2. **Administrators**
   - System management
   - User oversight
   - Analytics review

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.