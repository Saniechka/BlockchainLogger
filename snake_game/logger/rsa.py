from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization


def generate_private_key():
# Generowanie kluczy RSA
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

def generate_public_key(private_key):
    public_key = private_key.public_key()





# Zapisywanie klucza prywatnego
with open("private_key.pem", "wb") as private_key_file:
    private_key_file.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

# Zapisywanie klucza publicznego
with open("public_key.pem", "wb") as public_key_file:
    public_key_file.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )



def get_private_key():
    with open("private_key.pem", "rb") as private_key_file:
        private_key = serialization.load_pem_private_key(
            private_key_file.read(),
            password=None,  # Tu wpisz hasło, jeśli klucz prywatny jest zabezpieczony
            backend=default_backend()
        )
def get_public_key():
    with open("public_key.pem", "rb") as public_key_file:
        public_key = serialization.load_pem_public_key(
            public_key_file.read(),
            backend=default_backend()
        )


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



# Lista wiadomości
messages = [b"Hello, RSA!", b"This is a test message.", b"Another message."]

# Kodowanie i odczytywanie wiadomości z listy
for message in messages:
    # Kodowanie wiadomości
    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(ciphertext)

   

    print("Original message:", message.decode())
    print("Decrypted message:", plaintext.decode())
    print("-" * 20)