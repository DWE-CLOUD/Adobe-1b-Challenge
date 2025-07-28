import nltk
import os

print("Downloading NLTK 'punkt' tokenizer data...")
download_dir = 'nltk_data'
os.makedirs(download_dir, exist_ok=True)
nltk.download('punkt_tab', download_dir=download_dir)
print(f"NLTK data saved successfully to '{download_dir}'")