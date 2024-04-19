from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

def pad_key(key):
    # Pad the key with zeros until it reaches 16 characters
    while len(key) < 16:
        key += '0'
    return key[:16]  # Truncate the key to 16 characters if it exceeds 16

def encrypt_text(Key, text):
    key=pad_key(Key)
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(text.encode(), AES.block_size))
    ciphertext = b64encode(ciphertext).decode()
    return ciphertext

def decrypt_text(Key, ciphertext):
    key=pad_key(Key)
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    decrypted_text = unpad(cipher.decrypt(b64decode(ciphertext.encode())), AES.block_size).decode()
    return decrypted_text

