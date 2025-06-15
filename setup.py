from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-compliance-checker",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-Powered Enterprise Compliance Checker for GDPR, SOC2, HIPAA, and RBI frameworks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-compliance-checker",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial",
        "Topic :: Security",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.11",
    install_requires=[
        "streamlit>=1.28.0",
        "openai>=1.3.0",
        "pandas>=2.0.0",
        "plotly>=5.17.0",
        "spacy>=3.7.0",
        "PyPDF2>=3.0.0",
        "pdfplumber>=0.9.0",
        "python-docx>=0.8.11",
        "xlsxwriter>=3.1.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "compliance-checker=app:main",
        ],
    },
    keywords="compliance, ai, nlp, gdpr, soc2, hipaa, rbi, enterprise, security, privacy",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ai-compliance-checker/issues",
        "Source": "https://github.com/yourusername/ai-compliance-checker",
        "Documentation": "https://github.com/yourusername/ai-compliance-checker#readme",
    },
)