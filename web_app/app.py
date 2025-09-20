from flask import Flask, render_template, request, jsonify
import torch
from transformers import pipeline
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Set Hugging Face token
os.environ["HUGGINGFACE_HUB_TOKEN"] = "f_dHMvtQsUlDqCIBaWCSJfpgcsVwnVArbdQw"

# Global variable to store the model
model_pipeline = None

def load_model():
    """Load the Mistral model for translation"""
    global model_pipeline
    
    if model_pipeline is None:
        try:
            logger.info("Loading Mistral model...")
            model_pipeline = pipeline(
                "text-generation",
                model="mistralai/Mistral-7B-Instruct-v0.2",
                device=-1,  # Use CPU
                torch_dtype=torch.float16,
                max_length=512,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
            )
            logger.info("Model loaded successfully!")
        except Exception as e:
            logger.error(f"Failed to load Mistral model: {e}")
            model_pipeline = None

def translate_text(pipe, formal_text):
    """Translate formal text to informal using Mistral"""
    try:
        # Create prompt for Mistral
        prompt = f"<s>[INST] Translate the following formal English sentence to informal slang: {formal_text} [/INST]"
        
        # Generate translation
        result = pipe(
            prompt, 
            max_new_tokens=50, 
            pad_token_id=pipe.tokenizer.eos_token_id
        )
        
        # Extract response
        generated_text = result[0]['generated_text']
        informal_text = generated_text.replace(prompt, "").strip()
        
        # Clean up response
        if informal_text.endswith("</s>"):
            informal_text = informal_text[:-4].strip()
        
        return informal_text
        
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return f"Translation failed: {str(e)}"

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    """Translate formal text to informal"""
    try:
        data = request.get_json()
        formal_text = data.get('text', '').strip()
        
        if not formal_text:
            return jsonify({'error': 'Please enter some text'}), 400
        
        if model_pipeline is None:
            load_model()
        
        if model_pipeline is None:
            return jsonify({'error': 'Model not available. Please try again in a moment.'}), 500
        
        # Translate the text
        informal_text = translate_text(model_pipeline, formal_text)
        
        return jsonify({
            'formal': formal_text,
            'informal': informal_text,
            'success': True
        })
        
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return jsonify({'error': f'Translation failed: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'model_loaded': model_pipeline is not None})

if __name__ == '__main__':
    # Use port 5002 to avoid conflicts
    port = 5002
    
    # Load model on startup
    load_model()
    
    # Run the app
    print(f"🚀 Starting Slang Translator with Mistral on http://localhost:{port}")
    print("📱 Open your browser and go to the URL above")
    print("⏹️  Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=port)
