from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import os


def generate_rsa_key_pair(key_size=2048):
    """
    Genera un par de claves RSA (pública y privada)

    Args:
        key_size (int): Tamaño de la clave en bits

    Returns:
        tuple: (clave_privada, clave_publica) como objetos RSA
    """
    private_key = RSA.generate(key_size)
    public_key = private_key.publickey()

    return private_key, public_key


def save_rsa_keys(private_key, public_key, private_path="private.pem", public_path="public.pem"):
    """
    Guarda las claves RSA en archivos PEM

    Args:
        private_key: Objeto RSA de clave privada
        public_key: Objeto RSA de clave pública
        private_path (str): Ruta para guardar la clave privada
        public_path (str): Ruta para guardar la clave pública
    """
    # Guardar clave privada
    with open(private_path, "wb") as f:
        f.write(private_key.export_key("PEM"))

    # Guardar clave pública
    with open(public_path, "wb") as f:
        f.write(public_key.export_key("PEM"))


def load_rsa_public_key(public_path="public.pem"):
    """
    Carga una clave pública RSA desde un archivo

    Args:
        public_path (str): Ruta del archivo de clave pública

    Returns:
        Objeto RSA con la clave pública
    """
    with open(public_path, "rb") as f:
        public_key = RSA.import_key(f.read())

    return public_key


def load_rsa_private_key(private_path="private.pem"):
    """
    Carga una clave privada RSA desde un archivo

    Args:
        private_path (str): Ruta del archivo de clave privada

    Returns:
        Objeto RSA con la clave privada
    """
    with open(private_path, "rb") as f:
        private_key = RSA.import_key(f.read())

    return private_key


def encrypt_rsa(data, public_key):
    """
    Encripta datos usando RSA

    Args:
        data (bytes): Datos a encriptar
        public_key: Objeto RSA de clave pública

    Returns:
        bytes: Datos encriptados
    """
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_data = cipher.encrypt(data)

    return encrypted_data


def decrypt_rsa(encrypted_data, private_key):
    """
    Desencripta datos usando RSA

    Args:
        encrypted_data (bytes): Datos encriptados
        private_key: Objeto RSA de clave privada

    Returns:
        bytes: Datos desencriptados
    """
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_data = cipher.decrypt(encrypted_data)

    return decrypted_data