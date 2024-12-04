import sys
import os
from unittest.mock import Mock
from servidor import recibir_mensaje

# Agrega el directorio raíz del proyecto al PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



HEADER_LENGTH = 1000  # Manteniendo la longitud original del encabezado.

# Caso positivo: Se recibe un mensaje correctamente.
def test_recibir_mensaje_caso_positivo():
    # Crear un socket ficticio
    mock_socket = Mock()

    # Simular un encabezado válido (longitud de 12 bytes)
    mensaje_encabezado = f"{12:<{HEADER_LENGTH}}".encode('utf-8')
    mensaje_data = "Hola, Mundo!".encode('utf-8')

    # El socket devuelve el encabezado y el mensaje cuando se llama a `recv`
    mock_socket.recv.side_effect = [mensaje_encabezado, mensaje_data]

    # Llamar a la función
    resultado = recibir_mensaje(mock_socket)

    # Verificar resultados
    assert resultado is not False
    assert resultado['data'] == mensaje_data
    assert resultado['encabezado'] == mensaje_encabezado

# Caso negativo: No se recibe ningún dato.
def test_recibir_mensaje_caso_negativo():
    # Crear un socket ficticio
    mock_socket = Mock()

    # Simular que el socket no devuelve datos
    mock_socket.recv.return_value = b''

    # Llamar a la función
    resultado = recibir_mensaje(mock_socket)

    # Verificar resultados
    assert resultado is False

# Caso negativo: Encabezado corrupto o incompleto.
def test_recibir_mensaje_encabezado_incompleto():
    # Crear un socket ficticio
    mock_socket = Mock()

    # Simular un encabezado incompleto (no contiene longitud válida)
    mensaje_encabezado = b' ' * HEADER_LENGTH

    # Configurar el socket para devolver el encabezado y nada más
    mock_socket.recv.side_effect = [mensaje_encabezado]

    # Llamar a la función
    resultado = recibir_mensaje(mock_socket)

    # Verificar resultados
    assert resultado is False
