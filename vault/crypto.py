from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

def derive_key(master_password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    key = kdf.derive(master_password.encode())
    return base64.urlsafe_b64encode(key)

def encrypt_password(plain_password: str, master_password: str, salt: bytes) -> bytes:
    key = derive_key(master_password, salt)
    f = Fernet(key)
    token = f.encrypt(plain_password.encode())
    return token

def decrypt_password(encrypted_password: bytes, master_password: str, salt: bytes) -> str:
    key = derive_key(master_password, salt)
    f = Fernet(key)
    plain = f.decrypt(encrypted_password)
    return plain.decode()