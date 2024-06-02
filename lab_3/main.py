import argparse

from system import HybridEncryptionManager
from algorithms.symmetric_algs import SymmetricAlgs
from algorithms.asymmetric_algs import AsymmetricAlgs
from helpers.file_helper import FileHelper

from assets.constants import FILE_PATH, MODES_WORK


def load_paths(file_path):
    file_manager = FileHelper(file_path)
    return file_manager.load_json()


def add_arguments(parser, paths):
    arguments = {
        '-mode': {'dest': 'mode', 'type': int, 'help': '1 - Generate keys, 2 - Encrypt text, 3 - Decrypt text'},
        '-text': {'dest': 'original_text', 'type': str, 'default': paths["original_text"],
                  'help': 'Path of the input txt file with text'},
        '-public_key': {'dest': 'asymmetric_public_key', 'type': str, 'default': paths["asymmetric_public_key"],
                        'help': 'Path of the public pem file with key'},
        '-private_key': {'dest': 'asymmetric_private_key', 'type': str, 'default': paths["asymmetric_private_key"],
                         'help': 'Path of the private pem file with key'},
        '-sym_key': {'dest': 'symmetric_key', 'type': str, 'default': paths["symmetric_key"],
                     'help': 'Path of the symmetric txt file with key'},
        '-enc_path': {'dest': 'encrypted_text', 'type': str, 'default': paths["encrypted_text"],
                      'help': 'Path of the txt file with encrypted text'},
        '-dec_path': {'dest': 'decrypted_text', 'type': str, 'default': paths["decrypted_text"],
                      'help': 'Path of the txt file with decrypted text'}
    }

    for arg, options in arguments.items():
        parser.add_argument(arg, **options)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Hybrid encryption/decryption system')
    paths = load_paths(FILE_PATH)
    add_arguments(parser, paths)
    return parser.parse_args()


def main():
    args = parse_arguments()

    symmetric_alg = SymmetricAlgs()
    asymmetric_alg = AsymmetricAlgs(args.asymmetric_private_key, args.asymmetric_public_key)

    hybrid_system = HybridEncryptionManager(
        args.original_text,
        args.symmetric_key,
        args.encrypted_text,
        args.decrypted_text,
        symmetric_alg,
        asymmetric_alg
    )

    match MODES_WORK[args.mode]:
        case 'GENERATE_KEYS':
            hybrid_system.generate_and_store_keys()
        case 'ENCRYPT_TEXT':
            hybrid_system.encrypt_file_text()
        case 'DECRYPT_TEXT':
            hybrid_system.decrypt_file_text()


if __name__ == "__main__":
    main()
