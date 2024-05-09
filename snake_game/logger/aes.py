from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii
import json

def getAESKey():
    with open('config.json', 'r') as file:
        config_data = json.load(file)
    return config_data.get('AESkey', None)

def generateKey():
    key = get_random_bytes(16)
    return key

def aesDecrypt(encrypted_hex, key, nonce, tag):
    ciphertext = binascii.unhexlify(encrypted_hex)
    nonce = binascii.unhexlify(nonce)
    tag = binascii.unhexlify(tag)
    key = binascii.unhexlify(key)
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    return data

def aesEncrypt(data, key):
    key_bytes = binascii.unhexlify(key)
    cipher = AES.new(key_bytes, AES.MODE_EAX)
    nonce = cipher.nonce  
    ciphertext, tag = cipher.encrypt_and_digest(data)
    
    
    encrypted_hex_str = ciphertext.hex()
    nonce_str = nonce.hex()
    tag_str = tag.hex()
    
    return encrypted_hex_str, nonce_str, tag_str
'''
    # Generowanie klucza AES
key = generateKey()

# Wiadomość do zaszyfrowania
message = b"Hello, AESk!"

# Szyfrowanie wiadomości
encrypted_hex, nonce, tag = aesEncrypt(message, key)

# Konwersja wartości do stringa i połączenie ich kropkami
result_string = ".".join([encrypted_hex.hex(), nonce.hex(), tag.hex()])

# Wydrukowanie wyniku
print("Encrypted message:", result_string)'''
