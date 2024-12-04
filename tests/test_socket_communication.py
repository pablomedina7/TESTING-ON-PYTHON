import socket
import threading
import pytest
from servidor import iniciar_servidor


IP = "127.0.0.1"
PORT = 1602

@pytest.fixture(scope='module')
def servidor():
    # Inicia el servidor en un hilo separado para que esté en paralelo a la prueba
    server_thread = threading.Thread(target=iniciar_servidor)
    server_thread.daemon = True
    server_thread.start()
    print("Servidor en hilo iniciado para pruebas")
    
def test_conexion_cliente(servidor):
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente_socket.connect((IP, PORT))
        print("Cliente conectado correctamente")
        assert cliente_socket  # Verifica si la conexión fue exitosa
    except socket.error as e:
        pytest.fail(f"El cliente no pudo conectarse al servidor: {e}")
    finally:
        cliente_socket.close()
        print("Cliente desconectado")
