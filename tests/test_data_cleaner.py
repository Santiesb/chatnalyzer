import os
from dotenv import load_dotenv
import pandas as pd
from collections import Counter
from src.data_loader import TelegramDataLoader
from src.data_cleaner import ChatDataCleaner

# Load environment variables
load_dotenv()

# Retrieve folder path and JSON filename from .env
TEST_FOLDER_PATH = os.getenv("TEST_FOLDER_PATH")
JSON_FILENAME = os.getenv("JSON_FILENAME", "result.json")

# Ensure the path is valid
if not TEST_FOLDER_PATH:
    raise ValueError("TEST_FOLDER_PATH environment variable is not set.")

# Load raw chat data
loader = TelegramDataLoader(import_folder=TEST_FOLDER_PATH, json_filename=JSON_FILENAME)
raw_messages = loader.get_messages()

# Clean chat data
cleaner = ChatDataCleaner(raw_messages)
cleaned_df = cleaner.clean_data()

# Step 1: Basic message structure check
print("\n📊 Step 1: Cleaned Chat Data Sample (first 5 rows):")
print(cleaned_df[["id", "type", "date", "from", "original_text", "cleaned_text"]].head())

# Step 2: URL extraction check
if "urls" in cleaned_df.columns:
    url_counts = cleaned_df["urls"].dropna().value_counts().reset_index()
    url_counts.columns = ["URL", "Message Count"]
    print("\n🔗 Step 2: Most Shared URLs:")
    print(url_counts.head(10))
else:
    print("\n⚠️ Step 2: No URLs detected.")

# Step 3: Emoji extraction check
if "emojis" in cleaned_df.columns:
    emoji_counter = Counter("".join(cleaned_df["emojis"].dropna()))
    emoji_df = pd.DataFrame(emoji_counter.items(), columns=["Emoji", "Count"]).sort_values(by="Count", ascending=False)
    print("\n😀 Step 3: Most Used Emojis:")
    print(emoji_df.head(10))
else:
    print("\n⚠️ Step 3: No emojis detected.")

# Step 4: Text normalization check
print("\n📝 Step 4: Sample of Original vs. Normalized Text")
print(cleaned_df[["original_text", "cleaned_text"]].head(10))

# Step 5: Tokenization check
if "tokens" in cleaned_df.columns:
    print("\n✂️ Step 5: Tokenized Words (first 5 messages):")
    print(cleaned_df[["original_text", "tokens"]].head(5))
else:
    print("\n⚠️ Step 5: Tokenization not applied.")

# Step 6: Stopword Removal, Lemmatization & Stemming check
if "filtered_tokens" in cleaned_df.columns:
    print("\n🛠️ Step 6: Stopword Removal, Lemmatization & Stemming")
    print(cleaned_df[["original_text", "tokens", "filtered_tokens"]].head(5))
else:
    print("\n⚠️ Step 6: Stopword removal, lemmatization & stemming not applied.")

print("\n✅ Data Cleaning Tests Completed Successfully!")
