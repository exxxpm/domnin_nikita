import logging
import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

logging.basicConfig(level=logging.INFO)


class SymmetricAlgs:
    """
      A class for symmetric cryptography operations.

      This class provides methods for generating symmetric keys,
      encrypting, and decrypting data using symmetric encryption algorithms.
      """
    key_length = 128

    def generate_symmetric_key(self) -> bytes:
        """
        Generate and return a symmetric key.

        :return: Symmetric key in bytes.
        """
        return os.urandom(self.key_length // 8)

    @staticmethod
    def encrypt_data(symmetric_key: bytes, plaintext_data: bytes) -> bytes:
        """
        Encrypt the plaintext data using the provided symmetric key.
        :param symmetric_key: Symmetric key in bytes.
        :param plaintext_data: Data to encrypt in bytes.
        :return: Encrypted data in bytes.
        Returns:
            object:
        """
        try:
            initialization_vector = os.urandom(16)
            cipher = Cipher(algorithms.SM4(symmetric_key), modes.CBC(initialization_vector))
            encryptor = cipher.encryptor()
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(plaintext_data) + padder.finalize()
            encrypted_data = initialization_vector + encryptor.update(padded_data) + encryptor.finalize()
            return encrypted_data

        except Exception as encryption_error:
            logging.error(f"Encryption error: {encryption_error}")

    @staticmethod
    def decrypt_data(symmetric_key: bytes, encrypted_data: bytes) -> bytes:
        """
        Decrypt the encrypted data using the provided symmetric key.
        :param symmetric_key: Symmetric key in bytes.
        :param encrypted_data: Encrypted data in bytes.
        :return: Decrypted data in bytes.
        """
        try:
            initialization_vector = encrypted_data[:16]
            encrypted_payload = encrypted_data[16:]
            cipher = Cipher(algorithms.SM4(symmetric_key), modes.CBC(initialization_vector))
            decryptor = cipher.decryptor()
            decrypted_data = decryptor.update(encrypted_payload) + decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()
            plaintext_data = unpadder.update(decrypted_data) + unpadder.finalize()
            return plaintext_data

        except Exception as decryption_error:
            logging.error(f"Decryption error: {decryption_error}")