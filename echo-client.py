#!/usr/bin/env python3

import socket

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    while True:
        try:
            # Solicitar al usuario que ingrese un mensaje
            message = input("Ingrese un mensaje (o presione Enter para salir): ")
            
            # Salir del bucle si no se ingresa ningún mensaje
            if not message:
                break
            
            # Convertir el mensaje a bytes y enviarlo al servidor
            s.sendall(message.encode())
            
            # Recibir la respuesta del servidor
            data = s.recv(1024)
            
            # Decodificar y mostrar la respuesta recibida del servidor
            response_from_server = data.decode()
            print(f"Mensaje recibido del servidor: {response_from_server}")
        
        except socket.timeout:
            print("Tiempo de espera alcanzado. Cerrando conexión.")
            break
