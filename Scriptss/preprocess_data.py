import re
import string
import os
from pathlib import Path
import emoji
import pandas as pd
from textblob import TextBlob

# --- Preprocessing Functions (from your text_preprocessing_script) ---

# Dictionary of English contractions
contractions_dict = {
    "ain't": "am not", "aren't": "are not", "can't": "cannot", "can't've": "cannot have",
    "'cause": "because", "could've": "could have", "couldn't": "could not", "couldn't've": "could not have",
    "didn't": "did not", "doesn't": "does not", "don't": "do not", "hadn't": "had not",
    "hadn't've": "had not have", "hasn't": "has not", "haven't": "have not", "he'd": "he would",
    "he'd've": "he would have", "he'll": "he will", "he'll've": "he will have", "he's": "he is",
    "how'd": "how did", "how'd'y": "how do you", "how'll": "how will", "how's": "how is",
    "I'd": "I would", "I'd've": "I would have", "I'll": "I will", "I'll've": "I will have",
    "I'm": "I am", "I've": "I have", "isn't": "is not", "it'd": "it would",
    "it'd've": "it would have", "it'll": "it will", "it'll've": "it will have", "it's": "it is",
    "let's": "let us", "ma'am": "madam", "mayn't": "may not", "might've": "might have",
    "mightn't": "might not", "mightn't've": "might not have", "must've": "must have",
    "mustn't": "must not", "mustn't've": "must not have", "needn't": "need not",
    "needn't've": "need not have", "o'clock": "of the clock", "oughtn't": "ought not",
    "oughtn't've": "ought not have", "shan't": "shall not", "sha'n't": "shall not",
    "shan't've": "shall not have", "she'd": "she would", "she'd've": "she would have",
    "she'll": "she will", "she'll've": "she will have", "she's": "she is",
    "should've": "should have", "shouldn't": "should not", "shouldn't've": "should not have",
    "so've": "so have", "so's": "so is", "that'd": "that would", "that'd've": "that would have",
    "that's": "that is", "there'd": "there would", "there'd've": "there would have",
    "there's": "there is", "they'd": "they would", "they'd've": "they would have",
    "they'll": "they will", "they'll've": "they will have", "they're": "they are",
    "they've": "they have", "to've": "to have", "wasn't": "was not", "we'd": "we would",
    "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have", "we're": "we are",
    "we've": "we have", "weren't": "were not", "what'll": "what will", "what'll've": "what will have",
    "what're": "what are", "what's": "what is", "what've": "what have", "when's": "when is",
    "when've": "when have", "where'd": "where did", "where's": "where is", "where've": "where have",
    "who'll": "who will", "who'll've": "who will have", "who's": "who is", "who've": "who have",
    "why's": "why is", "why've": "why have", "will've": "will have", "won't": "will not",
    "won't've": "will not have", "would've": "would have", "wouldn't": "would not",
    "wouldn't've": "would not have", "y'all": "you all", "y'all'd": "you all would",
    "y'all'd've": "you all would have", "y'all're": "you all are", "y'all've": "you all have",
    "you'd": "you would", "you'd've": "you would have", "you'll": "you will",
    "you'll've": "you will have", "you're": "you are", "you've": "you have"
}

def expand_contractions(text):
    contractions_pattern = re.compile('({})'.format('|'.join(contractions_dict.keys())), flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        expanded_contraction = contractions_dict.get(match.lower())
        return expanded_contraction if expanded_contraction else match
    expanded_text = contractions_pattern.sub(expand_match, text)
    return expanded_text

def normalize_case(text):
    return text.lower()

def remove_punctuation(text):
    return re.sub(f'[{re.escape(string.punctuation)}]', '', text)

def handle_emojis(text):
    return emoji.demojize(text, delimiters=(" <", "> "))

def normalize_elongated_words(text):
    return re.sub(r'(.)\1{2,}', r'\1\1', text)

def correct_spelling(text):
    # Use with caution
    return str(TextBlob(text).correct())

def preprocess_text(text):
    """Applies all preprocessing steps to a single text string."""
    if not isinstance(text, str):
        return ""
    text = expand_contractions(text)
    text = normalize_case(text)
    # Punctuation removal and other steps can be context-dependent.
    # For this task, we'll keep it simple.
    text = normalize_elongated_words(text)
    # Spelling correction is disabled by default due to its tendency
    # to "correct" actual slang. Uncomment if needed.
    # text = correct_spelling(text)
    return text

# --- Main Script Logic ---
def main():
    """Reads raw data, preprocesses it, and saves the cleaned data."""
    # Define file paths
    data_dir = Path("Dataa")
    raw_data_path = data_dir / "raw_data_fixed.csv"
    cleaned_data_path = data_dir / "cleaned_data.csv"

    # Check if raw data file exists
    if not raw_data_path.is_file():
        print(f"Error: Raw data file not found at {raw_data_path}")
        print("Please create the file and add data before running.")
        return

    print(f"Reading raw data from {raw_data_path}...")
    df = pd.read_csv(raw_data_path)

    print("Preprocessing data...")
    # Apply the preprocessing pipeline to both columns
    df['formal_text_cleaned'] = df['formal_text'].apply(preprocess_text)
    df['informal_text_cleaned'] = df['informal_text'].apply(preprocess_text)
    
    # Drop rows where cleaned text is empty
    df.dropna(subset=['formal_text_cleaned', 'informal_text_cleaned'], inplace=True)
    df = df[df['formal_text_cleaned'].str.strip() != '']
    df = df[df['informal_text_cleaned'].str.strip() != '']


    print(f"Saving cleaned data to {cleaned_data_path}...")
    # Select only the cleaned columns to save
    cleaned_df = df[['formal_text_cleaned', 'informal_text_cleaned']]
    cleaned_df.to_csv(cleaned_data_path, index=False)

    print("Preprocessing complete.")
    print("\n--- Cleaned Data Sample ---")
    print(cleaned_df.head())

if __name__ == "__main__":
    main()
