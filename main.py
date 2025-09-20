# main.py

# Import the specific functions you need from your scripts
from Scriptss.preprocess_data import preprocess_text
from Scriptss.format_data import format_for_sft # Assuming you have such a function
from Scriptss.fine_tune import run_training # Assuming you refactor fine_tune.py into a function
from Scriptss.infer import translate_to_slang

def run_full_pipeline():
    """
    Orchestrates the entire process from preprocessing to inference.
    """
    print("--- Step 1: Preprocessing Data ---")
    # This is a simplified example. You'd read a file, process it, and save it.
    # preprocess_data() # You would call your main preprocessing function here.
    print("Data preprocessing complete.")

    print("\n--- Step 2: Formatting Data ---")
    # format_data() # You would call your main formatting function here.
    print("Data formatting complete.")

    print("\n--- Step 3: Fine-Tuning Model ---")
    # run_training() # This would launch the fine-tuning process.
    print("Model fine-tuning complete.")

    print("\n--- Step 4: Running Inference for a Test ---")
    formal_sentence = "I am very excited about this new project."
    slang_translation = translate_to_slang(formal_sentence)
    
    print(f"\nFormal Input: '{formal_sentence}'")
    print(f"Slang Output: '{slang_translation}'")


if __name__ == "__main__":
    run_full_pipeline()