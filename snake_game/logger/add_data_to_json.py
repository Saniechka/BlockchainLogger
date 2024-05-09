def generate_rsa_keys(username):
    # Generowanie kluczy RSA
    private_key = generate_private_key()
    public_key = generate_public_key(private_key)
    
    # Zapisywanie kluczy RSA do plików PEM
    save_private_key(private_key, f"{username}_private_key.pem")
    save_public_key(public_key, f"{username}_public_key.pem")

    # Generowanie i zapisywanie klucza AES do pliku
    aes_key = generateKey()
    save_aes_key(aes_key, f"{username}_aes_key.txt")
    
    return new_entry

def save_aes_key(aes_key, filename):
    # Zapisywanie klucza AES do pliku
    with open(filename, "w") as aes_key_file:
        aes_key_file.write(aes_key)


