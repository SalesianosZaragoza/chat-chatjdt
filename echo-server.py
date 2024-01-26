#!/usr/bin/env python3

import socket
import time

HOST = "127.0.0.1"
PORT = 65432
TIEMPO_ESPERA = 60  # segundos

# Inicializar la variable para almacenar el mensaje del cliente
input_client = ""

# Lista de strings con las opciones que se pueden usar como comandos
command_list = ["/LIST", "/CREATE", "/CONNECT", "/JOIN", "/MSG"]

# Diccionarios
channel = {
    'canal1': '[]',
    'canal2': '[ismael, jose]',
    'canal3': '[ismael, juan]'
}
# Creacion de canales usando diccionarios
users = {
    'ismael': '192.168.1.2',
    'jose': '192.168.1.3',
    'juan': '192.168.1.4'
}

user = ("ismael", "192.168.1.2")


def establecerConexion():
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
                    admitirComandos(input_client, conn)

                except socket.timeout:
                    print("Tiempo de espera alcanzado. Cerrando conexión.")
                    break


"""Metodo admitir comandos, 
Ve que el comando empiece por / o // o + y luego compruebe que la cadena de texto  sea en mayusculas. 
O que sea en minusculas o mayusculas el metodo establezca todo a mayusculas y sean palabras reservadas
Comprobar si la variable comienza con "/" y el resto está en mayúsculas y en la lista"""


def admitirComandos(input_client, conn):
    if input_client.upper() in command_list:
        print("El input es un comando valido")
        if input_client.equals("/JOIN"):
            join_channel(user, conn)

        if input_client[1:].isupper() and input_client[1:] in command_list:
            print("El input es un comando valido")
            # Falta llamar a la funcion correspondiente, por ahora no está implementado porque no sabemos como se van a llamar las funciones
        else:
            print("El comando no existe o no está escrito correctamente. Recuerda que los comandos son en mayusculas y empiezan por /")
    else:
        print("El input no incluye un comando (no comienza por /)")


# ESTA BIEN
def join_channel(user, conn):
    channel = list(channel.keys())  # Lista de canales existentes
    message = print("/JOIN Canales existentes: " + channel)
    # Enviar de vuelta el mensaje modificado al cliente
    conn.sendall(message.encode())

    # Recibir la respuesta del cliente y decodificarla, guardandola en la variable data
    # será el nombre del canal al que se quiere unir
    data = conn.recv(1024)
    # Decodificar y guardar el mensaje del cliente
    input_client = data.decode()
    # Comprobar si el canal existe
    if input_client in channel:
        # Si existe, añadir al usuario a la lista de usuarios del canal
        channel[input_client].append(user)
        # Enviar de vuelta el mensaje modificado al cliente
        conn.sendall(message.encode())
    else:
        # Si no existe, enviar mensaje de error
        message = print("El canal no existe")
        # Enviar de vuelta el mensaje modificado al cliente
        conn.sendall(message.encode())


# Llamada al metodo establecerConexion
establecerConexion()
