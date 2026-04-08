from flask import Flask, render_template, request, jsonify
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from huggingface_hub import login
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='.')

# Get Hugging Face token
hf_token = os.getenv("HUGGINGFACE_HUB_TOKEN")
logger.info(f"Token status: {'FOUND' if hf_token else 'NOT FOUND'}")

# Explicitly authenticate if token is available
if hf_token:
    try:
        login(token=hf_token, add_to_git_credential=False)
        logger.info("✓ Successfully authenticated with HuggingFace Hub")
    except Exception as e:
        logger.warning(f"⚠ Authentication error: {e}")
else:
    logger.warning("⚠ Warning: HUGGINGFACE_HUB_TOKEN not set. Gated models will fail to load.")

# --- Configuration ---
ADAPTER_REPO = "ayushnsfw/slang-translator-llama-1b"
BASE_MODEL = "meta-llama/Llama-3.2-1B-Instruct"

# --- Load Model & Tokenizer ---
logger.info("Loading model... this may take a moment.")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, token=hf_token)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    token=hf_token,
    torch_dtype=torch.float16,
    device_map="auto",
    low_cpu_mem_usage=True
)

# Load fine-tuned adapter
try:
    logger.info("Loading fine-tuned adapter...")
    model = PeftModel.from_pretrained(model, ADAPTER_REPO)
    logger.info("✓ Fine-tuned adapter loaded successfully")
except Exception as e:
    logger.warning(f"⚠ Could not load adapter: {e}")

def translate(formal_text):
    """Translate formal text to slang"""
    system_msg = "You are a specialized translator. Convert formal English into casual, modern slang."
    prompt = (
        f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
        f"{system_msg}<|eot_id|>"
        f"<|start_header_id|>user<|end_header_id|>\n\n"
        f"Translate: {formal_text}<|eot_id|>"
        f"<|start_header_id|>assistant<|end_header_id|>\n\n"
    )
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=64,
            temperature=0.7,
            do_sample=True,
            eos_token_id=tokenizer.eos_token_id
        )
    
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract only the assistant's response
    try:
        return decoded.split("assistant")[-1].strip()
    except:
        return decoded

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_api():
    """API endpoint for translation"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'success': False, 'error': 'Please provide text to translate'})
        
        slang_text = translate(text)
        return jsonify({'success': True, 'informal': slang_text})
    
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return jsonify({'success': False, 'error': f'Translation error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=7860)
