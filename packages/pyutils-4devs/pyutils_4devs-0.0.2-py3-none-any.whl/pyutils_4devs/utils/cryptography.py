from .file import File
from pyutils_4devs.decorators.cryptography import fernet_key_validator

import bcrypt
from cryptography.fernet import Fernet


class Cryptography:
    def __init__(self, salt: bytes = bcrypt.gensalt(), fernet_key: bytes = None):
        self.salt = salt
        self.fernet_key = fernet_key

    def encrypt_password(self, pw: bytes) -> bytes:
        return bcrypt.hashpw(pw, self.salt)

    def check_password(self, pw: bytes, hashed_string: bytes) -> bool:
        return bcrypt.checkpw(pw, hashed_string)

    def set_fernet_key(self):
        self.fernet_key = Fernet.generate_key()
        File.save_file('fernet_key.key', self.fernet_key)

    @fernet_key_validator
    def encrypt_file(self, filepath: str) -> str:
        fernet = Fernet(self.fernet_key)

        new_filepath = 'encrypted_' + filepath
        original_file = File.read_file(filepath)
        encrypted_file = fernet.encrypt(original_file)
        File.save_file(new_filepath, encrypted_file)
        return new_filepath

    @fernet_key_validator
    def decrypt_file(self, filepath: str) -> None:
        fernet = Fernet(self.fernet_key)

        encrypted_file = File.read_file(filepath)
        decrypted_file = fernet.decrypt(encrypted_file)
        File.save_file(filepath, decrypted_file)
