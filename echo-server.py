import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 65448
TIEMPO_ESPERA = 60  # segundos

# Diccionario para almacenar los canales y usuarios
channels = {}

# Diccionario para almacenar los usuarios y sus direcciones IP
users = {}
lock = threading.Lock()


# Métodos del servidor
def handle_connection(conn, addr):
    with conn:
        conn.settimeout(TIEMPO_ESPERA)
        username = None
        print(f"Conectado por {addr}")
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                if (
                    username is None
                ):  # Solo intenta registrar si no tenemos un username aún
                    username = register_user(
                        data, addr, conn
                    )  # Siempre pasa el username actual
                username = handle_command(conn, data, addr, username)
            except socket.timeout:
                # Si el tiempo de espera se alcanza, cierra la conexión del cliente.
                print(
                    "Tiempo de espera alcanzado. Cerrando conexión del cliente("
                    + username
                    + ") con dirección IP ("
                    + str(addr)
                    + ")"
                )
                break
            except ConnectionResetError:
                print("La conexión fue restablecida por el cliente.")
                break


def handle_command(conn, data, addr, username):
    global channels, users
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
        elif command == "WHISPER":
            send_whisper(conn, input_client, username)
        elif command == "QUIT":
            quit_channel(conn, input_client, username)
        elif command == "NAME":
            new_username = change_username(conn, input_client, username, addr)
            if new_username:  # Asegura la actualización del nuevo nombre en username
                username = new_username
        elif command == "KICK":
            kick_user(conn, input_client, username)
        elif command == "USERS":
            list_users(conn)
        elif command == "HELP":
            help_command(conn)  # Agregamos el manejo del comando HELP
        else:
            conn.sendall("Comando no reconocido".encode())
    else:
        broadcast_message(conn, input_client, username)
    return username


def register_user(data, addr, conn):
    global users
    parts = data.decode().split(":")
    if parts[0] == "USERNAME":
        username = parts[1]
        if username not in users:  # Solo registra si el usuario es nuevo
            with lock:
                users[username] = {"ip": addr[0], "conn": conn}
                response_to_client = (
                    f"Bienvenido, {username}! Tu dirección IP es {addr[0]}\n"
                )
                conn.sendall(response_to_client.encode())
                print(f"Usuario registrado: {username} - {addr[0]}")
        return username  # Devuelve el username registrado o ya existente
    else:
        return None


def create_channel(conn, input_client):
    global channels
    parts = input_client.split(" ", 1)
    if len(parts) < 2:
        response_to_client = "Formato incorrecto. Usa /CREATE [nombreDelCanal]"
        conn.sendall(response_to_client.encode("utf-8"))
        return
    channel_name = parts[1].strip()
    if channel_name in channels:
        response_to_client = f"El canal '{channel_name}' ya existe."
        conn.sendall(response_to_client.encode("utf-8"))
    else:
        channels[channel_name] = {}
        response_to_client = f"Canal '{channel_name}' creado con éxito."
        conn.sendall(response_to_client.encode("utf-8"))


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
    conn.sendall(message_list.encode("utf-8"))


def list_users(conn):
    global users
    if users:
        message_list = "usuarios disponibles:\n"
        for username, info in users.items():
            ip = info["ip"]
            message_list += f"{username} (IP: {ip})\n"
    else:
        message_list = "No hay usuarios disponibles en este momento."
    conn.sendall(message_list.encode("utf-8"))


def join_channel(conn, input_client, username, addr):
    global channels, users
    parts = input_client.split(" ", 1)
    if len(parts) < 2:
        conn.sendall("Formato incorrecto. Usa /JOIN [nombreDelCanal]".encode("utf-8"))
        return
    channel_name = parts[1].strip()
    # Verifica si el canal ya existe en el diccionario de canales
    if channel_name not in channels:
        conn.sendall(f"El canal '{channel_name}' no existe.".encode("utf-8"))
        return

    # Asegúrate de que el usuario está registrado antes de añadirlo a un canal.
    if username in users:
        channels.setdefault(channel_name, {})
        channels[channel_name][username] = users[username]
        conn.sendall(f"Te has unido al canal '{channel_name}'.".encode("utf-8"))
    else:
        conn.sendall("Primero debes registrarte.".encode("utf-8"))


def send_message(conn, input_client, username):
    global channels

    parts = input_client.split(" ", 2)
    if len(parts) < 3:
        conn.sendall("Formato incorrecto. Usa /MSG [canal] [mensaje]".encode("utf-8"))
        return
    channel, message_to_send = parts[1], parts[2]
    print(f"Estado actual de channels: {channels}")
    print(f"Verificando la membresía para el usuario '{username}' en el canal '{channel}'")
    if channel in channels:
        if username not in channels[channel]:
            conn.sendall("No eres miembro de este canal o has sido expulsado.".encode("utf-8"))
            return
        for user, user_info in channels[channel].items():
            user_conn = user_info["conn"]
            try:
                user_conn.sendall(
                    f"{username} (dijo en {channel}): {message_to_send}".encode("utf-8")
                )
            except Exception as e:
                print(f"Error al enviar mensaje a {user}: {e}")


def send_whisper(conn, input_client, username):
    global users
    parts = input_client.split(" ", 2)
    if len(parts) < 3:
        conn.sendall(
            "Formato incorrecto. Usa /WHISPER [nombreUsuario] [mensaje]".encode("utf-8")
        )
        return

    recipient_username = parts[1]
    message_to_send = parts[2]

    if recipient_username in users:
        recipient_conn = users[recipient_username]["conn"]
        try:
            recipient_conn.sendall(
                f"{username} te susurró: {message_to_send}".encode("utf-8")
            )
        except Exception as e:
            print(f"Error al enviar mensaje a {recipient_username}: {e}")
            conn.sendall(
                f"No se pudo enviar el mensaje a {recipient_username}.".encode("utf-8")
            )
    else:
        conn.sendall(
            f"El usuario {recipient_username} no está disponible o no está registrado.".encode(
                "utf-8"
            )
        )


def broadcast_message(conn, input_client, username):
    conn.sendall(f"{username}: {input_client}".encode("utf-8"))


def quit_channel(conn, input_client, username):
    global channels
    parts = input_client.split()
    if len(parts) != 3:
        conn.sendall("Formato incorrecto. Usa /QUIT [nombre_del_canal] [nombre_usuario]".encode("utf-8"))
        return
    channel_name, user_to_quit = parts[1], parts[2]
    if channel_name in channels and user_to_quit in channels[channel_name]:
        with lock:
            del channels[channel_name][user_to_quit] 
        conn.sendall(f"El usuario {user_to_quit} ha abandonado el canal {channel_name}.".encode("utf-8"))
    else:
        conn.sendall("No estás en ese canal o el canal no existe.".encode("utf-8"))


def change_username(conn, input_client, username, addr):
    global users, channels, lock
    parts = input_client.split()
    if len(parts) != 2:
        conn.sendall("Formato incorrecto. Usa /NAME [nuevo_nombre]".encode("utf-8"))
        return
    new_username = parts[1]
    if new_username in users:
        conn.sendall("Ese nombre de usuario ya está en uso.".encode("utf-8"))
    else:
        with lock:
            # Actualiza el diccionario de usuarios con el nuevo nombre.
            user_info = users.pop(username)
            users[new_username] = user_info

            # Actualiza el nombre del usuario en todos los canales.
            for channel, channel_users in channels.items():
                if username in channel_users:
                    userInfo = channel_users.pop(username)
                    channel_users[new_username] = userInfo

        for channel, user_list in channels.items():
            print(f"Canal: {channel}, Usuarios: {user_list}")
        conn.sendall(
            f"Tu nombre de usuario ha sido cambiado a {new_username}.".encode("utf-8")
        )
        return new_username

def kick_user(conn, input_client, username):
    global channels
    # Solo el usuario "Admin" puede utilizar este comando
    if username.lower() != "admin":
        conn.sendall("No tienes permisos para ejecutar este comando.".encode("utf-8"))
        return
    parts = input_client.split()
    if len(parts) != 3:
        conn.sendall(
            "Formato incorrecto. Usa /KICK [nombre_del_canal] [usuario]".encode()
        )
        return
    channel_name, user_to_kick = parts[1], parts[2]
    if channel_name in channels and user_to_kick in channels[channel_name]:
        with lock:
            del channels[channel_name][user_to_kick]  # Expulsa al usuario del canal
            try:
                user_info = users[user_to_kick]
                user_conn = user_info["conn"]
                user_conn.sendall(f"Has sido expulsado del canal {channel_name}.".encode("utf-8"))
            except Exception as e:
                print(f"Error al notificar al usuario {user_to_kick} sobre la expulsión: {e}")
        conn.sendall( f"El usuario {user_to_kick} ha sido expulsado del canal {channel_name}.".encode())
    else:
        conn.sendall("El usuario no está en ese canal o el canal no existe.".encode())


def help_command(conn):
    comandos = [
        " * [bold magenta]/CREATE[/]  [[bold magenta]canal[/bold magenta]]  ---- Crear un canal",
        " * [bold magenta]/JOIN[/] [[bold magenta]canal[/bold magenta]]  ---- Unirse a un canal",
        " * [bold magenta]/LIST[/] ---- Listar todos los canales",
        " * [bold magenta]/USERS[/]  ---- Mostrar todos los usuarios en el canal actual",
        " * [bold magenta]/MSG[/] [[bold magenta]canal[/bold magenta]] [[bold magenta]mensaje[/bold magenta]] ---- Mandar mensaje a un canal",
        " * [bold magenta]/WHISPER[/] [[bold magenta]nombreUsuario[/bold magenta]] [[bold magenta]mensaje[/bold magenta]] ---- Mandar un mensaje a un usuario",
        " * [bold magenta]/QUIT[/] [[bold magenta]canal[/bold magenta]] [[bold magenta]usuario[/bold magenta]] ---- Abandonar un canal",
        " * [bold magenta]/NAME[/] [[bold magenta]nuevoNombre[/bold magenta]] ---- Cambiar el nombre de usuario",
        " * [bold magenta]/KICK[/] [[bold magenta]canal[/bold magenta]] [[bold magenta]usuario[/bold magenta]] ---- Expulsar a un usuario del canal",
        " * [bold magenta]/HELP[/] ---- Mostrar la lista de comandos disponibles",
    ]
    help_message = "Ulitice estos comandos para moverse por el chat:\n" + "\n".join(
        comandos
    )
    conn.sendall(help_message.encode("utf-8"))


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
            print("\nCerrando el servidor de CHAT-JDT...")
            sys.exit(0)


if __name__ == "__main__":
    establish_connections()
