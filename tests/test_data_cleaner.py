import os
from dotenv import load_dotenv
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

# Display results
# Print full DataFrame
print(cleaned_df)

# Print only urls column
df_with_urls = cleaned_df[cleaned_df["urls"].notna()]
print("Messages containing URLs:")
print(df_with_urls[["id", "urls"]])  # Only show relevant columns
print("Messages containing URLs count:"+str(df_with_urls.urls.count()))

print("Cleaned Chat Data Sample:")
print(cleaned_df.head())

# Validate that service messages were removed
assert "service" not in cleaned_df["type"].values, "Service messages were not properly removed."

print("Data cleaning test passed!")
