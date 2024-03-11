# CHAT-JDT

## Descripción

CHAT-JDT es una aplicación de chat en tiempo real que permite a los usuarios crear canales, unirse a ellos, enviar mensajes, susurros y más. Utiliza sockets para la comunicación en red, implementando un servidor y un cliente, con una interfaz de usuario rica gracias a las bibliotecas `rich` y `prompt_toolkit`, y notificaciones sonoras mediante `pygame`.

## Colaboradores

Este proyecto ha sido posible gracias a los esfuerzos de:

- ![IamIsmaelDev](https://avatars.githubusercontent.com/u/119622279?v=4) [IamIsmaelDev](https://github.com/IamIsmaelDev)
- ![ismaelbernadtello](https://avatars.githubusercontent.com/u/87675183?v=4) [ismaelbernadtello](https://github.com/ismaelbernadtello)
- ![alex55fc](https://avatars.githubusercontent.com/u/117534026?v=4) [alex55fc](https://github.com/alex55fc)
- ![jesusmonteroking](https://avatars.githubusercontent.com/u/92047765?v=4) [jesusmonteroking](https://github.com/jesusmonteroking)
- ![Trainsick](https://avatars.githubusercontent.com/u/119432771?v=4) [Trainsick](https://github.com/Trainsick)
- ![GemmaRubioJ](https://avatars.githubusercontent.com/u/128501232?v=4) [GemmaRubioJ](https://github.com/GemmaRubioJ)

## Características

- **Creación de Canales**: Los usuarios pueden crear canales para distintos temas o conversaciones.
- **Gestión de Usuarios**: Registro de usuarios con nombres únicos y listado de usuarios en canales.
- **Mensajes en Canales**: Envío de mensajes a todos los miembros de un canal.
- **Susurros**: Envío de mensajes privados entre usuarios.
- **Sonidos de Notificación**: Reproduce sonidos específicos para mensajes y susurros.
- **Comandos de Ayuda**: Comandos integrados para facilitar la navegación y uso de la aplicación.

## Requisitos

- Python 3.6 o superior.
- Bibliotecas de Python: `socket`, `threading`, `sys`, `rich`, `prompt_toolkit`, `pygame`.

## Instalación

Asegúrate de tener Python 3.6 o superior instalado en tu sistema. Instala las dependencias necesarias
ejecutando el archivo instalacion.py:

```bash
python3 instalacion.py
```

## Uso

Para iniciar el servidor de chat:

```bash
python3 echo-server.py
```

Para conectar un cliente al chat:

```bash
python echo-client.py
``` 

## Comandos Disponibles
- `/CREATE [nombreDelCanal]`: Crea un nuevo canal.
- `/JOIN [nombreDelCanal]`: Únete a un canal existente.
- `/LIST`: Lista todos los canales disponibles.
- `/USERS`: Muestra todos los usuarios en el canal actual.
- `/MSG [canal] [mensaje]`: Envía un mensaje al canal especificado.
- `/WHISPER [nombreUsuario] [mensaje]`: Envía un mensaje privado a un usuario.
- `/QUIT [canal] [usuario]`: Abandona un canal.
- `/NAME [nuevoNombre]`: Cambia tu nombre de usuario.
- `/KICK [canal] [usuario]`: (Admin) Expulsa a un usuario de un canal.
- `/HELP`: Muestra la lista de comandos disponibles.

## Contribuciones

Las contribuciones son bienvenidas. Si tienes sugerencias para mejorar la aplicación, siéntete libre de crear un *pull request* o abrir un *issue* en el repositorio.

## Licencia

CHAT-JDT es un software de código abierto bajo la [licencia GPL](LICENSE).