import socket
import select
import threading
from utils.utils import recibir_mensaje
HEADER_LENGTH = 1000
IP = "127.0.0.1"
PORT = 1602

def iniciar_servidor():
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor_socket.bind((IP, PORT))
    servidor_socket.listen()

    lista_sockets = [servidor_socket]
    clientes = {}

    print(f'SERVIDOR EN LÍNEA {IP}:{PORT}...')

    while True:
        try:
            leer_sockets, _, exception_sockets = select.select(lista_sockets, [], lista_sockets)
            for socket_notificado in leer_sockets:
                if socket_notificado == servidor_socket:
                    # Nueva conexión
                    socket_cliente, direccion_cliente = servidor_socket.accept()
                    usuario = recibir_mensaje(socket_cliente)
                    if usuario is False:
                        continue
                    lista_sockets.append(socket_cliente)
                    clientes[socket_cliente] = usuario
                    print(f'Nueva conexión de {direccion_cliente[0]}:{direccion_cliente[1]} nombre de usuario: {usuario["data"].decode("utf-8")}')
                else:
                    # Mensajes de clientes
                    mensaje = recibir_mensaje(socket_notificado)
                    if mensaje is False:
                        print(f'Conexión cerrada de {clientes[socket_notificado]["data"].decode("utf-8")}')
                        lista_sockets.remove(socket_notificado)
                        del clientes[socket_notificado]
                        continue
                    usuario = clientes[socket_notificado]
                    datos_mensaje = mensaje["data"].decode("utf-8")
                    if datos_mensaje.lower() == "cerrar_sesion":
                        print(f'--- {usuario["data"].decode("utf-8")} se ha desconectado ---')
                        lista_sockets.remove(socket_notificado)
                        del clientes[socket_notificado]
                        continue
                    print(f'*Mensaje de {usuario["data"].decode("utf-8")}: {datos_mensaje}*')

                    # Enviar mensaje a otros clientes
                    for cliente_socket in clientes:
                        if cliente_socket != socket_notificado:
                            try:
                                cliente_socket.send(usuario['encabezado'] + usuario['data'] + mensaje['encabezado'] + mensaje['data'])
                            except ConnectionResetError:
                                print(f'Error: Cliente desconectado inesperadamente.')
                                lista_sockets.remove(cliente_socket)
                                del clientes[cliente_socket]

            # Manejar excepciones en sockets
            for socket_notificado in exception_sockets:
                lista_sockets.remove(socket_notificado)
                del clientes[socket_notificado]

        except Exception as e:
            print(f"Error general en el servidor: {e}")


if __name__ == "__main__":
    server_thread = threading.Thread(target=iniciar_servidor)
    server_thread.daemon = True
    server_thread.start()
    server_thread.join()
