# 🚀 Slang Translator

A powerful AI-powered translator that converts formal English text to informal slang using the Mistral 7B model.

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

## 🚀 Deployment

### Local Development
```bash
./run_web_app.sh
```

### Production (Render)
1. Push to GitHub
2. Connect to Render
3. Set environment variables
4. Deploy automatically

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