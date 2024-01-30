#!/usr/bin/env python3

import socket

HOST = "127.0.0.1"
PORT = 65433
TIEMPO_ESPERA = 20  # segundos

# Inicializar la variable para almacenar el mensaje del cliente
input_client = ""  

#Lista de strings con las opciones que se pueden usar como comandos
command_list = ["LIST", "CREATE", "CONNECT", "JOIN", "MSG"]

#Diccionarios
channell = {
    'canal1': '[ismael, jose, juan]',
    'canal2': '[ismael, jose]',
    'canal3': '[ismael, juan]'
    }
# Creacion de canales usando diccionarios
user = {
    'ismael': '192.168.1.2',
    'jose': '192.168.1.3',
    'juan': '192.168.1.4'
    }
#Diccionario de usuarios
users = {}

def establecerConexion():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        #conn y addr son variables que se usan para almacenar la conexion y la direccion del cliente
        conn, addr = s.accept()
        with conn:
            # Establecer un tiempo de espera para el servidor
            conn.settimeout(TIEMPO_ESPERA)

            print(f"Conectado por {addr}")

            while True:
                try:
                    # Recibir datos del cliente (hasta 1024 bytes)
                    data = conn.recv(1024)
                    if not data:
                        print("Cliente desconectado")
                        break

                    # Decodificar y guardar el mensaje del cliente
                    input_client = data.decode()
                    registroUsuario(input_client, addr, conn)

                    # Modificar el mensaje a enviar de vuelta al cliente
                    response_to_client = f"Mensaje desde el servidor: {input_client}"
                    # codifica el mensaje con encode y lo envia al cliente.
                    conn.sendall(response_to_client.encode())


                    admitirComandos(input_client)

                except socket.timeout:
                    print("Tiempo de espera alcanzado. Cerrando conexión.")
                    break
                
"""Metodo admitir comandos, 
Ve que el comando empiece por / o // o + y luego compruebe que la cadena de texto  sea en mayusculas. 
O que sea en minusculas o mayusculas el metodo establezca todo a mayusculas y sean palabras reservadas
Comprobar si la variable comienza con "/" y el resto está en mayúsculas y en la lista"""
def admitirComandos(input_client):
    if input_client.startswith("/"):
        print("El input empieza por /")
        if input_client[1:].isupper() and input_client[1:] in command_list:
            print("El input es un comando valido")
            #Falta llamar a la funcion correspondiente, por ahora no está implementado porque no sabemos como se van a llamar las funciones
        else:
            print("El comando no existe o no está escrito correctamente. Recuerda que los comandos son en mayusculas y empiezan por /")
    else:
        print("El input no incluye un comando (no comienza por /)")
        
"""Metodo registroUsuario,
Separa el mensaje del cliente en dos partes, verifica si el mensaje tiene el formato esperado
Almacena el usuario y su dirección IP en el diccionario, envia un mensaje personalizado de confirmación al cliente"""
def registroUsuario(input_client, addr, conn):
    # Separar el mensaje del cliente en dos partes                
    partes_mensaje = input_client.split(':')
    # Verificar si el mensaje tiene el formato esperado
    if len(partes_mensaje) == 2 and partes_mensaje[0] == "USERNAME":
        username = partes_mensaje[1]

        # Almacenar el usuario y su dirección IP en el diccionario
        users[username] = addr[0]

        # Enviar un mensaje personalizado de confirmación al cliente
        response_to_client = f"Bienvenido, {username}! Tu dirección IP es {addr[0]}"
        conn.sendall(response_to_client.encode())

        print(f"Usuario registrado: {username} - {addr[0]}")
    else:
        print("Mensaje no reconocido")

    
#Llamada al metodo establecerConexion        
establecerConexion() 
