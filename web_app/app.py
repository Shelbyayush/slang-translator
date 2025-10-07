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
            # Fallback to smaller model
            try:
                logger.info("Loading fallback model...")
                model_pipeline = pipeline(
                    "text-generation",
                    model="microsoft/DialoGPT-medium",
                    device=-1,
                    max_length=256,
                    do_sample=True,
                    temperature=0.7,
                )
                logger.info("Fallback model loaded!")
            except Exception as e2:
                logger.error(f"Failed to load fallback model: {e2}")
                model_pipeline = None

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
            return jsonify({'error': 'Model not available'}), 500
        
        # Create prompt for Mistral
        prompt = f"<s>[INST] Translate the following formal English sentence to informal slang: {formal_text} [/INST]"
        
        # Generate translation
        result = model_pipeline(
            prompt, 
            max_new_tokens=50, 
            pad_token_id=model_pipeline.tokenizer.eos_token_id
        )
        
        # Extract response
        generated_text = result[0]['generated_text']
        informal_text = generated_text.replace(prompt, "").strip()
        
        # Clean up response
        if informal_text.endswith("</s>"):
            informal_text = informal_text[:-4].strip()
        
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
    # Get port from environment variable (Docker/Cloud requirement)
    port = int(os.environ.get('PORT', 5001))
    
    # Load model on startup (commented out for faster startup)
    # load_model()
    
    # Run the app
    app.run(debug=False, host='0.0.0.0', port=port)
