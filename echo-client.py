#!/usr/bin/env python3

import socket
import threading

HOST = "127.0.0.1"
PORT = 65433

def recibir_mensajes(sock):
    while True:
        data = sock.recv(1024)
        if not data:
            break
        response_from_server = data.decode()
        print(f"Mensaje recibido del servidor: {response_from_server}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    username = input("Ingrese su nombre de usuario: ")
    username_message = f"USERNAME:{username}"
    s.sendall(username_message.encode())

    # Recibir la respuesta del servidor
    data = s.recv(1024)
    response_from_server = data.decode()
    print(response_from_server)

    # Iniciar un hilo para recibir mensajes del servidor
    thread = threading.Thread(target=recibir_mensajes, args=(s,))
    thread.start()

    while True:
        try:
            # Convertir el mensaje a bytes y enviarlo al servidor
            message = input("Ingrese un mensaje (o presione Enter para salir): ")
            if not message:
                break
            s.sendall(message.encode())

        except socket.timeout:
            print("Tiempo de espera alcanzado. Cerrando conexión.")
            break

    # Esperar a que el hilo de recepción termine antes de cerrar la conexión
    thread.join()
