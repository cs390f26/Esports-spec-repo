#!/bin/bash
set -euo pipefail

# Install the tools the rest of the script needs (Amazon Linux 2023):
# git clones the repo, nginx serves the pages, python3 builds the venv.
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

# Copy the mockups from ui/ into nginx's web folder.
# "ui/." copies the folder's contents, not the folder itself.
cp -a "$REPO_DIR/ui/." /usr/share/nginx/html/
# nginx serves index.html for "/", so make the overview page the home page.
cp /usr/share/nginx/html/01-overview.html /usr/share/nginx/html/index.html

# enable starts nginx automatically after every reboot; restart starts it now
# and picks up the new pages.
systemctl enable nginx
systemctl restart nginx
