import logging

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes

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

    def save_private_key(self, private_key: rsa.RSAPrivateKey) -> None:
        """
        Serialize the private key and save it to a file.

        :param private_key: The private key to serialize and save.
        """
        try:
            with open(self.private_key_filepath, 'wb') as private_key_file:
                private_key_file.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                ))
        except Exception as error:
            logging.error(f"Error in saving private key - {error}")

    def save_public_key(self, public_key: rsa.RSAPublicKey) -> None:
        """
        Serialize the public key and save it to a file.

        :param public_key: The public key to serialize and save.
        """
        try:
            with open(self.public_key_filepath, 'wb') as public_key_file:
                public_key_file.write(public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))
        except Exception as error:
            logging.error(f"Error in saving public key - {error}")

    def load_private_key(self) -> rsa.RSAPrivateKey:
        """
        Deserialize the private key from a file and return it.

        :return: The deserialized private key.
        """
        try:
            with open(self.private_key_filepath, 'rb') as private_key_file:
                return serialization.load_pem_private_key(private_key_file.read(), password=None)
        except Exception as error:
            logging.error(f"Error in loading private key - {error}")

    def load_public_key(self) -> rsa.RSAPublicKey:
        """
        Deserialize the public key from a file and return it.

        :return: The deserialized public key.
        """
        try:
            with open(self.public_key_filepath, 'rb') as public_key_file:
                return serialization.load_pem_public_key(public_key_file.read())
        except Exception as error:
            logging.error(f"Error in loading public key - {error}")

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
