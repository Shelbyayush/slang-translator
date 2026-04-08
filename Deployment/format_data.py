import pandas as pd
import json
from pathlib import Path

def create_llama_instruction_prompt(formal_sentence, slang_sentence):
    """
    Formats the sentence pair into the Llama 3.2 Chat/Instruction format.
    Template: <|begin_of_text|><|start_header_id|>system<|end_header_id|>
    {System Prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>
    {User Prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
    {Response}<|eot_id|>
    """
    system_msg = "You are a specialized translator. Convert formal English into casual, modern slang."
    
    prompt = (
        f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
        f"{system_msg}<|eot_id|>"
        f"<|start_header_id|>user<|end_header_id|>\n\n"
        f"Translate: {formal_sentence}<|eot_id|>"
        f"<|start_header_id|>assistant<|end_header_id|>\n\n"
        f"{slang_sentence}<|eot_id|>"
    )
    return prompt

def main():
    """Reads cleaned data and formats it into a JSONL file for Llama 3.2 fine-tuning."""
    # Define file paths (Adjust paths as needed for your deployment branch structure)
    data_dir = Path("../Dataa")
    cleaned_data_path = data_dir / "cleaned_data.csv"
    formatted_data_path = data_dir / "formatted_dataset.jsonl"

    if not cleaned_data_path.is_file():
        print(f"Error: Cleaned data file not found at {cleaned_data_path}")
        return

    print(f"Reading cleaned data from {cleaned_data_path}...")
    df = pd.read_csv(cleaned_data_path)
    
    # Ensure columns are strings and remove any NaNs
    df = df.dropna(subset=['formal_text_cleaned', 'informal_text_cleaned'])
    df['formal_text_cleaned'] = df['formal_text_cleaned'].astype(str)
    df['informal_text_cleaned'] = df['informal_text_cleaned'].astype(str)

    print(f"Formatting data for Llama 3.2 and saving to {formatted_data_path}...")
    with open(formatted_data_path, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            formatted_string = create_llama_instruction_prompt(
                row['formal_text_cleaned'], 
                row['informal_text_cleaned']
            )
            
            # Create a JSON object and write it to the file
            json_record = {"text": formatted_string}
            f.write(json.dumps(json_record) + '\n')

    print(f"Formatting complete. Successfully created {formatted_data_path}.")

if __name__ == "__main__":
    main()