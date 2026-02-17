#!/usr/bin/env bash
# Setup web server for deployment of web_static

# We install nginx if not already installed
if ! dpkg -s nginx >/dev/null 2>&1; then
     sudo apt update -y
     sudo apt install -y nginx
fi

# Create required directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create fake html file
cat > /data/web_static/releases/test/index.html <<EOF
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF

# Remove existing symbolic link if it exists
sudo rm -rf /data/web_static/current

# create new symbolic link
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Set ownership to ubuntu user and group (recursive)
sudo chown -R ubuntu:ubuntu /data/

# Update nginx configuration to serve hbnb_static
NGINX_CONF="/etc/nginx/sites-available/default"

if ! grep -q "hbnb_static" "$NGINX_CONF"; then
    sudo sed -i "/server_name _;/a \
    location /hbnb_static/ {\n\
        alias /data/web_static/current/;\n\
    }" "$NGINX_CONF"
fi

# Restart nginx
sudo service nginx restart

# Always exit successfully
exit 0

