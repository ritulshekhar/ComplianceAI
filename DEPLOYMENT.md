# Deployment Guide

This document provides step-by-step instructions for deploying the AI Compliance Checker to various platforms.

## Table of Contents
- [Streamlit Cloud](#streamlit-cloud)
- [Heroku](#heroku)
- [Docker](#docker)
- [AWS EC2](#aws-ec2)
- [Railway](#railway)

## Streamlit Cloud (Recommended)

### Prerequisites
- GitHub repository with your code
- Streamlit Cloud account (free)
- OpenAI API key

### Steps
1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Click "New app"
   - Connect your GitHub repository
   - Set main file path: `app.py`
   - Add secrets in Advanced settings:
     ```
     OPENAI_API_KEY = "your-api-key-here"
     ```

3. **Access your app**
   - Your app will be available at: `https://share.streamlit.io/username/repo-name/main/app.py`

## Heroku

### Prerequisites
- Heroku account
- Heroku CLI installed

### Steps
1. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

2. **Create Procfile**
   ```bash
   echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
   ```

3. **Set environment variables**
   ```bash
   heroku config:set OPENAI_API_KEY=your-api-key-here
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

## Docker

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data
```

### Commands
```bash
# Build and run
docker build -t ai-compliance-checker .
docker run -p 8501:8501 -e OPENAI_API_KEY=your-key ai-compliance-checker

# Using docker-compose
docker-compose up
```

## AWS EC2

### Steps
1. **Launch EC2 instance**
   - Choose Ubuntu 22.04 LTS
   - Select t3.medium or larger
   - Configure security group to allow port 8501

2. **Connect and setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and pip
   sudo apt install python3.11 python3.11-pip -y
   
   # Clone repository
   git clone https://github.com/yourusername/ai-compliance-checker.git
   cd ai-compliance-checker
   
   # Install dependencies
   pip3.11 install -r requirements.txt
   
   # Download spaCy model
   python3.11 -m spacy download en_core_web_sm
   ```

3. **Set environment variables**
   ```bash
   echo "export OPENAI_API_KEY='your-api-key'" >> ~/.bashrc
   source ~/.bashrc
   ```

4. **Run with PM2 (process manager)**
   ```bash
   # Install PM2
   sudo npm install -g pm2
   
   # Create ecosystem file
   cat > ecosystem.config.js << EOF
   module.exports = {
     apps: [{
       name: 'compliance-checker',
       script: 'python3.11',
       args: '-m streamlit run app.py --server.port 8501 --server.address 0.0.0.0',
       cwd: '/home/ubuntu/ai-compliance-checker',
       env: {
         OPENAI_API_KEY: 'your-api-key'
       }
     }]
   }
   EOF
   
   # Start application
   pm2 start ecosystem.config.js
   pm2 startup
   pm2 save
   ```

## Railway

### Steps
1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and initialize**
   ```bash
   railway login
   railway init
   ```

3. **Deploy**
   ```bash
   railway up
   ```

4. **Set environment variables**
   ```bash
   railway variables set OPENAI_API_KEY=your-api-key
   ```

## Environment Variables

All deployments require these environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |
| `STREAMLIT_SERVER_PORT` | Port number (default: 8501) | No |
| `STREAMLIT_SERVER_ADDRESS` | Server address (default: 0.0.0.0) | No |

## Security Considerations

1. **Never commit API keys** to version control
2. **Use environment variables** for all secrets
3. **Enable HTTPS** in production
4. **Implement rate limiting** for API calls
5. **Regular security updates** for dependencies

## Monitoring

### Health Checks
```python
# Add to app.py for health monitoring
import streamlit as st

@st.cache_data
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
```

### Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Troubleshooting

### Common Issues

1. **Port binding errors**
   - Ensure the correct port is specified
   - Check firewall settings

2. **Memory issues**
   - Increase instance size
   - Optimize model loading

3. **API rate limits**
   - Implement request throttling
   - Add retry logic

4. **File upload limits**
   - Configure max file size in Streamlit
   - Handle large files appropriately

### Performance Optimization

1. **Caching**
   ```python
   @st.cache_data
   def load_model():
       return spacy.load("en_core_web_sm")
   ```

2. **Async processing**
   ```python
   import asyncio
   
   async def process_document(text):
       # Async document processing
       pass
   ```

3. **Resource monitoring**
   - Monitor CPU and memory usage
   - Set up alerts for high resource consumption