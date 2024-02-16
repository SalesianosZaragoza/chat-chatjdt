#!/usr/bin/env python3

import socket
import threading

TIEMPO_ESPERA = 100  # segundos maximos que espera el servidor antes de cerrar la conexion
PORT = 65433 #Puerto del servidor
HOST = "127.0.0.1" #IP del servidor

# Inicializar la variable para almacenar el mensaje del cliente
input_client = ""  

#Lista de strings con las opciones que se pueden usar como comandos
command_list = ["LIST", "CREATE", "CONNECT", "JOIN", "MSG"]

#Diccionario de usuarios. 
users = {}
#Conforme se registran usuarios se va rellenando con El nombre del usuario y su IP
"""
users = {
    'Usuario1': '192.168.0.15'
}
"""

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

            # Si el usuario no está registrado, solicitar el registro
            data = conn.recv(1024)
            if not data:
                print("Cliente desconectado")

            # Decodificar y guardar el mensaje del cliente
            input_client = data.decode()
            registroUsuario(input_client, addr, conn)
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        print("Cliente desconectado")
                        break
                    input_client = data.decode()
                    
                    if input_client == "mensaje":
                        """Si el usuario está enviando un mensaje se lanza un hilo para no detener la aplicación.
                        En este se comprueba si el mensaje contiene algún comando"""
                        threading.Thread(target=admitirComandos,args=(input_client)).run();
                    
                    
                    # Modificar el mensaje a enviar de vuelta al cliente
                    response_to_client = f"Mensaje desde el servidor: {input_client}"
                    # codifica el mensaje con encode y lo envia al cliente.
                    conn.sendall(response_to_client.encode())

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
        print(f"Usuarios registrados: {users}")
    else:
        print("Mensaje no reconocido")

establecerConexion()