from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def encrypt_data(data: bytes, private_key: bytes) -> bytes:
    """Encrypt data using RSA private key."""
    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key)
    return cipher.encrypt(data)

def decrypt_data(data: bytes, private_key: bytes) -> bytes:
    """Decrypt data using RSA private key."""
    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key)
    return cipher.decrypt(data)
