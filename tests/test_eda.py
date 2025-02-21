import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from src.data_loader import TelegramDataLoader
from src.data_cleaner import ChatDataCleaner
from src.eda import ChatEDA

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

# Initialize EDA module
eda = ChatEDA(cleaned_df)

# Test: Messages per user
user_counts = eda.messages_per_user()
print("\n📊 Messages per User:")
print(user_counts.head())

# Test: Messages over time (Daily)
time_series = eda.messages_over_time("D")
print("\n📈 Messages Over Time (Daily):")
print(time_series.head())

# Test: Most common words
word_counts = eda.most_common_words(top_n=10)
print("\n🔠 Most Common Words:")
print(word_counts.head())

# Generate and display plots
print("\n🖼️ Generating Plots...")
eda.plot_messages_per_user()
eda.plot_messages_over_time("D")

print("\nEDA tests completed successfully!")
