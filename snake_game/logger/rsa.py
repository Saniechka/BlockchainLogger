from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from aes import generateKey, save_aes_key
import os



def generate_keys_rsa():
    private_key=generate_private_key()
    generate_public_key(private_key)
    save_private_key(private_key, 'private_key.pem')
    save_public_key(public_key, 'public_key.pem')



def generate_private_key():
# Generowanie kluczy RSA
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return private_key

def generate_public_key(private_key):
    public_key = private_key.public_key()
    return public_key





def save_private_key(private_key, filename):
    with open(filename, "wb") as private_key_file:
        private_key_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

def save_public_key(public_key, filename):
    with open(filename, "wb") as public_key_file:
        public_key_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )


def get_private_key(username):
    private_key_file_path = os.path.join('keys', f"{username}_private_key.pem")
    if not os.path.exists(private_key_file_path):
        print(f"Plik z kluczem prywatnym dla użytkownika {username} nie istnieje.")
        return None
    
    with open(private_key_file_path, "rb") as private_key_file:
        private_key = serialization.load_pem_private_key(
            private_key_file.read(),
            password=None,  # Tu wpisz hasło, jeśli klucz prywatny jest zabezpieczony
            backend=default_backend()
        )
    return private_key



def get_public_key(username):
    public_key_file_path = os.path.join('keys', f"{username}_public_key.pem")
    if not os.path.exists(public_key_file_path):
        print(f"Plik z kluczem publicznym dla użytkownika {username} nie istnieje.")
        return None
    
    with open(public_key_file_path, "rb") as public_key_file:
        public_key = serialization.load_pem_public_key(
            public_key_file.read(),
            backend=default_backend()
        )
    return public_key


def rsaDecrypt(ciphertext, private_key):
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext


def rsaEncrypt(message, public_key):
    # Kodowanie wiadomości
    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext
    

'''
def generate_all_keys(username):
    # Tworzenie folderu 'keys', jeśli nie istnieje
    if not os.path.exists('keys'):
        os.makedirs('keys')

    # Generowanie kluczy RSA
    private_key = generate_private_key()
    public_key = generate_public_key(private_key)
    
    # Zapisywanie kluczy RSA do folderu keys
    save_private_key(private_key, os.path.join('keys', f"{username}_private_key.pem"))
    save_public_key(public_key, os.path.join('keys', f"{username}_public_key.pem"))

    # Generowanie i zapisywanie klucza AES do folderu keys
    aes_key = generateKey()
    save_aes_key(aes_key, os.path.join('keys', f"{username}_aes_key.txt"))
    '''

def generate_all_keys(username):
    # Tworzenie folderu 'keys', jeśli nie istnieje
    if not os.path.exists('keys'):
        os.makedirs('keys')

    # Sprawdzenie, czy pliki z kluczami RSA i AES już istnieją
    rsa_private_key_file_path = os.path.join('keys', f"{username}_private_key.pem")
    rsa_public_key_file_path = os.path.join('keys', f"{username}_public_key.pem")
    aes_key_file_path = os.path.join('keys', f"{username}_aes_key.txt")
    
    if os.path.exists(rsa_private_key_file_path) and os.path.exists(rsa_public_key_file_path) and os.path.exists(aes_key_file_path):
        print(f"Pliki z kluczami RSA i AES dla użytkownika {username} już istnieją.")
        return

     # Generowanie kluczy RSA
    private_key = generate_private_key()
    public_key = generate_public_key(private_key)
    
    # Zapisywanie kluczy RSA do folderu keys
    save_private_key(private_key, os.path.join('keys', f"{username}_private_key.pem"))
    save_public_key(public_key, os.path.join('keys', f"{username}_public_key.pem"))

    # Generowanie i zapisywanie klucza AES do folderu keys
    aes_key = generateKey()
    save_aes_key(aes_key, os.path.join('keys', f"{username}_aes_key.txt"))
  





