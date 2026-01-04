#!/bin/sh

# Fix database permissions (volume-mounted file)
if [ -f /opt/tucan/web/database/app.db ]; then
    chown root:root /opt/tucan/web/database/app.db
    chmod 640 /opt/tucan/web/database/app.db
fi

# Ensure /etc/shadow is readable only by root
chmod 640 /etc/shadow
chown root:shadow /etc/shadow

exec /usr/sbin/sshd -D