import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 65431

def receive_messages(sock):
    while True:
        data = sock.recv(1024)
        if not data:
            break
        print(data.decode().rstrip())
        

def send_messages(sock):
    while True:
        message = input("Comando: ")
        # Codifica el mensaje, ignorando caracteres problemáticos
        encoded_message = message.encode('utf-8', errors='ignore')
        sock.sendall(encoded_message)
        

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("BIENVENIDO A CHAT-JDT")
            print("Ingrese un nombre de usuario para comenzar:")
            username = input("Username: ")
            s.sendall(f"USERNAME:{username}".encode())
            
            response_from_server = s.recv(1024).decode()
            print(response_from_server)
            
            print("Ingrese un comando o pulse Intro para salir")
            print("Ulitice estos comandos para moverse por el chat")
            print(" * /CREATE [canal] ---- Crear un canal")
            print(" * /JOIN [canal] ---- Unirse a un canal")
            print(" * /LIST ---- Listar todos los canales")
            print(" * /MSG [canal] [mensaje] ---- Mandar mensaje a un canal")
            print(" * /QUIT [canal] ---- Abandonar un canal")
            print(" * /NAME [nuevoNombre] ---- Cambiar el nombre de usuario")
            print(" * /KICK [canal] [usuario] ---- Expulsar a un usuario del canal")

            # Iniciar el hilo para recibir mensajes
            receive_thread = threading.Thread(target=receive_messages, args=(s,))
            receive_thread.start()

            # Enviar mensajes en un bucle infinito
            while True:
                send_messages(s)
        except KeyboardInterrupt:
            print("\nCerrando la conexión...")
            s.close()
            sys.exit(0)

if __name__ == "__main__":
    main()
