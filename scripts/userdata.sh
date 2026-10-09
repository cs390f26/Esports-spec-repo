#!/bin/bash
set -euo pipefail

# Install the tools the rest of the script needs (Amazon Linux 2023):
# git clones the repo, nginx accepts browser traffic on port 80,
# python3 builds the venv and creates the SQLite file.
dnf install -y git nginx python3

# Download the repo. --depth 1 fetches only the latest commit,
# which is all the server needs.
REPO_DIR=/opt/esports-spec-repo
rm -rf "$REPO_DIR"
git clone --depth 1 https://github.com/cs390f26/Esports-spec-repo.git "$REPO_DIR"

# Create a virtual environment. Calling the venv's own pip installs
# there instead of system Python,
# without needing to activate the environment.
python3 -m venv "$REPO_DIR/venv"
"$REPO_DIR/venv/bin/pip" install -r "$REPO_DIR/deploy/requirements.txt"

# Build esports.db in the repo root, which is where src/app.py opens it.
# schema.sql drops and recreates the tables; sampledata.sql fills them.
python3 - <<PY
import sqlite3
from pathlib import Path

root = Path("$REPO_DIR")
db = sqlite3.connect(root / "esports.db")
db.executescript((root / "schema.sql").read_text())
db.executescript((root / "sampledata.sql").read_text())
db.close()
PY

# Gunicorn runs as ec2-user, so that user must own the repo and the
# database file. SQLite also creates a journal file next to esports.db.
chown -R ec2-user:ec2-user "$REPO_DIR"

# One worker keeps SQLite writes on a single connection. The app listens
# on localhost only; nginx is the public entry point.
cat > /etc/systemd/system/esports.service <<EOF
[Unit]
Description=Esports reservation app
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=$REPO_DIR
ExecStart=$REPO_DIR/venv/bin/gunicorn --bind 127.0.0.1:8000 --workers 1 src.app:app
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable esports
systemctl restart esports

# Replace the default static site. Every request, including /inventory
# and the HTML pages, is forwarded to gunicorn.
cat > /etc/nginx/nginx.conf <<'EOF'
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    sendfile on;
    keepalive_timeout 65;

    server {
        listen 80;
        listen [::]:80;
        server_name _;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
EOF

# SELinux, when enforcing, blocks nginx from opening a connection to gunicorn.
if command -v getenforce >/dev/null 2>&1 && [ "$(getenforce)" = "Enforcing" ]; then
  dnf install -y policycoreutils
  setsebool -P httpd_can_network_connect 1
fi

nginx -t
systemctl enable nginx
systemctl restart nginx
