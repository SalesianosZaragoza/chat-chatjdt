#!/usr/bin/env python3

import socket
import time

HOST = "127.0.0.1"
PORT = 65432
TIEMPO_ESPERA = 60  # segundos

# Inicializar la variable para almacenar el mensaje del cliente
input_client = ""  

#Lista de strings con las opciones que se pueden usar como comandos
command_list = ["LIST", "CREATE", "CONNECT", "JOIN", "MSG"]

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

#Llamada al metodo establecerConexion        
establecerConexion() 
