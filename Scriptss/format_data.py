import pandas as pd
import json
from pathlib import Path

def create_instruction_prompt(formal_sentence, slang_sentence):
    """Formats the sentence pair into the Mistral-instruct prompt format."""
    # Using the standard Mistral instruction format
    return f"<s>[INST] Translate the following formal English sentence to informal slang: {formal_sentence} [/INST] {slang_sentence} </s>"

def main():
    """Reads cleaned data and formats it into a JSONL file for SFTTrainer."""
    # Define file paths
    data_dir = Path("Dataa")
    cleaned_data_path = data_dir / "raw_data_fixed.csv"  # Use the fixed CSV
    formatted_data_path = data_dir / "formatted_dataset.jsonl"

    # Check if cleaned data file exists
    if not cleaned_data_path.is_file():
        print(f"Error: Fixed data file not found at {cleaned_data_path}")
        print("Please run the data preprocessing first.")
        return

    print(f"Reading data from {cleaned_data_path}...")
    df = pd.read_csv(cleaned_data_path)
    
    # Use the original columns from the fixed CSV
    formal_col = 'formal_text'
    informal_col = 'informal_text'
    
    # Ensure columns exist
    if formal_col not in df.columns or informal_col not in df.columns:
        print(f"Error: Expected columns '{formal_col}' and '{informal_col}' not found.")
        print(f"Available columns: {df.columns.tolist()}")
        return
    
    # Ensure columns are strings
    df[formal_col] = df[formal_col].astype(str)
    df[informal_col] = df[informal_col].astype(str)

    print(f"Formatting data and saving to {formatted_data_path}...")
    
    # Create formatted data
    formatted_data = []
    for _, row in df.iterrows():
        formal_text = row[formal_col].strip()
        informal_text = row[informal_col].strip()
        
        # Skip empty or very short texts
        if len(formal_text) < 3 or len(informal_text) < 3:
            continue
            
        formatted_text = create_instruction_prompt(formal_text, informal_text)
        formatted_data.append({"text": formatted_text})

    # Save as JSONL
    with open(formatted_data_path, 'w', encoding='utf-8') as f:
        for item in formatted_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    print(f"Formatted {len(formatted_data)} examples and saved to {formatted_data_path}")
    print("Data formatting completed!")

if __name__ == "__main__":
    main()
