import base64
import hashlib
from cryptography.fernet import Fernet

from app.constants import config
from .logger import logger

# 1. Hash the secret to make it 32 bytes
hashed = hashlib.sha256(str(config["HASH_KEY"]).encode()).digest()

# 2. Base64 encode the 32-byte hash to make it a valid Fernet key
fernet_key = base64.urlsafe_b64encode(hashed)

# Now create cipher
cipher = Fernet(fernet_key)

def encrypt_string(string):
    """
    Encrypt a string using Fernet
    """
    encode = cipher.encrypt(string.encode()).decode()
    logger.debug({
        "message": "(encrypt_string)Encrypted string",
        "string": string,
        "encode": encode
    })

    return encode

def decrypt_string(string):
    """
    Decrypt a string using Fernet
    """
    decode = cipher.decrypt(string.encode()).decode()
    logger.debug({
        "message": "(decrypt_string)Decrypted string",
        "string": string,
        "decode": decode
    })
    
    return decode
