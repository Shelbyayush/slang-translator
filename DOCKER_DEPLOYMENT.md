# 🐳 Docker Deployment Guide

## Overview
This guide will help you deploy your Slang Translator Flask application using Docker.

## 📋 Prerequisites
- Docker installed on your system
- Hugging Face token for model access
- At least 8GB RAM available for the container

## 🚀 Quick Start

### Option 1: Using the Build Script (Recommended)
```bash
# Set your Hugging Face token
export HUGGINGFACE_HUB_TOKEN="your_token_here"

# Run the build script
./build_docker.sh
```

### Option 2: Manual Docker Commands

#### Build the Image
```bash
docker build -t slang-translator:latest .
```

#### Run the Container
```bash
docker run -d \
  --name slang-translator-app \
  -p 5000:5000 \
  -e HUGGINGFACE_HUB_TOKEN="your_token_here" \
  slang-translator:latest
```

### Option 3: Using Docker Compose
```bash
# Set environment variable
export HUGGINGFACE_HUB_TOKEN="your_token_here"

# Start with docker-compose
docker-compose up -d
```

## 🔧 Configuration

### Environment Variables
- `HUGGINGFACE_HUB_TOKEN`: Your Hugging Face token (required)
- `FLASK_APP`: Set to `web_app/app.py` (default)
- `FLASK_ENV`: Set to `production` (default)
- `PORT`: Port number (default: 5000)

### Memory Requirements
- **Minimum**: 4GB RAM
- **Recommended**: 8GB RAM
- **Model Size**: ~13GB (Mistral-7B)

## 📊 Container Management

### View Logs
```bash
docker logs slang-translator-app
```

### Stop Container
```bash
docker stop slang-translator-app
```

### Remove Container
```bash
docker rm slang-translator-app
```

### Restart Container
```bash
docker restart slang-translator-app
```

## 🌐 Accessing the Application

- **Local URL**: http://localhost:5000
- **Health Check**: http://localhost:5000/health
- **API Endpoint**: http://localhost:5000/translate

## 🔍 Troubleshooting

### Common Issues

1. **Out of Memory Error**:
   - Increase Docker memory limit
   - Use a smaller model or CPU-only mode

2. **Model Loading Fails**:
   - Check Hugging Face token
   - Verify internet connection
   - Check container logs

3. **Port Already in Use**:
   - Change port mapping: `-p 8080:5000`
   - Stop conflicting services

### Debug Commands
```bash
# Check container status
docker ps -a

# View container logs
docker logs slang-translator-app

# Access container shell
docker exec -it slang-translator-app /bin/bash

# Check resource usage
docker stats slang-translator-app
```

## 🚀 Production Deployment

### Cloud Platforms

#### Google Cloud Run
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/slang-translator

# Deploy to Cloud Run
gcloud run deploy --image gcr.io/PROJECT_ID/slang-translator --platform managed
```

#### AWS ECS
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker tag slang-translator:latest ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/slang-translator:latest
docker push ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/slang-translator:latest
```

#### Azure Container Instances
```bash
# Build and push to Azure Container Registry
az acr build --registry myregistry --image slang-translator:latest .
```

## 📈 Performance Optimization

### For Production
- Use multi-stage builds
- Enable model caching
- Set appropriate memory limits
- Use GPU if available

### Resource Limits
```yaml
# In docker-compose.yml
deploy:
  resources:
    limits:
      memory: 8G
      cpus: '2.0'
    reservations:
      memory: 4G
      cpus: '1.0'
```

## 🔒 Security Considerations

1. **Environment Variables**: Never hardcode tokens
2. **Non-root User**: Container runs as non-root user
3. **Health Checks**: Built-in health monitoring
4. **Resource Limits**: Prevent resource exhaustion

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review container logs
3. Verify environment variables
4. Check system resources

---

**Happy Containerizing! 🐳🚀**
