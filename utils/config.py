import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración del servidor HTTP
HTTP_HOST = os.getenv('HTTP_HOST', '0.0.0.0')
HTTP_PORT = int(os.getenv('HTTP_PORT', 5000))
HTTP_DEBUG = os.getenv('HTTP_DEBUG', 'False').lower() == 'true'

# Rutas de certificados para TLS
CERT_PATH = os.getenv('CERT_PATH', 'certificados/cert.pem')
KEY_PATH = os.getenv('KEY_PATH', 'certificados/key.pem')
CA_PATH = os.getenv('CA_PATH', 'certificados/ca.crt')

# Configuración de seguridad
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secreta')
JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', 1))

# Configuración del servidor gRPC
GRPC_HOST = os.getenv('GRPC_HOST', '0.0.0.0')
GRPC_PORT = int(os.getenv('GRPC_PORT', 50051))
GRPC_MAX_WORKERS = int(os.getenv('GRPC_MAX_WORKERS', 10))

# Configuración de RabbitMQ
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'guest')
RABBITMQ_NOTIFICATION_QUEUE = os.getenv('RABBITMQ_NOTIFICATION_QUEUE', 'notificaciones')

# Configuración de MQTT
MQTT_BROKER = os.getenv('MQTT_BROKER', 'localhost')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
MQTT_TLS_PORT = int(os.getenv('MQTT_TLS_PORT', 8883))
MQTT_USER = os.getenv('MQTT_USER', '')
MQTT_PASS = os.getenv('MQTT_PASS', '')
MQTT_CHAT_TOPIC = os.getenv('MQTT_CHAT_TOPIC', 'chat/')

# Configuración de Base de Datos (si se necesita)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 5432))
DB_NAME = os.getenv('DB_NAME', 'mensajeria')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'postgres')

# Configuración de logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'logs/mensajeria.log')

# Usuarios por defecto para pruebas (solo para desarrollo)
DEFAULT_USERS = {
    'admin': {'password': '1234', 'role': 'admin'},
    'user1': {'password': 'user1', 'role': 'user'},
    'user2': {'password': 'user2', 'role': 'user'}
}

# Función para obtener la URL completa de RabbitMQ
def get_rabbitmq_url():
    return f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"