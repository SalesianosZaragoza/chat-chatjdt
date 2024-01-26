#!/usr/bin/env python3

import socket
import time

#Recogemos el nombre del Host para obtener su IP
HOSTNAME = socket.gethostname()
HOSTIP = socket.gethostbyname(HOSTNAME)

PORT = 65432

TIEMPO_ESPERA = 60  # segundos

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOSTIP, PORT))
    
    # Establecer un tiempo de espera para el cliente
    s.settimeout(TIEMPO_ESPERA)
    
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
