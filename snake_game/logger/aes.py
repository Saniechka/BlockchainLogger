from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii
import json
import os
def getAESKey(username):
    # Tworzenie ścieżki do pliku klucza AES dla danego użytkownika
    aes_key_file_path = os.path.join('keys', f"{username}_aes_key.txt")

    # Sprawdzenie, czy plik z kluczem AES dla danego użytkownika istnieje
    if not os.path.exists(aes_key_file_path):
        print(f"Plik z kluczem AES dla użytkownika {username} nie istnieje.")
        return None

    # Wczytanie klucza AES z pliku
    with open(aes_key_file_path, 'r') as file:
        aes_key = file.read().strip()

    return aes_key


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


def save_aes_key(aes_key, filename):
    # Zapisywanie klucza AES do pliku w postaci szesnastkowej (hex)
    with open(filename, "w") as aes_key_file:
        aes_key_file.write(aes_key.hex())  # Konwersja bajtów na ciąg znaków szesnastkowych i zapisanie do pliku

