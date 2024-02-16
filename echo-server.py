import socket
import threading

HOST = "127.0.0.1"
PORT = 65433
TIEMPO_ESPERA = 100  # segundos

# Lista de strings con las opciones que se pueden usar como comandos
command_list = ["LIST", "CREATE", "CONNECT", "JOIN", "MSG"]

# Diccionario de usuarios
users = {}
lock = threading.Lock()

def manejarConexion(conn, addr):
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

                # Modificar el mensaje a enviar de vuelta al cliente
                response_to_client = f"Mensaje desde el servidor: {input_client}"
                # codifica el mensaje con encode y lo envía al cliente.
                conn.sendall(response_to_client.encode())

                admitirComandos(input_client)

            except socket.timeout:
                print("Tiempo de espera alcanzado. Cerrando conexión.")
                break

def admitirComandos(input_client):
    # Implementa la lógica para admitir comandos (similar a tu código actual)
    if input_client.startswith("/"):
        print("El input empieza por /")
        if input_client[1:].isupper() and input_client[1:] in command_list:
            print("El input es un comando valido")
            #Falta llamar a la funcion correspondiente, por ahora no está implementado porque no sabemos como se van a llamar las funciones
        else:
            print("El comando no existe o no está escrito correctamente. Recuerda que los comandos son en mayusculas y empiezan por /")
    else:
        print("El input no incluye un comando (no comienza por /)")
      
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

def establecerConexion():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=manejarConexion, args=(conn, addr))
            thread.start()

# Llamada al metodo establecerConexion
establecerConexion()
