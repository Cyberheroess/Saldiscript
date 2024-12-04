from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
import base64

def generate_rsa_keypair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_data_with_public_key(data, public_key):
    key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key)
    encrypted_data = cipher.encrypt(data.encode())
    return base64.b64encode(encrypted_data).decode()

def decrypt_data_with_private_key(encrypted_data, private_key):
    encrypted_data = base64.b64decode(encrypted_data)
    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data.decode()

if __name__ == "__main__":
    private_key, public_key = generate_rsa_keypair()

    data = "This is a sensitive payload"
    encrypted_data = encrypt_data_with_public_key(data, public_key)
    print(f"Encrypted Data: {encrypted_data}")

    decrypted_data = decrypt_data_with_private_key(encrypted_data, private_key)
    print(f"Decrypted Data: {decrypted_data}")
