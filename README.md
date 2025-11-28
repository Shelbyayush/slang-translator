# 🚀 Slang Translator

A powerful AI-powered translator that converts formal English text to informal slang using the Mistral 7B model.
▶️ [Download Demo Video](https://github.com/Shelbyayush/slang-translator/raw/main/demo_video.mov)
## ✨ Features

- **AI-Powered Translation**: Uses Mistral 7B Instruct model for accurate translations
- **Beautiful Web Interface**: Modern, responsive design
- **Real-time Translation**: Instant results as you type
- **Example Sentences**: Click to try pre-loaded examples
- **Health Monitoring**: Built-in health check endpoint

## 🚀 Quick Start

### Option 1: Web App (Recommended)
```bash
./run_web_app.sh
```
Then open http://localhost:5002 in your browser.

### Option 2: Command Line
```bash
source nlpenv/bin/activate
python Scriptss/infer.py
```

## 📁 Project Structure

```
Slang_Translator/
├── web_app/                 # Web application
│   ├── app.py              # Main Flask app
│   ├── templates/          # HTML templates
│   └── static/             # CSS/JS files
├── Scriptss/               # Python scripts
│   ├── infer.py            # Command-line inference
│   ├── fine_tune.py        # Model training
│   ├── preprocess_data.py  # Data preprocessing
│   └── format_data.py      # Data formatting
├── Dataa/                  # Data files
│   ├── raw_data_fixed.csv  # Cleaned dataset
│   └── formatted_dataset.jsonl # Training data
└── run_web_app.sh         # Quick launcher
```

## 🔧 Setup

1. **Activate virtual environment:**
   ```bash
   source nlpenv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r web_app/requirements.txt
   ```

3. **Run the app:**
   ```bash
   ./run_web_app.sh
   ```

## 🌐 Web Interface

- **URL**: http://localhost:5002
- **Features**: 
  - Real-time translation
  - Example sentences
  - Responsive design
  - Error handling

## 📊 Data

- **Dataset**: 1,348 formal-to-informal text pairs
- **Format**: CSV with cleaned data
- **Training**: Ready for fine-tuning with Mistral 7B

## 🔐 Authentication

- **Hugging Face Token**: Embedded in code
- **Model Access**: Automatic authentication
- **No Manual Setup**: Ready to use out of the box

## 🐳 Docker Deployment

### Quick Start with Docker
```bash
# Set your Hugging Face token
export HUGGINGFACE_HUB_TOKEN="your_token_here"

# Build and run with Docker
./build_docker.sh
```

### Manual Docker Commands
```bash
# Build the image
docker build -t slang-translator:latest .

# Run the container
docker run -d --name slang-translator-app -p 5000:5000 -e HUGGINGFACE_HUB_TOKEN="your_token" slang-translator:latest
```

### Access the App
- **Local URL**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

## 🎬 Demo Video

**Watch the live demo**: [![Demo Video](https://img.shields.io/badge/📹-Watch%20Demo-red?style=for-the-badge)](demo_video.mov)

### What the demo shows:
- 🐳 **Docker containerization** - Building and running the container
- 🎨 **Web interface** - Clean UI with "Created by Ayush Chaudhary"
- ⚡ **Real-time translation** - Live examples of formal to slang conversion
- 🔧 **Technical details** - Docker commands and container management
- 📊 **Performance** - Model loading and translation speed

### Demo Highlights:
- **Interface**: Modern, responsive design with your name prominently displayed
- **Functionality**: Multiple translation examples showing accuracy
- **Docker**: Complete containerization process from build to run
- **Technical**: Terminal commands and container status monitoring
=======
## 🚀 Deployment

### Local Development
```bash
./run_web_app.sh
```

### Docker (Recommended)
```bash
./build_docker.sh
```

## 🛠️ Troubleshooting

- **Port 5002 in use**: The script automatically uses port 5002
- **Model loading slow**: First run downloads 13GB model
- **Memory issues**: Mistral 7B needs ~16GB RAM

## 📱 Usage

1. **Web App**: Enter formal text → Get slang translation
2. **CLI**: Run `python Scriptss/infer.py` for command-line interface
3. **API**: Use `/translate` endpoint for programmatic access

## 🎯 Examples

- "I would like to request your assistance" → "Can you help me out?"
- "Please wait a moment" → "Hang on a sec"
- "Thank you for your help" → "Thanks a lot!"

## 📈 Performance

- **Model**: Mistral 7B Instruct v0.2
- **Size**: ~13GB
- **Speed**: 2-5 seconds per translation
- **Accuracy**: High-quality slang translations

---

**Ready to translate? Run `./run_web_app.sh` and start converting formal text to slang!** 🎉

made a new branch "test_new_changes"
