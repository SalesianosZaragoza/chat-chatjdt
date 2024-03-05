import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 65440
TIEMPO_ESPERA = 100  # segundos

# Diccionario para almacenar los canales y usuarios
channels = {}

# Diccionario para almacenar los usuarios y sus direcciones IP
users = {}
lock = threading.Lock()


# Métodos del servidor
def handle_connection(conn, addr):
    with conn:
        conn.settimeout(TIEMPO_ESPERA)
        print(f"Conectado por {addr}")
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                username = register_user(data, addr, conn)
                handle_command(conn, data, addr, username)
            except socket.timeout:
                print("Tiempo de espera alcanzado. Cerrando conexión.")
                break
            except ConnectionResetError:
                print("La conexión fue restablecida por el cliente.")
                break


def handle_command(conn, data, addr, username):
    global channels
    input_client = data.decode()
    if input_client.startswith("/"):
        command = input_client.split()[0][1:]  # Extraer el comando sin el '/'
        parts = input_client.split()
        if command == "JOIN":
            join_channel(conn, input_client, username, addr)
        elif command == "CREATE":
            create_channel(conn, input_client)
        elif command == "LIST":
            list_channels(conn)
        elif command == "MSG":
            send_message(conn, input_client, username)
        elif command == "QUIT":
            quit_channel(conn, input_client, username)
        elif command == "NAME":
            change_username(conn, input_client, username)
        elif command == "KICK":
            kick_user(conn, input_client, username)
        else:
            conn.sendall("Comando no reconocido".encode())
    else:
        broadcast_message(conn, input_client, username)


def register_user(data, addr, conn):
    global users
    parts = data.decode().split(":")
    if len(parts) == 2 and parts[0] == "USERNAME":
        username = parts[1]
        with lock:
            users[username] = addr[0]
            response_to_client = (
                f"Bienvenido, {username}! Tu dirección IP es {addr[0]}\n"
            )
            conn.sendall(response_to_client.encode())
            print(f"Usuario registrado: {username} - {addr[0]}")
            print(f"Usuarios registrados: {users}")
            return username
    else:
        print("Mensaje no reconocido")
        return None


def create_channel(conn, input_client):
    global channels
    parts = input_client.split(" ", 1)
    if len(parts) < 2:
        conn.sendall("Formato incorrecto. Usa /CREATE [nombreDelCanal]".encode())
        return
    channel_name = parts[1].strip()
    if channel_name in channels:
        conn.sendall(f"El canal '{channel_name}' ya existe.".encode())
    else:
        channels[channel_name] = {}
        conn.sendall(f"Canal '{channel_name}' creado con éxito.".encode())


def list_channels(conn):
    global channels
    if channels:
        message_list = "Canales disponibles:\n"
        for channel, users in channels.items():
            message_list += f"{channel}: {len(users)} usuarios\n"
            for username, info in users.items():
                ip = info["ip"]
                message_list += f"    {username} (IP: {ip})\n"
    else:
        message_list = "No hay canales disponibles en este momento."
    conn.sendall(message_list.encode())


def join_channel(conn, input_client, username, addr):
    global channels
    parts = input_client.split(" ", 1)
    if len(parts) < 2:
        conn.sendall("Formato incorrecto. Usa /JOIN [nombreDelCanal]".encode())
        return
    channel_name = parts[1].strip()
    if channel_name in channels:
        if username is not None:
            if username in channels[channel_name]:
                conn.sendall(f"Ya estás en el canal '{channel_name}'.".encode())
            else:
                channels[channel_name][username] = {"ip": addr}
                conn.sendall(f"Te has unido al canal '{channel_name}'.".encode())
    else:
        conn.sendall(f"El canal '{channel_name}' no existe.".encode())


def send_message(conn, input_client, username):
    global channels
    parts = input_client.split(" ", 2)
    if len(parts) < 3:
        conn.sendall("Formato incorrecto. Usa /MSG [canal] [mensaje]".encode())
        return
    channel, message_to_send = parts[1], parts[2]
    if channel in channels and username in channels[channel]:
        conn.sendall(f"{username} (en {channel}): {message_to_send}".encode())
    else:
        conn.sendall("No estás en ese canal o el canal no existe.".encode())


def broadcast_message(conn, input_client, username):
    conn.sendall(f"{username}: {input_client}".encode())


def quit_channel(conn, input_client, username):
    pass  # Implementar lógica para que un usuario abandone un canal


def change_username(conn, input_client, username):
    pass  # Implementar lógica para que un usuario cambie su nombre


def kick_user(conn, input_client, username):
    pass  # Implementar lógica para que un usuario sea expulsado de un canal


# Diccionario de métodos del servidor, Tiene que estar aquí porque las funciones se definen arriba del diccionario y sino no se pueden usar.
server_methods = {
    "handle_connection": handle_connection,
    "handle_command": handle_command,
    "register_user": register_user,
    "create_channel": create_channel,
    "list_channels": list_channels,
    "join_channel": join_channel,
    "send_message": send_message,
    "broadcast_message": broadcast_message,
}


def establish_connections():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
            s.listen()
            print(f"Servidor escuchando en {HOST}:{PORT}")
            while True:
                conn, addr = s.accept()
                threading.Thread(
                    target=server_methods["handle_connection"], args=(conn, addr)
                ).start()
        except KeyboardInterrupt:
            print("\nCerrando el servidor...")
            sys.exit(0)


if __name__ == "__main__":
    establish_connections()
