FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Santiago

RUN apt-get update && apt-get install -y \
    git gcc g++ make cmake libssl-dev \
    unzip automake pkg-config tclsh perl patch tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/ossrs/srs.git /srs

WORKDIR /srs/trunk

RUN ./configure && make

RUN printf "listen 1935;\ndaemon off;\nmax_connections 100;\nhttp_api {\n    enabled on;\n    listen 1985;\n}\nhttp_server {\n    enabled on;\n    listen 8080;\n}\nvhost __defaultVhost__ {}\n" > conf/docker.conf

EXPOSE 1935 1985 8080

CMD ["./objs/srs", "-c", "conf/docker.conf"]
