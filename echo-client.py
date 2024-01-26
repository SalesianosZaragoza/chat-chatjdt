#!/usr/bin/env python3

import socket
import time

# Recogemos el nombre del Host para obtener su IP
HOSTIP = "127.0.0.1"
PORT = 65432

PORT = 65432

TIEMPO_ESPERA = 60  # segundos

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOSTIP, PORT))

    # Establecer un tiempo de espera para el cliente
    s.settimeout(TIEMPO_ESPERA)

    while True:
        try:
            # Solicitar al usuario que ingrese un mensaje
            message = input(
                "Ingrese un mensaje (o presione Enter para salir): ")

            # Salir del bucle si no se ingresa ningún mensaje
            if not message:
                break

            print(
                f"Mensaje recibido del servidor: {comprobarRespuestaServidor()}")

        except socket.timeout:
            print("Tiempo de espera alcanzado. Cerrando conexión.")
            break


def comprobarRespuestaServidor():
    # Recibir la respuesta del servidor
    data = s.recv(1024)
    # Decodificar y guardar el mensaje del servidor
    mensaje = data.decode()


def join_client(mensaje):
    mensaje = mensaje.split(" ")
