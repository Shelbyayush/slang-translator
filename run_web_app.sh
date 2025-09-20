#!/bin/bash

echo "🚀 Starting Slang Translator Web App..."

# Check if virtual environment exists
if [ ! -d "nlpenv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
source nlpenv/bin/activate

# Install Flask if not already installed
pip install Flask==2.3.3

# Set Hugging Face token
export HUGGINGFACE_HUB_TOKEN="f_dHMvtQsUlDqCIBaWCSJfpgcsVwnVArbdQw"

# Start the web app
echo "🌐 Starting web server on http://localhost:5002"
echo "📱 Open your browser and go to: http://localhost:5002"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

cd web_app
python app.py
