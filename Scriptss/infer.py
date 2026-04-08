import torch
from peft import PeftModel
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)
from pathlib import Path

# --- Configuration ---
# Make sure this path points to your saved fine-tuned model checkpoint
MODEL_PATH = "./models/slang_translator_v1_low_vram/final_checkpoint"
BASE_MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"

# --- Device Setup ---
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {DEVICE}")
print("Warning: Running on a CPU will be very slow and memory-intensive.")

# --- Load Model and Tokenizer (CPU Version) ---

# Load the base model without any quantization
# We specify torch_dtype=torch.float16 to load a smaller version of the model.
# This is crucial for running on a CPU with limited RAM.
base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL_NAME,
    torch_dtype=torch.float16, # Use half-precision floats
    device_map="auto" # Let transformers handle device mapping
)

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

# Load the PEFT model (your fine-tuned adapters)
# This will merge the adapter weights with the base model for inference
model = PeftModel.from_pretrained(base_model, MODEL_PATH)
model = model.eval() # Set the model to evaluation mode

print("Model and tokenizer loaded successfully.")

# --- Inference Function ---

def translate_to_slang(formal_sentence: str) -> str:
    """
    Takes a formal English sentence and returns its informal slang translation.
    """
    # Create the instruction-based prompt
    prompt = f"<s>[INST] Translate the following formal English sentence to informal slang: {formal_sentence} [/INST]"
    
    # Tokenize the input prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)

    # Generate the output
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=50,       # Max length of the generated slang
            temperature=0.7,         # Controls randomness. Lower is more deterministic.
            do_sample=True,          # Enable sampling for more creative outputs
            pad_token_id=tokenizer.eos_token_id
        )
    
    # Decode the generated tokens
    decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract only the generated part (the answer)
    try:
        slang_translation = decoded_output.split('[/INST]')[1].strip()
    except IndexError:
        slang_translation = "Sorry, I couldn't generate a translation."

    return slang_translation

# --- Example Usage ---
if __name__ == "__main__":
    # Example sentences to translate
    test_sentences = [
        "That is a very impressive achievement.",
        "I am feeling quite unwell today.",
    ]
    
    print("\n--- Running Inference Examples (this may take a few minutes per sentence) ---")
    for sentence in test_sentences:
        slang_version = translate_to_slang(sentence)
        print(f"Formal: {sentence}")
        print(f"Slang:  {slang_version}\n")

