#!/bin/bash
# Fix permissions on the database if it exists
if [ -f /opt/tucan/web/database/app.db ]; then
    chown root:root /opt/tucan/web/database/app.db
    chmod 640 /opt/tucan/web/database/app.db
fi

# Start SSH
exec /usr/sbin/sshd -D
