FROM ubuntu:22.04

RUN apt update && apt install -y \
    openssh-server \
    sudo \
    sqlite3 \
    net-tools \
    procps

RUN useradd -m admin1 && echo "admin1:admin123" | chpasswd
RUN mkdir /var/run/sshd

# for privilege escalation 
RUN echo "admin1 ALL=(root) NOPASSWD: /usr/bin/sqlite3" >> /etc/sudoers

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 22
ENTRYPOINT ["/entrypoint.sh"]
