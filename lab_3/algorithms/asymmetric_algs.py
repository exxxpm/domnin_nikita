import logging

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key)


logging.basicConfig(level=logging.INFO)


class AsymmetricAlgs:
    """
    A class for asymmetric cryptography operations.

    This class provides methods for generating key pairs,
    encrypting, and decrypting data using asymmetric encryption algorithms.
    """

    def __init__(self, private_key_filepath: str, public_key_filepath: str) -> None:
        """
        Initialize AsymmetricCryptography object with paths to the private and public key files.

        :param private_key_filepath: Path to the private key file.
        :param public_key_filepath: Path to the public key file.
        """
        self.private_key_filepath = private_key_filepath
        self.public_key_filepath = public_key_filepath

    @staticmethod
    def generate_key_pair(key_size: int) -> tuple:
        """
        Generate an RSA key pair.

        :param key_size: The size of the RSA key in bits.

        :return: A tuple containing the private and public keys.
        """
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def get_private_key_bytes(private_key: rsa.RSAPrivateKey) -> bytes:
        """
        Returns bytes of private key.

        :param private_key: The RSA private key used for decryption.

        :return: bytes
        """
        try:
            return private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                             format=serialization.PrivateFormat.TraditionalOpenSSL,
                                             encryption_algorithm=serialization.NoEncryption())
        except Exception as ex:
            logging.error(f"An error occurred while trying to retrieve the bytes of the private key: {ex}")

    @staticmethod
    def get_public_key_bytes(public_key: rsa.RSAPublicKey) -> bytes:
        """
        Returns bytes of public key.

        :param public_key: The RSA public key used for decryption.

        :return: bytes
        """
        try:
            return public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                           format=serialization.PublicFormat.SubjectPublicKeyInfo)
        except Exception as e:
            logging.error(f"Error in try to get bytes of public key: {e}")

    @staticmethod
    def get_public_key_from_bytes(public_key_bytes: bytes) -> rsa.RSAPublicKey:
        """
        Returns public key parsed from bytes.
        :param public_key_bytes: RSA public key in bytes.
        :return: RSA public key
        """
        try:
            return load_pem_public_key(public_key_bytes)
        except Exception as ex:
            logging.error(f"An unsuccessful attempt to decrypt the bytes of the public key: {ex}")

    @staticmethod
    def get_private_key_from_bytes(private_key_bytes: bytes) -> rsa.RSAPrivateKey:
        """
        Returns private key parsed from bytes.
        :param private_key_bytes: RSA private key in bytes.
        :return: RSA public key
        """
        try:
            return load_pem_private_key(private_key_bytes, password=None, )
        except Exception as ex:
            logging.error(f"An unsuccessful attempt to decrypt the bytes of the private key: {ex}")

    @staticmethod
    def encrypt(public_key: rsa.RSAPublicKey, plaintext: bytes) -> bytes:
        """
        Encrypt plaintext using the provided public key.

        :param public_key: The RSA public key used for encryption.
        :param plaintext: The plaintext to be encrypted.

        :return: The ciphertext produced by the encryption process.
        """
        return public_key.encrypt(
            plaintext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    @staticmethod
    def decrypt(private_key: rsa.RSAPrivateKey, ciphertext: bytes) -> bytes:
        """
        Decrypt ciphertext using the provided private key.

        :param private_key: The RSA private key used for decryption.
        :param ciphertext: The ciphertext to be decrypted.

        :return: The plaintext produced by the decryption process.
        """
        return private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
