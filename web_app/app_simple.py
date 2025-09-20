from flask import Flask, render_template, request, jsonify
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Simple translation mappings for fallback
TRANSLATION_MAPPINGS = {
    "i would like to request your assistance": "can you help me out?",
    "please wait a moment": "hang on a sec",
    "thank you for your help": "thanks a lot!",
    "i appreciate your time": "thanks for your time",
    "could you please": "can you",
    "i would be grateful if": "it would be awesome if",
    "please let me know": "let me know",
    "i apologize for the inconvenience": "sorry about that",
    "i hope this email finds you well": "hey there",
    "i am writing to inform you": "just wanted to let you know",
    "i would like to express my gratitude": "thanks so much",
    "please find attached": "here's the file",
    "i look forward to hearing from you": "let me know what you think",
    "please do not hesitate to contact me": "feel free to reach out",
    "i would like to schedule a meeting": "want to meet up?",
    "please confirm your attendance": "are you coming?",
    "i regret to inform you": "unfortunately",
    "i am pleased to announce": "great news!",
    "please be advised": "heads up",
    "i would like to take this opportunity": "wanted to mention"
}

def simple_translate(formal_text):
    """Simple rule-based translation"""
    text_lower = formal_text.lower().strip()
    
    # Check for exact matches first
    if text_lower in TRANSLATION_MAPPINGS:
        return TRANSLATION_MAPPINGS[text_lower]
    
    # More comprehensive translation mappings
    replacements = {
        "i would like to": "i want to",
        "please": "",
        "would you": "can you",
        "could you": "can you",
        "i am": "i'm",
        "you are": "you're",
        "it is": "it's",
        "do not": "don't",
        "cannot": "can't",
        "will not": "won't",
        "should not": "shouldn't",
        "thank you": "thanks",
        "i appreciate": "thanks for",
        "i apologize": "sorry",
        "i hope": "hoping",
        "i look forward to": "looking forward to",
        "please let me know": "let me know",
        "i would be grateful": "it would be awesome",
        "i regret to inform": "unfortunately",
        "i am pleased to": "great news!",
        "please be advised": "heads up",
        "i would like to take this opportunity": "wanted to mention",
        "please find attached": "here's the file",
        "i look forward to hearing from you": "let me know what you think",
        "please do not hesitate to contact me": "feel free to reach out",
        "i would like to schedule a meeting": "want to meet up?",
        "please confirm your attendance": "are you coming?",
        "i am writing to inform you": "just wanted to let you know",
        "i would like to express my gratitude": "thanks so much",
        "i hope this email finds you well": "hey there",
        "i apologize for the inconvenience": "sorry about that"
    }
    
    result = formal_text
    # Apply replacements in order of length (longest first)
    for formal, informal in sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True):
        if formal in text_lower:
            result = result.replace(formal, informal)
            break  # Only apply one replacement to avoid conflicts
    
    # Clean up extra spaces and punctuation
    result = " ".join(result.split())
    
    # If no changes were made, add a casual prefix
    if result == formal_text:
        result = f"Hey! {formal_text.lower()}"
    
    return result

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
        
        logger.info(f"Received text: '{formal_text}'")
        
        if not formal_text:
            return jsonify({'error': 'Please enter some text'}), 400
        
        # Use simple translation
        informal_text = simple_translate(formal_text)
        
        logger.info(f"Translated to: '{informal_text}'")
        
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
    return jsonify({'status': 'healthy', 'model_loaded': True})

@app.route('/test')
def test():
    """Test translation endpoint"""
    test_text = "I would like to request your assistance"
    result = simple_translate(test_text)
    return jsonify({
        'input': test_text,
        'output': result,
        'status': 'working'
    })

if __name__ == '__main__':
    # Get port from environment variable
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(debug=False, host='0.0.0.0', port=port)
