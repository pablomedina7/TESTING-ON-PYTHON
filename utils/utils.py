HEADER_LENGTH = 1000

def recibir_mensaje(socket_cliente):
    """
    Recibe un mensaje del socket.
    Devuelve un diccionario con el encabezado y los datos, o False si no hay datos.
    """
    try:
        mensaje_encabezado = socket_cliente.recv(HEADER_LENGTH)
        if not mensaje_encabezado:
            return False
        tamaño_del_mensaje = int(mensaje_encabezado.decode('utf-8').strip())
        mensaje = socket_cliente.recv(tamaño_del_mensaje)
        return {'encabezado': mensaje_encabezado, 'data': mensaje}
    except Exception:
        return False
