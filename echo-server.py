#!/usr/bin/env python3

import socket
import time

HOST = "127.0.0.1"
PORT = 65432
TIEMPO_ESPERA = 60  # segundos

input_client = ""  # Inicializar la variable para almacenar el mensaje del cliente

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Conectado por {addr}")
        
        # Establecer un tiempo de espera para el servidor
        conn.settimeout(TIEMPO_ESPERA)
        
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print("Cliente desconectado")
                    break

                # Decodificar y guardar el mensaje del cliente
                input_client = data.decode()

                # Modificar el mensaje a enviar de vuelta al cliente
                response_to_client = f"Mensaje desde el servidor: {input_client}"

                # Enviar de vuelta el mensaje modificado al cliente
                conn.sendall(response_to_client.encode())

            except socket.timeout:
                print("Tiempo de espera alcanzado. Cerrando conexión.")
                break
