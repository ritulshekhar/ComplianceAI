# Dependencies

## Required Python Packages

Install these packages using pip:

```bash
pip install streamlit>=1.28.0
pip install openai>=1.3.0
pip install pandas>=2.0.0
pip install plotly>=5.17.0
pip install spacy>=3.7.0
pip install PyPDF2>=3.0.0
pip install pdfplumber>=0.9.0
pip install python-docx>=0.8.11
pip install xlsxwriter>=3.1.0
pip install python-dotenv>=1.0.0
```

## Alternative: Install all at once

```bash
pip install streamlit>=1.28.0 openai>=1.3.0 pandas>=2.0.0 plotly>=5.17.0 spacy>=3.7.0 PyPDF2>=3.0.0 pdfplumber>=0.9.0 python-docx>=0.8.11 xlsxwriter>=3.1.0 python-dotenv>=1.0.0
```

## Optional: Enhanced PII Detection

For better PII detection, install spaCy language model:

```bash
python -m spacy download en_core_web_sm
```

## Environment Setup

Create a `.env` file in your project root:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## System Requirements

- Python 3.11 or higher
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space
- Internet connection for OpenAI API calls

## Development Dependencies (Optional)

For development and testing:

```bash
pip install pytest>=7.0.0
pip install black>=23.0.0
pip install isort>=5.12.0
pip install mypy>=1.0.0
pip install flake8>=6.0.0
```