import jwt
import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# En producción, esta clave debería estar en un archivo .env seguro
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secreta")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_DELTA = datetime.timedelta(hours=1)  # Token válido por 1 hora


def generate_jwt(identity, additional_claims=None):
    """
    Genera un token JWT para un usuario

    Args:
        identity (str): Identificador del usuario (username)
        additional_claims (dict, optional): Claims adicionales para incluir en el token

    Returns:
        str: Token JWT generado
    """
    payload = {
        'sub': identity,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + JWT_EXPIRATION_DELTA
    }

    # Agregar claims adicionales si se proporcionan
    if additional_claims:
        payload.update(additional_claims)

    # Generar token
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    return token


def decode_jwt(token):
    """
    Decodifica y verifica un token JWT

    Args:
        token (str): Token JWT a verificar

    Returns:
        dict: Payload del token si es válido
        None: Si el token no es válido
    """
    try:
        # Decodificar y verificar token
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # Token expirado
        return None
    except jwt.InvalidTokenError:
        # Token inválido
        return None


def verify_jwt(token):
    """
    Verifica si un token JWT es válido

    Args:
        token (str): Token JWT a verificar

    Returns:
        bool: True si el token es válido, False en caso contrario
    """
    return decode_jwt(token) is not None


def get_identity_from_token(token):
    """
    Obtiene la identidad (username) de un token JWT

    Args:
        token (str): Token JWT

    Returns:
        str: Identidad (username) si el token es válido
        None: Si el token no es válido
    """
    payload = decode_jwt(token)

    if payload:
        return payload.get('sub')

    return None