from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os


def generate_aes_key(size=32):
    """
    Genera una clave AES-256 aleatoria (32 bytes)
    """
    return os.urandom(size)


def generate_iv():
    """
    Genera un vector de inicialización (IV) para AES
    """
    return os.urandom(16)  # AES block size


def encrypt_aes(plain_text, key, iv):
    """
    Encripta un texto usando AES-256 en modo CBC

    Args:
        plain_text (str): Texto plano a encriptar
        key (bytes): Clave AES de 32 bytes (256 bits)
        iv (bytes): Vector de inicialización de 16 bytes

    Returns:
        str: Texto encriptado en formato base64
    """
    # Aseguramos que el texto esté en bytes
    if isinstance(plain_text, str):
        plain_text = plain_text.encode('utf-8')

    # Crear el cipher AES en modo CBC con el IV
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Encriptamos con padding para asegurar múltiplos del tamaño de bloque
    padded_data = pad(plain_text, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)

    # Retornamos como string en base64
    return base64.b64encode(encrypted_data).decode('utf-8')


def decrypt_aes(encrypted_text, key, iv):
    """
    Desencripta un texto usando AES-256 en modo CBC

    Args:
        encrypted_text (str): Texto encriptado en formato base64
        key (bytes): Clave AES de 32 bytes (256 bits)
        iv (bytes): Vector de inicialización de 16 bytes

    Returns:
        str: Texto plano desencriptado
    """
    # Decodificamos el texto en base64
    if isinstance(encrypted_text, str):
        encrypted_data = base64.b64decode(encrypted_text)
    else:
        encrypted_data = base64.b64decode(encrypted_text.decode('utf-8'))

    # Crear el cipher AES en modo CBC con el IV
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Desencriptamos y eliminamos el padding
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    # Retornamos como string
    return decrypted_data.decode('utf-8')