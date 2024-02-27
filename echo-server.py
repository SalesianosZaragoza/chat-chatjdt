import socket
import threading

HOST = "127.0.0.1"
PORT = 65440
TIEMPO_ESPERA = 100  # segundos

# Inicializar la variable para almacenar el mensaje del cliente
input_client = "" 
channels = {} 


#Lista de strings con las opciones que se pueden usar como comandos

command_list = ["LIST", "CREATE", "CONNECT", "JOIN", "MSG"]
#estado del comando para métodos Create y Join. Si no tiene un estado lo recibe como un mensaje en lugar de un
estado_comando = {"comando_actual": None, "datos": None}

# Diccionario de usuarios
users = {}
lock = threading.Lock()

def manejarConexion(conn, addr):
    with conn:
        # Establecer un tiempo de espera para el servidor
        conn.settimeout(TIEMPO_ESPERA)

        print(f"Conectado por {addr}")

            # Decodificar y guardar el mensaje del cliente
            input_client = data.decode()
            username = registroUsuario(input_client, addr, conn)
            while True:


        # Decodificar y guardar el mensaje del cliente
        input_client = data.decode()
        registroUsuario(input_client, addr, conn)

                    # Modificar el mensaje a enviar de vuelta al cliente
                    #response_to_client = f"Mensaje desde el servidor: {input_client}"
                    # codifica el mensaje con encode y lo envia al cliente.
                    #conn.sendall(response_to_client.encode())


                # Modificar el mensaje a enviar de vuelta al cliente
                response_to_client = f"Mensaje desde el servidor: {input_client}"
                # codifica el mensaje con encode y lo envía al cliente.
                conn.sendall(response_to_client.encode())

                    manejar_comando(conn, input_client, channels, addr, username)

                except socket.timeout:
                    print("Tiempo de espera alcanzado. Cerrando conexión.")
                    break
                
                
                
def manejar_comando(conn, input_client, channels, addr, username):
    

    if input_client.startswith("/"):
        comando = input_client.split()[0][1:]  # Extraer el comando sin el '/'
        
        if comando == "JOIN":
            if estado_comando["comando_actual"] == "JOIN":
                # Manejar la elección del canal después de listar los canales
                join_channel(conn, input_client, channels, username, addr)
            else:
                # Listar canales y establecer el estado a JOIN
                list_channels(conn, channels, username)
                estado_comando["comando_actual"] = "JOIN"
                
        elif comando == "CREATE":
            create_channel(conn, input_client, channels)
            
        elif comando == "LIST":
            list_channels(conn, channels, username)
            
        elif comando == "MSG":
            send_message(conn, input_client, channels, username)
            
        else:
            conn.sendall("Comando no reconocido".encode())
    elif estado_comando["comando_actual"] == "JOIN":
        # Maneja el estado del comando después de listar los canales, para que el usuario pueda unirse a uno
        join_channel(conn, input_client, channels, username, addr)
        estado_comando["comando_actual"] = None
    else:
        # Manejar mensajes normales si no es un comando
        broadcast_message(conn, input_client, username)
        


#CREAR CANAL
def create_channel(conn, input_client, channels):
    partes = input_client.split(" ", 1)
    if len(partes) < 2:
        conn.sendall("Formato incorrecto. Usa /CREATE [nombreDelCanal]".encode())
        return

    nombre_canal = partes[1].strip()

    if nombre_canal in channels:
        conn.sendall(f"El canal '{nombre_canal}' ya existe.".encode())
    else:
        channels[nombre_canal] = {}
        conn.sendall(f"Canal '{nombre_canal}' creado con éxito.".encode())


#LISTAR LOS CANALES
def list_channels(conn, channels, username):
    if channels:
        print(channels)
        mensaje_lista = "Canales disponibles:\n"
        for canal, usuarios in channels.items():
            mensaje_lista += f"{canal}: {len(usuarios)} usuarios\n"
            for username, info in usuarios.items():
                # Asegúrate de acceder correctamente a la IP
                ip = info['ip']
                mensaje_lista += f"    {username} (IP: {ip})\n"
    else:
        mensaje_lista = "No hay canales disponibles en este momento."

    conn.sendall(mensaje_lista.encode())
    

#UNIR USUARIO A UN CANAL
def join_channel(conn, input_client, channels, username, addr):
    nombre_canal = input_client.strip()

    if nombre_canal in channels:
        if username not in channels[nombre_canal]:
            channels[nombre_canal][username] = {"ip": addr}
            conn.sendall(f"Te has unido al canal '{nombre_canal}'.".encode())
            estado_comando["comando_actual"] = None  # Restablecer el estado del comando
        else:
            conn.sendall(f"Ya estás en el canal '{nombre_canal}'.".encode())
    else:
        conn.sendall(f"El canal '{nombre_canal}' no existe.".encode())


#ENVIAR MENSAJE AL CANAL 
def send_message(conn, input_client, channels, username):
    partes = input_client.split(" ", 2)
    if len(partes) < 3:
        conn.sendall("Formato incorrecto. Usa /MSG [canal] [mensaje]".encode())
        return

    canal, mensaje_a_enviar = partes[1], partes[2]

    if canal in channels and username in channels[canal]:
        # Como solo hay un usuario, simplemente envía el mensaje de vuelta. Habrá que cambiar esto para que llegue a todos
        conn.sendall(f"{username} (en {canal}): {mensaje_a_enviar}".encode())
    else:
        conn.sendall("No estás en ese canal o el canal no existe.".encode())


#ENVIA MENSAJE A TODOS LOS USUARIOS DE LOS CANALES. HABRÁ QUE RECORRER LA LISTA DE CANALES Y MANDAR EL MENSAJE
def broadcast_message(conn, input_client, username):
    # Como solo hay un usuario, simplemente envía el mensaje de vuelta. Habrá que cambiar esto para que llegue a todos
    conn.sendall(f"{username}: {input_client}".encode())


   
        
"""Metodo registroUsuario,
Separa el mensaje del cliente en dos partes, verifica si el mensaje tiene el formato esperado
Almacena el usuario y su dirección IP en el diccionario, envia un mensaje personalizado de confirmación al cliente"""

def registroUsuario(input_client, addr, conn):
    partes_mensaje = input_client.split(':')
    if len(partes_mensaje) == 2 and partes_mensaje[0] == "USERNAME":
        username = partes_mensaje[1]

        # Utilizar un candado para evitar problemas de concurrencia al modificar el diccionario
        with lock:
            # Almacenar el usuario y su dirección IP en el diccionario
            users[username] = addr[0]

            # Enviar un mensaje personalizado de confirmación al cliente
            response_to_client = f"Bienvenido, {username}! Tu dirección IP es {addr[0]}"
            conn.sendall(response_to_client.encode())

            print(f"Usuario registrado: {username} - {addr[0]}")
            print(f"Usuarios registrados: {users}")
    else:
        print("Mensaje no reconocido")
    return username
    
#Llamada al metodo establecerConexion        
establecerConexion() 

