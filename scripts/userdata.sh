#!/bin/bash
set -euo pipefail

# EC2 user data: publish the static reservation mockups in ui/
# and install Flask into a virtual environment from deploy/requirements.txt.

if [ -f /etc/os-release ] && grep -qi ubuntu /etc/os-release; then
  export DEBIAN_FRONTEND=noninteractive
  apt-get update
  apt-get install -y git nginx python3 python3-venv python3-pip
  WEB_ROOT=/var/www/html
else
  if command -v dnf >/dev/null 2>&1; then
    dnf install -y git nginx python3 python3-pip
  else
    yum install -y git nginx python3 python3-pip
  fi
  WEB_ROOT=/usr/share/nginx/html
fi

REPO_DIR=/opt/esports-spec-repo
rm -rf "$REPO_DIR"
git clone --depth 1 https://github.com/cs390f26/Esports-spec-repo.git "$REPO_DIR"

python3 -m venv "$REPO_DIR/venv"
"$REPO_DIR/venv/bin/pip" install -r "$REPO_DIR/deploy/requirements.txt"

rm -rf "$WEB_ROOT"
mkdir -p "$WEB_ROOT"
cp -a "$REPO_DIR/ui/." "$WEB_ROOT/"
cp "$WEB_ROOT/01-overview.html" "$WEB_ROOT/index.html"

systemctl enable nginx
systemctl restart nginx
