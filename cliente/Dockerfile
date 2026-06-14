FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Santiago

RUN apt-get update && apt-get install -y \
    vlc \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]
