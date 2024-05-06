import json
from scipy.special import erfc
from mpmath import gammainc
import numpy as np

from constants import BLOCK_LENGTH, PI_ARRAY, FILE_PATH


def read_json(file_path: str) -> dict:
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


def frequency_bit_test(sequence: str) -> float | None:
    """
    Perform a frequency bit test on the input sequence.

    Args:
        sequence (str): Input bit sequence.

    Returns:
        float: p-value of the test.
    """
    try:
        sequence_length = len(sequence)
        scaled_sum = np.sum(np.where(np.array(list(sequence)) == '1', 1, -1)) / np.sqrt(sequence_length)
        p_value = erfc(abs(scaled_sum) / np.sqrt(2))
        return p_value
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def consecutive_bits_test(sequence: str) -> float | None:
    """
    Perform a consecutive bits test on the input sequence.

    Args:
        sequence (str): Input bit sequence.

    Returns:
        float: p-value of the test.
    """
    try:
        sequence_length = len(sequence)
        proportion_of_ones = sequence.count("1") / sequence_length
        if abs(proportion_of_ones - 0.5) >= 2 / np.sqrt(sequence_length):
            return 0
        differing_pairs = sum(1 if sequence[i] != sequence[i + 1] else 0 for i in range(sequence_length - 1))
        p_value = erfc(
            (abs(differing_pairs - 2 * sequence_length * proportion_of_ones * (1 - proportion_of_ones)))
            / (2 * np.sqrt(2 * sequence_length) * proportion_of_ones * (1 - proportion_of_ones))
        )
        return p_value
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def long_sequence_units_test(sequence: str) -> float | None:
    """
    Perform a long sequence units test on the input sequence.

    Args:
        sequence (str): Input bit sequence.

    Returns:
        float: p-value of the test.
    """
    try:
        blocks = [sequence[i: i + BLOCK_LENGTH] for i in range(0, len(sequence), BLOCK_LENGTH)]
        count_statistics = {"v1": 0, "v2": 0, "v3": 0, "v4": 0}

        for block in blocks:
            max_ones = 0
            current_ones = 0

            for bit in block:
                if bit == "1":
                    current_ones += 1
                    max_ones = max(max_ones, current_ones)
                else:
                    current_ones = 0

            count_statistics[f"v{min(max_ones, 4)}"] += 1

        chi_square = sum(((count_statistics[f"v{i + 1}"] - 16 * PI_ARRAY[i]) ** 2) / (16 * PI_ARRAY[i]) for i in range(4))
        p_value = gammainc(1.5, chi_square / 2)
        return p_value

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def main() -> None:
    """
    Main function to perform statistical tests on bit sequences.
    """
    data = read_json(FILE_PATH)
    for language, sequence in data.items():
        freq_bit_test_p_value = frequency_bit_test(sequence)
        consecutive_bits_test_p_value = consecutive_bits_test(sequence)
        long_sequence_units_test_p_value = long_sequence_units_test(sequence)

        print("===================================")
        print(f" Language: {language} ")
        print("===================================")
        print(f" p-value of frequency bit test: {freq_bit_test_p_value} ")
        print(f" p-value of consecutive bits test: {consecutive_bits_test_p_value} ")
        print(f" p-value of long sequence units test: {long_sequence_units_test_p_value} \n")


if __name__ == "__main__":
    main()
