import json
import logging
from pathlib import Path
from typing import Dict, List, Any

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class TelegramDataLoader:
    def __init__(self, import_folder: str, json_filename: str = "result.json"):
        """
        Initializes the class, allowing the user to define the folder containing the JSON file
        and optionally specify the JSON filename.

        :param import_folder: Path to the folder containing the JSON file.
        :param json_filename: Name of the JSON file (default: 'result.json').
        """
        self.file_path = Path(import_folder).resolve() / json_filename
        self._data = None
        logger.info(f"Initialized TelegramDataLoader with file: {self.file_path}")

    @property
    def data(self) -> Dict[str, Any]:
        """Loads data only if it hasn't been loaded yet."""
        if self._data is None:
            self._data = self.load_data()
        return self._data

    def load_data(self) -> Dict[str, Any]:
        """Loads data from the JSON file and stores it in _data."""
        if not self.file_path.exists():
            logger.warning(f"File not found: {self.file_path}")
            return {}

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Error loading {self.file_path}: {e}")
            return {}

    def get_messages(self) -> List[Dict[str, Any]]:
        """Retrieves the list of messages from the conversation."""
        messages = self.data.get("messages", [])
        logger.info(f"Total messages loaded: {len(messages)}")
        return messages

    def get_metadata(self) -> Dict[str, Any]:
        """Retrieves metadata of the chat group or conversation."""
        metadata = {key: self.data.get(key, "") for key in ["name", "type", "id"]}
        logger.info(f"Retrieved metadata: {metadata}")
        return metadata
