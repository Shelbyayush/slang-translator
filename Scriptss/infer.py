import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline
)
from pathlib import Path
import os

# --- Configuration ---
BASE_MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"

# Set Hugging Face token for gated model access
os.environ["HUGGINGFACE_HUB_TOKEN"] = "f_dHMvtQsUlDqCIBaWCSJfpgcsVwnVArbdQw"

# --- Device Setup ---
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {DEVICE}")

def load_model():
    """Load the Mistral model and tokenizer"""
    print("Loading Mistral model...")
    print("Note: This will download ~13GB of model files on first run.")
    
    try:
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME, trust_remote_code=True)
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "right"
        
        # Create text generation pipeline
        pipe = pipeline(
            "text-generation",
            model=BASE_MODEL_NAME,
            tokenizer=tokenizer,
            device=-1 if DEVICE == "cpu" else 0,  # Use CPU or GPU
            torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
            max_length=512,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
        )
        
        print("Model loaded successfully!")
        return pipe, tokenizer
        
    except Exception as e:
        print(f"Failed to load Mistral model: {e}")
        return None, None

def translate_text(pipe, tokenizer, formal_text):
    """Translate formal text to informal using Mistral"""
    try:
        # Create prompt for Mistral
        prompt = f"<s>[INST] Translate the following formal English sentence to informal slang: {formal_text} [/INST]"
        
        # Generate translation
        result = pipe(
            prompt, 
            max_new_tokens=50, 
            pad_token_id=tokenizer.eos_token_id
        )
        
        # Extract response
        generated_text = result[0]['generated_text']
        informal_text = generated_text.replace(prompt, "").strip()
        
        # Clean up response
        if informal_text.endswith("</s>"):
            informal_text = informal_text[:-4].strip()
        
        return informal_text
        
    except Exception as e:
        return f"Translation failed: {e}"

def main():
    print("=== Slang Translator ===")
    print(f"Using model: {BASE_MODEL_NAME}")
    
    # Load model
    pipe, tokenizer = load_model()
    
    if pipe is None:
        print("Failed to load model. Exiting.")
        return
    
    print("\nModel ready! Enter formal text to translate (type 'quit' to exit):")
    
    while True:
        try:
            formal_text = input("\nFormal text: ").strip()
            
            if formal_text.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not formal_text:
                print("Please enter some text.")
                continue
            
            print("Translating...")
            informal_text = translate_text(pipe, tokenizer, formal_text)
            
            print(f"Informal: {informal_text}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
