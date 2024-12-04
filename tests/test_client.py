import sys
import os
from unittest.mock import patch, Mock
import client  # Importamos el módulo client

# Agrega el directorio raíz del proyecto al PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



# Caso negativo: No se envía un mensaje vacío
def test_enviar_mensaje_vacio():
    with patch('client.socket_cliente', new=Mock()) as mock_socket:  # Simular el socket completo
        with patch('builtins.input', side_effect=["", "  ", "cerrar_sesion"]):  # Simular mensajes vacíos y luego cerrar sesión
            client.mi_nombre_usuario = "UsuarioDeTest"  # Definir un nombre de usuario      
            client.conexion_activa = True
            client.enviar_mensajes()

            # Verificar que el método send no se llame para mensajes vacíos
            assert len(mock_socket.send.call_args_list) == 1  # Solo "cerrar_sesion" se envía
            # Validar que se envía correctamente "cerrar_sesion"
            assert b"cerrar_sesion" in mock_socket.send.call_args_list[0][0][0]

# Caso positivo: Se envía un mensaje válido
def test_enviar_mensaje_valido():
    mensaje = "Hola, buenas, como estas?"
    with patch('client.socket_cliente', new=Mock()) as mock_socket:  # Simular el socket completo
        with patch('builtins.input', side_effect=[mensaje, "cerrar_sesion"]):  # Simular un mensaje válido y luego cerrar sesión
            client.mi_nombre_usuario = "UsuarioTest"  # Definir un nombre de usuario      
            client.conexion_activa = True
            client.enviar_mensajes()

            # Verificar que el método send se llame con el mensaje y el encabezado concatenados
            enviado = [call[0][0] for call in mock_socket.send.call_args_list]
            assert len(enviado) == 2  # Se deben enviar dos mensajes
            assert f"{len(mensaje):<{client.HEADER_LENGTH}}".encode('utf-8') + mensaje.encode('utf-8') in enviado
            assert f"{len('cerrar_sesion'):<{client.HEADER_LENGTH}}".encode('utf-8') + b"cerrar_sesion" in enviado
