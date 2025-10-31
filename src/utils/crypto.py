import hashlib
import base64
from cryptography.fernet import Fernet

def derive_fernet_key_from_level(global_secret: str, level: int) -> bytes:

    if not isinstance(global_secret, str):
        raise TypeError("global_secret deve ser uma string")
    if not isinstance(level, int):
        raise TypeError("level deve ser um inteiro")

    data = f"{global_secret}-{level}".encode("utf-8")
    digest = hashlib.sha256(data).digest()

    key = base64.urlsafe_b64encode(digest)
    return key
