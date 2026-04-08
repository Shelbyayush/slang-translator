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
    data_dir = Path("C:\\Users\\Isha\\IdeaProjects\\untitled\\Python\\Projects\\Slang_Translator\\Dataa")
    cleaned_data_path = data_dir / "cleaned_data.csv"
    formatted_data_path = data_dir / "formatted_dataset.jsonl"

    # Check if cleaned data file exists
    if not cleaned_data_path.is_file():
        print(f"Error: Cleaned data file not found at {cleaned_data_path}")
        print("Please run preprocess_data.py first.")
        return

    print(f"Reading cleaned data from {cleaned_data_path}...")
    df = pd.read_csv(cleaned_data_path)
    
    # Ensure columns are strings
    df['formal_text_cleaned'] = df['formal_text_cleaned'].astype(str)
    df['informal_text_cleaned'] = df['informal_text_cleaned'].astype(str)

    print(f"Formatting data and saving to {formatted_data_path}...")
    with open(formatted_data_path, 'w') as f:
        for index, row in df.iterrows():
            formal_text = row['formal_text_cleaned']
            informal_text = row['informal_text_cleaned']
            
            # Create the formatted string
            formatted_string = create_instruction_prompt(formal_text, informal_text)
            
            # Create a JSON object and write it to the file
            json_record = {"text": formatted_string}
            f.write(json.dumps(json_record) + '\n')

    print("Formatting complete.")
    print(f"\nSuccessfully created {formatted_data_path}.")
    # Print first few lines of the output file for verification
    with open(formatted_data_path, 'r') as f:
        print("\n--- Formatted Data Sample ---")
        for i, line in enumerate(f):
            if i >= 2: # Print first 2 records
                break
            print(line.strip())


if __name__ == "__main__":
    main()
