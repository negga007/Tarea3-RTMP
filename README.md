Tarea 2 - Protocolo RTMP
Taller de Redes y Servicios - Universidad Diego Portales
Lukas Díaz - Ignacio Espinoza
Protocolo: RTMP | Servidor: SRS | Cliente: VLC + ffmpeg



al ener Docker y Wireshark instalados en Ubuntu:

    sudo apt update
    sudo apt install docker.io wireshark -y

Estructura

    tarea2rtmp/
    ├── servidor/
    │   └── Dockerfile
    └── cliente/
        └── Dockerfile

1) Construir las imágenes

Primero el servidor (tarda varios minutos porque compila SRS desde fuente):

    cd servidor/
    sudo docker build -t servidor-rtmp .

Luego el cliente:

    cd ../cliente/
    sudo docker build -t cliente-vlc .

2) Crear la red

    sudo docker network create red-rtmp

3) Levantar el servidor

    sudo docker run -d --name servidor --network red-rtmp -p 1935:1935 -p 1985:1985 -p 8080:8080 servidor-rtmp

Para verificar que quedó corriendo:

    sudo docker ps

4) Capturar tráfico con Wireshark

Abrir Wireshark antes de levantar el cliente para capturar el handshake completo:

    sudo wireshark

Seleccionar interfaz any, escribir el filtro tcp.port == 1935 y capturar.

5) Levantar el cliente y transmitir

    sudo docker run -it --name cliente --network red-rtmp cliente-vlc /bin/bash

Dentro del contenedor ejecutar ffmpeg para generar el stream:

    ffmpeg -re -f lavfi -i testsrc=size=640x480:rate=30 -f lavfi -i sine=frequency=1000 -c:v libx264 -c:a aac -f flv rtmp://servidor/live/stream

6) Ver el stream con VLC

En otra terminal, fuera del contenedor:

    vlc rtmp://localhost/live/stream

Si hay que empezar de nuevo

    sudo docker rm -f servidor cliente
    sudo docker network rm red-rtmp
    sudo docker network create red-rtmp# Taller2-Taller_de_redes
