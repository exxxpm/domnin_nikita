import logging

from algorithms.asymmetric_algs import AsymmetricAlgs
from algorithms.symmetric_algs import SymmetricAlgs
from helpers.file_helper import FileHelper

logging.basicConfig(level=logging.INFO)


class HybridEncryptionManager:
    """
    Manages hybrid encryption operations using symmetric and asymmetric cryptographic algorithms.
    """

    def __init__(self, text_file_path: str, sym_key_file_path: str,
                 encrypted_file_path: str, decrypted_file_path: str,
                 sym_crypto: SymmetricAlgs, asym_crypto: AsymmetricAlgs) -> None:
        """
        Initializes the HybridEncryptionManager with the paths for text, keys, and encrypted files,
        as well as instances of symmetric and asymmetric cryptographic classes.

        :param text_file_path: Path to the plaintext file.
        :param sym_key_file_path: Path to the symmetric key file.
        :param encrypted_file_path: Path to the file where encrypted text will be stored.
        :param decrypted_file_path: Path to the file where decrypted text will be stored.
        :param sym_crypto: Instance for symmetric cryptography operations.
        :param asym_crypto: Instance for asymmetric cryptography operations.
        """
        self.text_file_path = text_file_path
        self.sym_key_file_path = sym_key_file_path
        self.encrypted_file_path = encrypted_file_path
        self.decrypted_file_path = decrypted_file_path
        self.sym_crypto = sym_crypto
        self.asym_crypto = asym_crypto

    def generate_and_store_keys(self) -> None:
        """
        Generates a symmetric key and an asymmetric key pair, encrypts the symmetric key with the public key,
        and stores all keys in their respective files.
        """
        try:
            symmetric_key = self.sym_crypto.generate_symmetric_key()
            private_key, public_key = self.asym_crypto.generate_key_pair(2048)

            private_file = FileHelper(self.asym_crypto.private_key_filepath)
            private_file.save_bytes(AsymmetricAlgs.get_private_key_bytes(private_key))

            public_file = FileHelper(self.asym_crypto.public_key_filepath)
            public_file.save_bytes(AsymmetricAlgs.get_public_key_bytes(public_key))

            encrypted_symmetric_key = self.asym_crypto.encrypt(public_key, symmetric_key)
            sym_key_file = FileHelper(f"{self.sym_key_file_path[:-4]}_{self.sym_crypto.key_length}.txt")
            sym_key_file.save_bytes(encrypted_symmetric_key)

            logging.info("Keys have been successfully generated and stored in files.")
        except Exception as ex:
            logging.error(f"An error occurred during key generation and storage: {ex}")

    def encrypt_file_text(self) -> None:
        """
        Encrypts the content of the plaintext file using the symmetric key and stores the encrypted text in a file.
        """
        try:
            sym_key_file = FileHelper(f"{self.sym_key_file_path[:-4]}_{self.sym_crypto.key_length}.txt")
            encrypted_symmetric_key = sym_key_file.load_bytes()
            private_key = FileHelper(self.asym_crypto.private_key_filepath)
            private_key = private_key.load_bytes()
            private_key = AsymmetricAlgs.get_private_key_from_bytes(private_key)
            symmetric_key = self.asym_crypto.decrypt(
                private_key, encrypted_symmetric_key)
            text_file = FileHelper(self.text_file_path)
            plaintext = bytes(text_file.read_text('utf-8'), "UTF-8")
            encrypted_text = self.sym_crypto.encrypt_data(symmetric_key, plaintext)
            encrypted_file = FileHelper(self.encrypted_file_path)
            encrypted_file.save_bytes(encrypted_text)
            logging.info("Text file has been successfully encrypted and stored.")
        except Exception as ex:
            logging.error(f"An error occurred during text file encryption: {ex}")

    def decrypt_file_text(self) -> None:
        """
        Decrypts the content of the encrypted text file using the symmetric key and stores the decrypted text in a file.
        """
        try:
            sym_key_file = FileHelper(f"{self.sym_key_file_path[:-4]}_{self.sym_crypto.key_length}.txt")
            encrypted_symmetric_key = sym_key_file.load_bytes()
            private_key = FileHelper(self.asym_crypto.private_key_filepath)
            private_key = private_key.load_bytes()
            private_key = AsymmetricAlgs.get_private_key_from_bytes(private_key)
            symmetric_key = self.asym_crypto.decrypt(
                private_key, encrypted_symmetric_key)
            encrypted_file = FileHelper(self.encrypted_file_path)
            encrypted_text = bytes(encrypted_file.load_bytes())
            decrypted_text = self.sym_crypto.decrypt_data(symmetric_key, encrypted_text)
            decrypted_file = FileHelper(self.decrypted_file_path)
            decrypted_file.save_bytes(decrypted_text)
            logging.info("Text file has been successfully decrypted and stored.")
        except Exception as ex:
            logging.error(f"An error occurred during text file decryption: {ex}")
