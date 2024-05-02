import os
import json

from constants import FILE_PATH as JSON_FILE, DICTIONARY
from analysis import load_json_data, read_text_file


def decrypt_text(ciphertext: str, cipher: dict) -> str:
    """
    Decrypts the text using the given cipher.

    Parameters:
        ciphertext (str): The text to decrypt.
        cipher (dict): The decryption dictionary.

    Returns:
        str: The decrypted text.
    """
    try:
        decrypted_text = ""
        for char in ciphertext:
            decrypted_text += cipher.get(char, char)
        return decrypted_text
    except Exception as e:
        print(f"An error occurred during text decryption: {e}")
        return ""


def main() -> None:
    """
    Main function to decrypt text.

    Parameters:
        None

    Returns:
        None
    """
    try:
        json_data = load_json_data(JSON_FILE)
        if json_data:
            directory = json_data.get("directory", "")
            source_text = json_data.get("source_text", "")
            result_text = json_data.get("result_text", "")

            input_text_path = os.path.join(directory, source_text)
            output_text_path = os.path.join(directory, result_text)

            text = read_text_file(input_text_path)
            if text:
                decrypted_text = decrypt_text(text, DICTIONARY)
                if decrypted_text:
                    print(decrypted_text)
                    with open(output_text_path, "w", encoding="utf-8") as file:
                        file.write(decrypted_text)
                        print(f"Decrypted text saved to '{output_text_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
