# AI-Powered Enterprise Compliance Checker

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/openai-gpt--4o-green.svg)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/yourusername/ai-compliance-checker.svg?style=social&label=Star)](https://github.com/yourusername/ai-compliance-checker)

🛡️ **Detect regulatory violations across GDPR, SOC2, HIPAA, and RBI frameworks using advanced AI and NLP**

## Overview

This application helps enterprises automatically detect compliance violations in documents, emails, and forms. It uses OpenAI's GPT-4o and advanced Natural Language Processing to identify non-compliant phrases, missing disclosures, and data misuse across major regulatory frameworks.

## Features

### 🔍 **Multi-Framework Compliance Detection**
- **GDPR**: Data protection, consent mechanisms, subject rights
- **SOC2**: Security controls, availability, processing integrity
- **HIPAA**: Protected health information (PHI) privacy and security
- **RBI**: Financial data localization, cybersecurity frameworks

### 🧠 **AI-Powered Analysis**
- Context-aware violation detection using GPT-4o
- Intelligent risk assessment and recommendations
- Comprehensive compliance scoring

### 🔐 **PII Detection**
- Named Entity Recognition using spaCy
- Pattern-based detection for sensitive data
- Support for emails, SSNs, credit cards, phone numbers, and more

### 📄 **Document Processing**
- Support for PDF, DOCX, and TXT files
- Advanced text extraction and cleaning
- Intelligent document section analysis

### 📊 **Comprehensive Reporting**
- Interactive dashboard with visualizations
- Export to PDF, Excel, and JSON formats
- Detailed violation breakdowns and recommendations

## Tech Stack

- **Frontend**: Streamlit
- **AI/ML**: OpenAI GPT-4o, spaCy NLP
- **Document Processing**: PyPDF2, pdfplumber, python-docx
- **Data Visualization**: Plotly, Pandas
- **Reporting**: XlsxWriter

## Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-compliance-checker.git
   cd ai-compliance-checker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download spaCy model (optional, for enhanced PII detection)**
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the app**
   Open your browser and go to `http://localhost:8501`

## Usage

### 1. Configure Analysis Settings
- Select compliance frameworks (GDPR, SOC2, HIPAA, RBI)
- Choose detection sensitivity level
- Enable/disable PII detection and AI analysis

### 2. Upload Document
- Support formats: PDF, DOCX, TXT
- Maximum file size: 200MB

### 3. Review Results
- View compliance summary and scores
- Analyze violations by framework and severity
- Examine detected PII entities
- Read AI-generated insights and recommendations

### 4. Export Reports
- Download comprehensive PDF reports
- Export detailed Excel spreadsheets
- Generate JSON data for integration

## Project Structure

```
ai-compliance-checker/
├── app.py                      # Main Streamlit application
├── compliance_checker.py      # Core compliance analysis engine
├── compliance_frameworks.py   # Framework-specific rules and patterns
├── document_processor.py      # Document parsing and text extraction
├── pii_detector.py            # PII detection using NLP and patterns
├── report_generator.py        # Report generation in multiple formats
├── utils.py                   # Utility functions and helpers
├── requirements.txt           # Python dependencies
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── README.md                  # Project documentation
└── .gitignore                 # Git ignore rules
```

## Configuration

### Streamlit Configuration
The app is configured to run on all interfaces at port 8501. Modify `.streamlit/config.toml` for custom settings:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 8501
```

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `STREAMLIT_SERVER_PORT`: Custom port (optional, default: 8501)

## Compliance Frameworks

### GDPR (General Data Protection Regulation)
- Data protection and privacy requirements
- Consent mechanism validation
- Subject rights compliance
- International transfer safeguards

### SOC2 (System and Organization Controls 2)
- Security controls and access management
- System availability and redundancy
- Processing integrity and validation
- Data confidentiality measures

### HIPAA (Health Insurance Portability and Accountability Act)
- Protected Health Information (PHI) security
- Access controls and audit requirements
- Business associate agreements
- Breach notification procedures

### RBI (Reserve Bank of India) Guidelines
- Financial data localization requirements
- Cybersecurity framework compliance
- KYC/AML procedure validation
- Payment system security

## API Reference

### ComplianceChecker Class
```python
from compliance_checker import ComplianceChecker

checker = ComplianceChecker(
    frameworks=["GDPR", "SOC2", "HIPAA", "RBI"],
    sensitivity="medium",
    include_pii=True,
    include_ai_analysis=True
)

results = checker.analyze_document(text_content)
```

### PIIDetector Class
```python
from pii_detector import PIIDetector

detector = PIIDetector()
pii_entities = detector.detect_pii(text)
```

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Formatting
```bash
black .
isort .
```

### Type Checking
```bash
mypy .
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing GPT-4o API
- spaCy team for excellent NLP capabilities
- Streamlit for the amazing web app framework

## Support

For support, email support@yourcompany.com or open an issue on GitHub.

## Roadmap

- [ ] Add more compliance frameworks (CCPA, PCI-DSS)
- [ ] Implement real-time document monitoring
- [ ] Add integration with document management systems
- [ ] Develop mobile application
- [ ] Add multi-language support

---

**Made with ❤️ for enterprise compliance and data protection**