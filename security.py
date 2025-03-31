from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
import os

def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return {
        "private_key": private_pem.decode(),
        "public_key": public_pem.decode()
    }

def encrypt_message(message, recipient_public_key_pem):
    recipient_public_key = serialization.load_pem_public_key(recipient_public_key_pem.encode())

    aes_key = os.urandom(32)
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(aes_key), modes.GCM(iv))
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(message.encode()) + encryptor.finalize()

    encrypted_aes_key = recipient_public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return base64.b64encode(encrypted_aes_key).decode(), base64.b64encode(encrypted_message).decode()

def decrypt_message(encrypted_message, encrypted_aes_key, recipient_private_key_pem):
    recipient_private_key = serialization.load_pem_private_key(recipient_private_key_pem.encode(), password=None)

    aes_key = recipient_private_key.decrypt(
        base64.b64decode(encrypted_aes_key),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    cipher = Cipher(algorithms.AES(aes_key), modes.GCM(os.urandom(16)))
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(base64.b64decode(encrypted_message)) + decryptor.finalize()

    return decrypted_message.decode()
