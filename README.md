# AI-Powered Resume Analyzer

An intelligent resume analysis and management system built with Streamlit that helps both job seekers and recruiters streamline the resume review process.

## 🌟 Features

- **Resume Analysis**: AI-powered resume parsing and evaluation
- **Resume Builder**: Interactive resume creation tool
- **Job Market Dashboard**: Real-time job market insights
- **Admin Panel**: Comprehensive management dashboard
- **User Management**: Track and manage user accounts
- **Analytics**: Detailed analytics and reporting

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/resume-analyzer.git
cd resume-analyzer
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## 💻 Usage

1. Run the application:
```bash
streamlit run app.py
```

2. Access the application in your web browser at:
```
http://localhost:8501
```

## 📁 Project Structure

```
resume-analyzer/
├── app.py              # Main application file
├── modules/            # Application modules
│   ├── admin.py       # Admin dashboard functionality
│   ├── analyzer.py    # Resume analysis logic
│   ├── builder.py     # Resume builder functionality
│   ├── dashboard.py   # Job market dashboard
│   ├── feedback.py    # User feedback system
│   └── home.py        # Homepage functionality
├── styles/            # CSS styling
│   └── styles.css     # Custom CSS
├── config/            # Configuration files
├── requirements.txt   # Project dependencies
└── README.md         # Project documentation
```

## 👥 User Types

### Regular Users
- Upload and analyze resumes
- Build professional resumes
- View job market insights
- Provide feedback

### Administrators
- Access admin dashboard
- Manage user accounts
- View analytics
- Configure system settings
- Monitor submissions

## 🔒 Security

Default admin credentials:
- Username: `admin`
- Password: `password`

**Note**: Change these credentials in a production environment.

## 🛠️ Configuration

System settings can be configured through the admin panel, including:
- Email settings
- API configurations
- Storage settings
- Security parameters

## 📊 Analytics

The admin dashboard provides:
- User activity metrics
- System performance stats
- Resume submission analytics
- Resource utilization graphs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Uses [Plotly](https://plotly.com/) for visualizations
- Powered by various open-source libraries

## ✨ Support

For support, please open an issue in the GitHub repository or contact the maintainers.