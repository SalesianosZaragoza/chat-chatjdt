from rich.console import Console
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.patch_stdout import patch_stdout
from playsound import playsound
import socket
import threading
import sys
import pygame


HOST = "127.0.0.1"
PORT = 65443

console = Console()
style = Style.from_dict(
    {
        "prompt": "bold yellow",  # Esto define el estilo para 'prompt'.
    }
)


def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            message = data.decode("utf-8").rstrip()
            console.print(message, style="green")
            if "susurró" in message or "dice" in message:
                # Reproduce el sonido cuando se recibe un mensaje
                pygame.mixer.init()
                pygame.mixer.music.load("notificacion.mp3")
                pygame.mixer.music.play()
        except Exception as e:
            console.print(f"Error al recibir mensajes: {e}", style="red")
            break


def send_messages(sock, session):
    try:
        while True:
            message = session.prompt("Comando: ", style=style)
            sock.sendall(message.encode("utf-8"))
    except KeyboardInterrupt:
        console.print(
            "\nCerrando CHAT-JDT ---  ¡ADIÓS!", style="cyan"
        )  # mensaje para cuando cierras client con Ctnl+C en consola y terminas el While


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
        except Exception as e:
            console.print(f"[red]Error al conectar: {e}[/red]")
            sys.exit(1)

        console.print("BIENVENIDO A CHAT-JDT", style="cyan")
        session = PromptSession(style=style)

        with patch_stdout():
            username = session.prompt("Ingrese un nombre de usuario para comenzar: ")
        s.sendall(f"USERNAME:{username}".encode())

        response_from_server = s.recv(1024).decode()
        console.print(response_from_server, style="magenta")

        console.print("Ulitice estos comandos para moverse por el chat", style="cyan")
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

        for comando in comandos:
            console.print(comando)
            # Iniciar el hilo para recibir mensajes
        threading.Thread(target=receive_messages, args=(s,)).start()
        send_messages(s, session)


if __name__ == "__main__":
    main()
