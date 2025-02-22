import re
import pandas as pd
import unicodedata
import emoji
from typing import List, Dict, Any
from datetime import datetime
import logging
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer

# Ensure necessary resources are downloaded
import nltk

def check_nltk_resource(resource_name: str):
    try:
        nltk.data.find(resource_name)
    except LookupError:
        nltk.download(resource_name, quiet=True)

# At the start of the class or in __init__:
check_nltk_resource("stopwords")
check_nltk_resource("wordnet")
check_nltk_resource("punkt")

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

    def remove_service_messages(self) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Removes messages that are of type 'service' (e.g., user joined, changed group name).
        
        :return: List of cleaned messages without service messages.
        """
        #print list of type of messages in the chat
        types = set([msg.get("type") for msg in self.messages])
        logger.info(f"Message types found in the chat: {types}")

        filtered_actions = [msg for msg in self.messages if msg.get("type") == "service"]
        filtered_messages = [msg for msg in self.messages if msg.get("type") == "message"]
        logger.info(f"Removed {len(self.messages) - len(filtered_messages)} service messages.")
        return filtered_messages, filtered_actions

    def standardize_timestamps(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Converts timestamps to datetime objects."""
        if messages:
            for msg in messages:
                if "date" in msg:
                    msg["date"] = datetime.fromisoformat(msg["date"])
            logger.info(f"Standardized timestamps for {len(messages)} messages.")  # ✅ Unique log message
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

            if "text" in msg and isinstance(msg["text"], str):
                urls = url_pattern.findall(msg["text"])  
                msg["text"] = url_pattern.sub("", msg["text"]).strip()  

            elif "text" in msg and isinstance(msg["text"], list):
                extracted_text = []
                for entity in msg["text"]:
                    if isinstance(entity, dict) and entity.get("type") == "link":
                        urls.append(entity["text"])  
                    elif isinstance(entity, str):
                        extracted_text.append(entity)  

                msg["text"] = " ".join(extracted_text).strip()

            msg["urls"] = ", ".join(urls) if urls else None

        logger.info("Extracted URLs and removed them from text messages.")
        return messages

    def extract_emojis(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extracts emojis from messages and moves them to a separate column.

        :param messages: List of messages.
        :return: List of messages with extracted emojis.
        """
        for msg in messages:
            if "text" in msg and isinstance(msg["text"], str):
                # Extract emojis using emoji.is_emoji()
                extracted_emojis = "".join(c for c in msg["text"] if emoji.is_emoji(c))

                # Remove emojis from the message text
                msg["text"] = emoji.replace_emoji(msg["text"], replace="")

                # Store extracted emojis in a separate column
                msg["emojis"] = extracted_emojis if extracted_emojis else None

        logger.info("Extracted emojis and removed them from text messages.")
        return messages

    def normalize_text(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalizes text by:
        - Lowercasing all text.
        - Replacing accented characters (á → a, ñ → n).
        - Expanding common contractions.
        - Removing extra spaces and non-alphanumeric characters.

        The original text remains unchanged in a separate column.

        :param messages: List of messages with raw text.
        :return: List of messages with cleaned and original text.
        """
        def remove_accents(text: str) -> str:
            """Removes accents from characters using Unicode normalization."""
            return unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8")

        for msg in messages:
            if "text" in msg:
                if isinstance(msg["text"], list):
                    msg["text"] = " ".join([str(item) for item in msg["text"] if isinstance(item, str)])
                
                if isinstance(msg["text"], str):
                    msg["original_text"] = msg["text"]
                # Convert text to lowercase
                    cleaned_text = msg["text"].lower()

                    # Replace accented characters
                    cleaned_text = remove_accents(cleaned_text)

                    # Remove special characters except spaces
                    cleaned_text = re.sub(r"[^a-z0-9\s]", "", cleaned_text)

                    # Trim extra spaces
                    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

                    msg["cleaned_text"] = cleaned_text  # Store cleaned version
                    
                else:
                    msg["cleaned_text"] = ""

        logger.info("Applied text normalization: lowercasing, removing accents, cleaning characters.")
        return messages

    def tokenize_text(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Tokenizes cleaned text into individual words using NLTK's word tokenizer.
        
        :param messages: List of messages with cleaned text.
        :return: List of messages with an additional 'tokens' field containing tokenized words.
        """
        for msg in messages:
            if "cleaned_text" in msg and isinstance(msg["cleaned_text"], str):
                msg["tokens"] = nltk.word_tokenize(msg["cleaned_text"])  # Tokenize cleaned text

        logger.info("Applied tokenization to all messages.")
        return messages

    def remove_stopwords_and_lemmatize(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Removes stopwords, applies lemmatization & stemming, and stores results in 'filtered_tokens'.
        
        :param messages: List of messages with tokenized words.
        :return: List of messages with an additional 'filtered_tokens' field.
        """
        stop_words = set(stopwords.words("spanish"))  # Load Spanish stopwords
        stemmer = SnowballStemmer("spanish")  # Stemming tool
        lemmatizer = WordNetLemmatizer()  # Lemmatization tool (WordNet-based, works best for English)

        for msg in messages:
            if "tokens" in msg and isinstance(msg["tokens"], list):
                # Remove stopwords
                filtered_words = [word for word in msg["tokens"] if word not in stop_words]

                # Apply lemmatization and stemming
                lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]
                stemmed_words = [stemmer.stem(word) for word in lemmatized_words]

                msg["filtered_tokens"] = stemmed_words  # Store final processed tokens

        logger.info("Applied stopword removal, lemmatization, and stemming.")
        return messages


    def clean_data(self) -> pd.DataFrame:
        """
        Runs all cleaning functions and returns a cleaned Pandas DataFrame.
        """
        cleaned_messages, self.cleaned_actions = self.remove_service_messages() 
        cleaned_messages = self.standardize_timestamps(cleaned_messages)
        cleaned_messages = self.extract_urls(cleaned_messages)
        cleaned_messages = self.extract_emojis(cleaned_messages)
        cleaned_messages = self.normalize_text(cleaned_messages)
        cleaned_messages = self.tokenize_text(cleaned_messages)
        cleaned_messages = self.remove_stopwords_and_lemmatize(cleaned_messages)

        # convert to dataframe
        self.cleaned_data = pd.DataFrame(cleaned_messages)
        logger.info(f"Cleaned data contains {len(self.cleaned_data)} messages.")
        return self.cleaned_data

