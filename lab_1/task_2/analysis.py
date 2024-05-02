import os
import json

from collections import Counter, defaultdict
from constants import FILE_PATH


def load_json_data(file_path: str) -> dict:
    """
    Load JSON data from a file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Loaded JSON data.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Data file not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON data.")
    except Exception as e:
        print(f"An error occurred: {e}")


def read_text_file(file_path: str) -> str:
    """
    Read text from a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Text read from the file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print("File not found.")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""


def calculate_character_frequencies(text: str) -> dict:
    """
    Calculate the frequency of each character in the text, including tabs.

    Args:
        text (str): Input text.

    Returns:
        dict: Character frequencies.
    """
    try:
        frequencies = Counter(text)
        return frequencies
    except Exception as e:
        print(f"An error occurred while calculating character frequencies: {e}")
        return {}


def main():
    try:
        json_data = load_json_data(FILE_PATH)
        if json_data:
            folder_path = json_data.get("directory")
            input_file = json_data.get("source_text")

            input_file_path = f"{folder_path}/{input_file}"

            text = read_text_file(input_file_path)
            if text:
                frequencies = calculate_character_frequencies(text)

                total_chars = sum(frequencies.values())

                sorted_frequencies = sorted(
                    frequencies.items(), key=lambda x: x[1], reverse=True
                )

                for char, freq in sorted_frequencies:
                    decimal_freq = freq / total_chars
                    print(f"Character '{char}': {decimal_freq:.4f}")
    except Exception as e:
        print(f"An error occurred in the main function: {e}")


if __name__ == "__main__":
    main()
