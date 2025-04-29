import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from utils.config import LOG_LEVEL, LOG_FILE

# Asegurar que el directorio de logs exista
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Mapeo de niveles de log como string a constantes de logging
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

# Obtener el nivel de log configurado o usar INFO por defecto
LEVEL = LOG_LEVELS.get(LOG_LEVEL.upper(), logging.INFO)

# Configurar formato de logs
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Configurar manejador de archivo con rotación
file_handler = RotatingFileHandler(
    filename=LOG_FILE,
    maxBytes=10485760,  # 10MB
    backupCount=5,
    encoding='utf-8'
)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

# Configurar manejador de consola
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

# Configurar logger raíz
logging.basicConfig(
    level=LEVEL,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[file_handler, console_handler]
)


# Función para obtener un logger configurado para un módulo específico
def get_logger(name):
    """
    Obtiene un logger configurado para un módulo específico

    Args:
        name (str): Nombre del módulo (normalmente __name__)

    Returns:
        Logger: Instancia de logger configurada
    """
    logger = logging.getLogger(name)
    logger.setLevel(LEVEL)

    # Evitar duplicación de handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger