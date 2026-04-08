#!/bin/bash

# Slang Translator - Docker Build Script
echo "🐳 Building Slang Translator Docker Image..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if HUGGINGFACE_HUB_TOKEN is set
if [ -z "$HUGGINGFACE_HUB_TOKEN" ]; then
    print_warning "HUGGINGFACE_HUB_TOKEN not set. Please set it:"
    echo "export HUGGINGFACE_HUB_TOKEN='your_token_here'"
    echo ""
    read -p "Enter your Hugging Face token: " token
    if [ -n "$token" ]; then
        export HUGGINGFACE_HUB_TOKEN="$token"
        print_success "Token set for this session"
    else
        print_error "No token provided. Exiting."
        exit 1
    fi
fi

# Build the Docker image
print_status "Building Docker image..."
docker build -t slang-translator:latest .

if [ $? -eq 0 ]; then
    print_success "Docker image built successfully!"
else
    print_error "Docker build failed!"
    exit 1
fi

# Ask if user wants to run the container
echo ""
read -p "Do you want to run the container now? (y/n): " run_now

if [ "$run_now" = "y" ] || [ "$run_now" = "Y" ]; then
    print_status "Starting container..."
    docker run -d \
        --name slang-translator-app \
        -p 5000:5000 \
        -e HUGGINGFACE_HUB_TOKEN="$HUGGINGFACE_HUB_TOKEN" \
        slang-translator:latest
    
    if [ $? -eq 0 ]; then
        print_success "Container started successfully!"
        print_status "App is available at: http://localhost:5000"
        print_status "Health check: http://localhost:5000/health"
        echo ""
        print_status "To view logs: docker logs slang-translator-app"
        print_status "To stop: docker stop slang-translator-app"
        print_status "To remove: docker rm slang-translator-app"
    else
        print_error "Failed to start container!"
        exit 1
    fi
else
    print_status "Container not started. You can run it later with:"
    echo "docker run -d --name slang-translator-app -p 5000:5000 -e HUGGINGFACE_HUB_TOKEN='$HUGGINGFACE_HUB_TOKEN' slang-translator:latest"
fi

print_success "Docker setup complete! 🎉"
