import socket
import threading
import sys
import time

HEADER_LENGTH = 1000
IP = "127.0.0.1"
PORT = 1602

socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    socket_cliente.connect((IP, PORT))
    socket_cliente.setblocking(False)  # Configurar en modo no bloqueante
except Exception as e:
    print(f"Error al conectar con el servidor: {e}")
    sys.exit()

conexion_activa = True

# Función para recibir mensajes del servidor
def recibir_mensajes():
    global conexion_activa
    while conexion_activa:
        try:
            encabezado_mensaje = socket_cliente.recv(HEADER_LENGTH)
            if not encabezado_mensaje:  # Si no hay datos
                print("--- Conexión cerrada por el servidor ---")
                conexion_activa = False
                break

            longitud_nombre_usuario = int(encabezado_mensaje.decode('utf-8').strip())
            nombre_usuario = socket_cliente.recv(longitud_nombre_usuario).decode('utf-8')

            encabezado_mensaje = socket_cliente.recv(HEADER_LENGTH)
            longitud_mensaje = int(encabezado_mensaje.decode('utf-8').strip())
            mensaje = socket_cliente.recv(longitud_mensaje).decode('utf-8')

            print(f"{nombre_usuario} > {mensaje}")
        except BlockingIOError:
            # Si no hay datos, continuar sin detener el programa
            time.sleep(0.1)  # Pequeña pausa para evitar un bucle ocupado
            continue
        except Exception as e:
            print("Error al recibir mensaje:", str(e))
            conexion_activa = False
            break

# Función para enviar mensajes al servidor
def enviar_mensajes():
    global conexion_activa
    while conexion_activa:
        mensaje = input(f'{mi_nombre_usuario} > ')
        if not mensaje.strip():
            print("No puedes enviar mensajes vacíos. Intenta de nuevo.")
            continue

        mensaje = mensaje.encode('utf-8')
        encabezado_mensaje = f"{len(mensaje):<{HEADER_LENGTH}}".encode('utf-8')
        socket_cliente.send(encabezado_mensaje + mensaje)

        if mensaje.decode('utf-8').lower() == "cerrar_sesion":
            print("Cerrando sesión...")
            conexion_activa = False
            socket_cliente.close()
            break

if __name__ == "__main__":
    while True:
        mi_nombre_usuario = input("Ingrese su nombre de usuario: ").strip()
        if mi_nombre_usuario:
            break
        print("El nombre de usuario no puede estar vacío.")
    
    nombre_usuario = mi_nombre_usuario.encode('utf-8')
    encabezado_usuario = f"{len(nombre_usuario):<{HEADER_LENGTH}}".encode('utf-8')
    socket_cliente.send(encabezado_usuario + nombre_usuario)

    recibir_hilo = threading.Thread(target=recibir_mensajes)
    enviar_hilo = threading.Thread(target=enviar_mensajes)

    recibir_hilo.start()
    enviar_hilo.start()

    recibir_hilo.join()
    enviar_hilo.join()
