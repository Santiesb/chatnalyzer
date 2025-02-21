import re
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class ChatDataCleaner:
    def __init__(self, messages: List[Dict[str, Any]]):
        """
        Initializes the cleaner with raw messages.
        
        :param messages: List of messages from the Telegram JSON.
        """
        self.messages = messages
        self.cleaned_data = None

    def remove_service_messages(self) -> List[Dict[str, Any]]:
        """
        Removes messages that are of type 'service' (e.g., user joined, changed group name).
        
        :return: List of cleaned messages without service messages.
        """
        filtered_messages = [msg for msg in self.messages if msg.get("type") == "message"]
        logger.info(f"Removed {len(self.messages) - len(filtered_messages)} service messages.")
        return filtered_messages

    def standardize_timestamps(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Converts timestamps to datetime objects.

        :param messages: List of messages with raw timestamps.
        :return: List of messages with standardized timestamps.
        """
        for msg in messages:
            if "date" in msg:
                msg["date"] = datetime.fromisoformat(msg["date"])
        logger.info("Standardized timestamps for all messages.")
        return messages

    def extract_urls(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extracts URLs from messages and moves them to a separate column.

        :param messages: List of messages.
        :return: List of messages with URLs separated.
        """
        url_pattern = re.compile(r"https?://\S+|www\.\S+")  # Matches http, https, www links

        for msg in messages:
            urls = []

            # Case 1: "text" is a simple string
            if "text" in msg and isinstance(msg["text"], str):
                urls = url_pattern.findall(msg["text"])  # Extract URLs from text
                msg["text"] = url_pattern.sub("", msg["text"]).strip()  # Remove URLs from message text

            # Case 2: "text" is a list (Telegram format with entities)
            elif "text" in msg and isinstance(msg["text"], list):
                extracted_text = []
                for entity in msg["text"]:
                    if isinstance(entity, dict):
                        if entity.get("type") == "link":
                            urls.append(entity["text"])  # Extract URL from dictionary
                        else:
                            extracted_text.append(entity.get("text", ""))  # Keep non-URL text
                    elif isinstance(entity, str):
                        extracted_text.append(entity)  # Keep plain strings in text list
                
                # Convert text list back into a string
                msg["text"] = " ".join(extracted_text).strip()

            # Store extracted URLs separately
            msg["urls"] = urls if urls else None

        logger.info("Extracted URLs and removed them from text messages.")
        return messages


    def normalize_text(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Converts text to lowercase and removes special characters.

        :param messages: List of messages with raw text.
        :return: List of messages with cleaned text.
        """
        for msg in messages:
            if "text" in msg and isinstance(msg["text"], str):
                msg["text"] = re.sub(r"[^a-zA-Z0-9\s]", "", msg["text"].lower())
        logger.info("Normalized text for all messages.")
        return messages

    def clean_data(self) -> pd.DataFrame:
        """
        Runs all cleaning functions and returns a cleaned Pandas DataFrame.

        :return: Cleaned messages in a DataFrame format.
        """
        cleaned_messages = self.remove_service_messages()
        cleaned_messages = self.standardize_timestamps(cleaned_messages)
        cleaned_messages = self.extract_urls(cleaned_messages)  # Extract URLs before normalizing text
        cleaned_messages = self.normalize_text(cleaned_messages)

        # Convert to DataFrame
        self.cleaned_data = pd.DataFrame(cleaned_messages)
        logger.info(f"Cleaned data contains {len(self.cleaned_data)} messages.")
        return self.cleaned_data
