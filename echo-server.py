#!/usr/bin/env python3

import socket

HOST = "10.10.0.131"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

# Variable que contiene un string, esto se reemplaza por el input del cliente
input_client = "/LIST"

#Lista de strings con las opciones que se pueden usar como comandos
command_list = ["LIST", "CREATE", "CONNECT", "JOIN", "MSG"]

def establecerConexion():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                print(f"Connected by {addr}")
                print("Esperando mensaje")
                print("Llamando a la funcion admitirComandos")
                admitirComandos(input_client)
                print("Llamada terminada")
                break;
                # if not data:
                #     break
                # conn.sendall(data)


#Metodo admitir comandos, 
# Ve que el comando empiece por / o // o + y luego compruebe que la cadena de texto  sea en mayusculas. 
# O que sea en minusculas o mayusculas el metodo establezca todo a mayusculas y sean palabras reservadas
# Comprobar si la variable comienza con "/" y el resto está en mayúsculas y en la lista
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
        
establecerConexion() #Llamada al metodo establecerConexion
