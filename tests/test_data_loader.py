import os
from dotenv import load_dotenv
from src.data_loader import TelegramDataLoader

# Load environment variables from .env file
load_dotenv()

# Get values from environment variables
TEST_FOLDER_PATH = os.getenv("TEST_FOLDER_PATH")
JSON_FILENAME = os.getenv("JSON_FILENAME", "result.json")  # Default to 'result.json' if not set

# Validate the folder path
if not TEST_FOLDER_PATH:
    raise ValueError("TEST_FOLDER_PATH environment variable is not set.")

if not os.path.exists(TEST_FOLDER_PATH):
    raise FileNotFoundError(f"The folder {TEST_FOLDER_PATH} does not exist. Please verify the path.")

# Instantiate the loader with the specified folder and JSON file
loader = TelegramDataLoader(import_folder=TEST_FOLDER_PATH, json_filename=JSON_FILENAME)

# Retrieve data
messages = loader.get_messages()
metadata = loader.get_metadata()

# Display results
print("Chat Metadata:", metadata)
print(f"Total Messages: {len(messages)}")
