FROM ubuntu:22.04

RUN apt update && apt install -y \
    sudo \
    vim \
    curl \
    netcat \
    && rm -rf /var/lib/apt/lists/*

CMD ["sleep", "infinity"]
