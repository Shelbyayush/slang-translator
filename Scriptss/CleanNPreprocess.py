import re
import string
import emoji
from textblob import TextBlob

# Dictionary of English contractions
contractions_dict = {
    "ain't": "am not",
    "awesum": "awesome",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "gonna": "going to",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "I'd": "I would",
    "I'd've": "I would have",
    "I'll": "I will",
    "I'll've": "I will have",
    "Im": "I am",
    "I'm": "I am",
    "I've": "I have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "luv": "love",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have"
}

def expand_contractions(text):
    """
    Expands contractions in a text string.
    For example: "I'm" becomes "I am".
    """
    contractions_pattern = re.compile('({})'.format('|'.join(contractions_dict.keys())),
                                    flags=re.IGNORECASE|re.DOTALL)
    text = re.sub(r"Im", "I'm", text)
    
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contractions_dict.get(match.lower())
        if not expanded_contraction:
            return match
        expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text

def normalize_case(text):
    """
    Converts all text to lowercase to ensure consistency.
    """
    return text.lower()

def remove_punctuation(text):
    """
    Removes punctuation characters from a text string.
    """
    # Using string.punctuation and re.sub()
    return re.sub(f'[{re.escape(string.punctuation)}]', '', text)

def handle_emojis(text):
    """
    Converts emojis to their textual representation.
    For example: '❤️' becomes ':red_heart:'.
    """
    return emoji.demojize(text, delimiters=(" <", "> "))

def normalize_elongated_words(text):
    """
    Reduces repeated characters in words used for emphasis.
    For example: "soooooo good" becomes "soo good".
    It keeps up to two repeated characters.
    """
    return re.sub(r'(.)\1{2,}', r'\1\1', text)

def correct_spelling(text):
    """
    Uses TextBlob to correct common spelling mistakes.
    Caution: This might incorrectly "fix" intentional slang.
    """
    # Use TextBlob for spelling correction
    text_blob = TextBlob(text)
    return str(text_blob.correct())

def preprocess_text(text):
    """
    A pipeline function that applies all the preprocessing steps in order.
    """
    text = expand_contractions(text)
    text = normalize_case(text)
    text = remove_punctuation(text)
    text = handle_emojis(text)
    text = normalize_elongated_words(text)
    # Spelling correction is last as it's computationally more expensive
    # and works best on cleaner text.
    text = correct_spelling(text)
    return text

# --- Example Usage ---
if __name__ == "__main__":
    sample_text = "I'm not gonna lie, that was soooooo awesum! I luv it ❤️. Y'all should try it."

    print("--- Original Text ---")
    print(sample_text)
    print("\n" + "="*30 + "\n")

    # --- Step-by-step demonstration ---
    print("--- Step-by-Step Preprocessing ---")
    step1 = expand_contractions(sample_text)
    print(f"1. Expand Contractions:\n   '{step1}'\n")

    step2 = normalize_case(step1)
    print(f"2. Normalize Case:\n   '{step2}'\n")

    step3 = remove_punctuation(step2)
    print(f"3. Remove Punctuation:\n   '{step3}'\n")

    step4 = handle_emojis(step3)
    print(f"4. Handle Emojis:\n   '{step4}'\n")

    step5 = normalize_elongated_words(step4)
    print(f"5. Normalize Elongated Words:\n   '{step5}'\n")

    step6 = correct_spelling(step5)
    print(f"6. Correct Spelling:\n   '{step6}'\n")

    print("="*30 + "\n")

    # --- Using the main pipeline function ---
    print("--- Final Processed Text (using pipeline) ---")
    processed_text = preprocess_text(sample_text)
    print(processed_text)

