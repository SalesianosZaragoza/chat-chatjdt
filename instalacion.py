import subprocess


def instalar_librerias():
    librerias = ["rich", "prompt-toolkit", "playsound"]

    for libreria in librerias:
        try:
            # Intenta instalar la librería utilizando pip
            subprocess.check_call(["pip", "install", libreria])
            print(f"La librería {libreria} se ha instalado correctamente.")
        except Exception as e:
            print(f"Error al instalar la librería {libreria}: {str(e)}")


if __name__ == "__main__":
    instalar_librerias()
