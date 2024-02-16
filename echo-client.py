#!/usr/bin/env python3

import socket

HOST = "127.0.0.1"
PORT = 65433

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    username = ""
    # Salir del bucle si no se ingresa ningún mensaje
    while not username:
        username = input("Ingrese Username: ")
        username = f"USERNAME:{username}"
        s.sendall(username.encode())

        # Recibir la respuesta del servidor
        data = s.recv(1024)
        response_from_server = data.decode()
        print({response_from_server})
        
    while True:
        try:
            # Convertir el mensaje a bytes y enviarlo al servidor
            message = input("Ingrese un mensaje (o presione Enter para Salir): ")
            if not message:
                break
            s.sendall(message.encode())
            
            # Recibir la respuesta del servidor
            data = s.recv(1024)
            
            # Decodificar y mostrar la respuesta recibida del servidor
            response_from_server = data.decode()
            print(f"Mensaje recibido del servidor: {response_from_server}")
        
        except socket.timeout:
            print("Tiempo de espera alcanzado. Cerrando conexión.")
            break
