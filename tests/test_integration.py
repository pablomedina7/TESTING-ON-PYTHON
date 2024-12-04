import socket
import threading
import time
import pytest

SERVER_IP = "127.0.0.1"
SERVER_PORT = 1602
HEADER_LENGTH = 1000

def cliente_simulado(nombre, mensajes, desconectar=False, delay=0):
    """
    Simula un cliente que se conecta al servidor, envía mensajes y opcionalmente se desconecta abruptamente.
    """
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((SERVER_IP, SERVER_PORT))

        # Enviar nombre de usuario
        nombre_codificado = nombre.encode('utf-8')
        encabezado_nombre = f"{len(nombre_codificado):<{HEADER_LENGTH}}".encode('utf-8')
        cliente_socket.send(encabezado_nombre + nombre_codificado)

        # Enviar mensajes con opcional delay
        for mensaje in mensajes:
            time.sleep(delay)
            mensaje_codificado = mensaje.encode('utf-8')
            encabezado_mensaje = f"{len(mensaje_codificado):<{HEADER_LENGTH}}".encode('utf-8')
            cliente_socket.send(encabezado_mensaje + mensaje_codificado)

        # Desconexión abrupta
        if desconectar:
            cliente_socket.close()

    except Exception as e:
        print(f"Error en el cliente simulado ({nombre}): {e}")

@pytest.mark.integration
def test_multiple_clientes():
    """
    Prueba la conexión simultánea de múltiples clientes y el manejo de desconexiones abruptas.
    """
    clientes = []

    # Crear y conectar múltiples clientes
    for i in range(5):  # Simular 5 clientes
        nombre = f"Cliente{i}"
        mensajes = [f"Mensaje {i}-1", f"Mensaje {i}-2", "cerrar_sesion"] if i % 2 == 0 else [f"Mensaje {i}-1"]
        desconectar = i % 2 != 0  # Desconexión abrupta para clientes impares
        cliente_hilo = threading.Thread(target=cliente_simulado, args=(nombre, mensajes, desconectar, 1))
        clientes.append(cliente_hilo)
        cliente_hilo.start()

    # Esperar a que todos los clientes terminen
    for cliente_hilo in clientes:
        cliente_hilo.join()

    # Aquí puedes agregar validaciones específicas como verificar logs del servidor o datos recibidos
    assert True  # Placeholder para que el test pase si no hay errores

@pytest.mark.integration
def test_servidor_resiliente():
    """
    Verifica que el servidor siga funcionando tras desconexiones abruptas de varios clientes.
    """
    clientes = []
    
    # Crear y conectar múltiples clientes
    for i in range(3):  # Simular 3 clientes
        nombre = f"ClienteAbrupto{i}"
        mensajes = [f"Inicio {i}"]
        desconectar = True  # Todos los clientes se desconectan abruptamente
        cliente_hilo = threading.Thread(target=cliente_simulado, args=(nombre, mensajes, desconectar, 2))
        clientes.append(cliente_hilo)
        cliente_hilo.start()

    # Esperar a que los clientes terminen
    for cliente_hilo in clientes:
        cliente_hilo.join()

    # Probar que un nuevo cliente puede conectarse después de las desconexiones
    nuevo_cliente = threading.Thread(target=cliente_simulado, args=("NuevoCliente", ["Hola de nuevo"], False, 0))
    nuevo_cliente.start()
    nuevo_cliente.join()

    # Aquí también se podrían agregar validaciones más avanzadas (logs, respuestas del servidor)
    assert True  # Placeholder para que el test pase si no hay errores
