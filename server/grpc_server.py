import grpc
from concurrent import futures
import sys
import os

# Añadir directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar módulos del proyecto
from utils.logger import get_logger
from utils.config import GRPC_HOST, GRPC_PORT, GRPC_MAX_WORKERS, DEFAULT_USERS
from security.jwt_utils import verify_jwt, get_identity_from_token

# Importar módulos generados por gRPC
try:
    import proto.auth_pb2 as auth_pb2
    import proto.auth_pb2_grpc as auth_pb2_grpc
except ImportError:
    print("Error: Archivos auth_pb2.py y auth_pb2_grpc.py no encontrados.")
    print(
        "Genera estos archivos primero con: python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/auth.proto")
    sys.exit(1)

# Obtener logger
logger = get_logger(__name__)


class AuthServicer(auth_pb2_grpc.AuthServicer):
    """
    Implementación del servicio de autenticación definido en auth.proto
    """

    def Validate(self, request, context):
        """
        Valida las credenciales de un usuario

        Args:
            request: Mensaje Credentials con username y password
            context: Contexto de gRPC

        Returns:
            ValidationResponse: Respuesta con resultado de validación
        """
        username = request.username
        password = request.password

        logger.info(f"Validando credenciales para usuario: {username}")

        # Verificar credenciales (en un sistema real, esto se haría contra una base de datos)
        if username in DEFAULT_USERS and DEFAULT_USERS[username]['password'] == password:
            logger.info(f"Validación exitosa para usuario: {username}")
            return auth_pb2.ValidationResponse(
                valid=True,
                message="Credenciales válidas",
                user_id=username
            )
        else:
            logger.warning(f"Validación fallida para usuario: {username}")
            return auth_pb2.ValidationResponse(
                valid=False,
                message="Credenciales inválidas",
                user_id=""
            )

    def VerifyToken(self, request, context):
        """
        Verifica si un token JWT es válido

        Args:
            request: Mensaje TokenRequest con token
            context: Contexto de gRPC

        Returns:
            ValidationResponse: Respuesta con resultado de validación
        """
        token = request.token

        logger.info("Verificando token JWT")

        # Verificar token
        is_valid = verify_jwt(token)

        if is_valid:
            identity = get_identity_from_token(token)
            logger.info(f"Token válido para usuario: {identity}")
            return auth_pb2.ValidationResponse(
                valid=True,
                message="Token válido",
                user_id=identity
            )
        else:
            logger.warning("Token inválido o expirado")
            return auth_pb2.ValidationResponse(
                valid=False,
                message="Token inválido o expirado",
                user_id=""
            )


def serve():
    """
    Inicia el servidor gRPC
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=GRPC_MAX_WORKERS))
    auth_pb2_grpc.add_AuthServicer_to_server(AuthServicer(), server)

    # Añadir dirección de escucha
    server_address = f"{GRPC_HOST}:{GRPC_PORT}"
    server.add_insecure_port(server_address)

    # Iniciar servidor
    server.start()
    logger.info(f"Servidor gRPC iniciado en {server_address}")

    # Mantener servidor en ejecución
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Cerrando servidor gRPC...")
        server.stop(0)


if __name__ == "__main__":
    serve()