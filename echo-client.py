import threading
import socket
import time


HOST = "127.0.0.1"
PORT = 65440



def receive(s):
    while True:
        try:
            data = s.recv(1024)
            if not data:
                break
            print(f"SERVIDOR: {data.decode()}")
        except Exception as e:
            print(f"Error al recibir datos: {e}")
            break

def send(s):
    while True:
        try:
            time.sleep(0.5)
            message = input("Comando :  ")
            
            s.sendall(message.encode())
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
            break

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        username = ""
        print("BIENVENIDO A CHAT-JDT")
        print("Ingrese un comando o pulse Intro para salir")
        print("Ulitice estos comandos para moverse por el chat")
        print(" * /CREATE ---- Crear un canal")
        print(" * /JOIN ---- Unirse a un canal")
        print(" * /LIST ---- Listar todos los canales")
        print(" * /MSG [canal] [mensaje] ---- Mandar mensaje a un canal")
        while not username:
            username = input("Ingrese Username: ")
            s.sendall(f"USERNAME:{username}".encode())
            response_from_server = s.recv(1024).decode()
            print({response_from_server})

        # Crear hilos para enviar y recibir
        hiloRecibir = threading.Thread(target=receive, args=(s,))
        hiloMandar = threading.Thread(target=send, args=(s,))

        hiloRecibir.start()
        hiloMandar.start()
        
        hiloRecibir.join()
        hiloMandar.join()

if __name__ == "__main__":
    main()