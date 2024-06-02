import json
import logging

logging.basicConfig(level=logging.INFO)


class FileHelper:
    def __init__(self, path: str) -> None:
        self.path = path

    def save_bytes(self, data: bytes) -> None:
        """
        Save bytes to a file.
        :param data: The bytes to be saved.
        """
        try:
            with open(self.path, 'wb') as file:
                file.write(data)
            logging.info(f"Successfully saved bytes to {self.path}")
        except Exception as ex:
            logging.error(f"Failed to save bytes to {self.path} - {ex}")

    def load_bytes(self) -> bytes:
        """
        Load bytes from a file.
        :return: The loaded bytes.
        """
        try:
            with open(self.path, 'rb') as file:
                return file.read()
        except Exception as ex:
            logging.error(f"Failed to load bytes from {self.path} - {ex}")
            return b''

    def read_text(self, encoding: str = 'utf-8') -> str:
        """
        Read text from a file.
        :param encoding: The encoding of the text file. Defaults to 'utf-8'.
        :return: The content of the text file.
        """
        try:
            with open(self.path, 'r', encoding=encoding) as file:
                return file.read()
        except Exception as ex:
            logging.error(f"Failed to read text from {self.path} - {ex}")
            return ""

    def write_text(self, text: str, encoding: str = 'utf-8') -> None:
        """
        Write text to a file.
        :param text: The text to write to the file.
        :param encoding: The encoding of the text file. Defaults to 'utf-8'.
        """
        try:
            with open(self.path, 'w', encoding=encoding) as file:
                file.write(text)
            logging.info(f"Successfully wrote text to {self.path}")
        except Exception as ex:
            logging.error(f"Failed to write text to {self.path} - {ex}")

    def load_json(self) -> dict:
        """
        Load JSON data from a file.
        :return: The loaded JSON data as a dictionary.
        """
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as ex:
            logging.error(f"Failed to load JSON from {self.path} - {ex}")
            return {}

    def save_json(self, data: dict) -> None:
        """
        Save JSON data to a file.
        :param data: The dictionary to be saved as JSON.
        """
        try:
            with open(self.path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            logging.info(f"Successfully saved JSON to {self.path}")
        except Exception as ex:
            logging.error(f"Failed to save JSON to {self.path} - {ex}")
