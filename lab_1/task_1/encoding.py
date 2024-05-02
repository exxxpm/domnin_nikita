import os
import json

from constants import RANDOM_ALPHABET_SQUARE, UNUSUAL_MARKS, FILE_PATH


def load_json(file_path: str) -> dict:
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
        print("File not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON data.")
    except Exception as e:
        print(f"An error occurred: {e}")


def encrypt_message(message: str, square: list) -> str:
    """
    Encrypt a message using a Polybius square.

    Args:
        message (str): The message to be encrypted.
        square (list): The Polybius square.

    Returns:
        str: The encrypted message.
    """
    encrypted_message = ""
    try:
        for char in message:
            if char.lower() in UNUSUAL_MARKS:
                encrypted_message += char
            else:
                for i in range(len(square)):
                    for j in range(len(square[i])):
                        if char.lower() == square[i][j]:
                            encrypted_message += f"({i + 1}{j + 1})"
                            break

    except Exception as e:
        print("An error occurred:", e)
        return ""
    return encrypted_message


def main() -> None:
    """
    Main function for file path operations.
    """
    data = load_json(FILE_PATH)
    if data:
        directory = data.get("directory", "")
        source_file = data.get("source_text", "")
        encrypted_file = data.get("encrypted_text", "")

        if directory and source_file and encrypted_file:
            try:
                with open(
                    os.path.join(directory, source_file), "r", encoding="utf-8"
                ) as file:
                    message = file.read()
                    encrypted_message = encrypt_message(message, RANDOM_ALPHABET_SQUARE)

                with open(
                    os.path.join(directory, encrypted_file), "w", encoding="utf-8"
                ) as file:
                    file.write(encrypted_message)

                print("Message successfully encrypted and saved to file.")
            except FileNotFoundError:
                print("One of the files not found.")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("Failed to get file paths from JSON data.")
    else:
        print("Failed to read data from JSON file.")


if __name__ == "__main__":
    main()
