#!/bin/bash

# Install python-is-python3
sudo apt-get update
sudo apt-get install -y python-is-python3

# Install git
sudo apt-get install -y git

# Clone the repository
git clone https://github.com/thomerc1/SecureChatServer.git

# Install virtualenv
sudo apt-get install -y python3-venv

# Create a virtual environment and activate it
cd SecureChatServer
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r dependencies.txt

# Install nginx
sudo apt-get install -y nginx

# Create nginx site configuration
sudo bash -c 'cat > /etc/nginx/sites-available/crypt.labarge.dev << EOF
server {
    server_name crypt.labarge.dev;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/crypt.labarge.dev/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/crypt.labarge.dev/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}
server {
    if ($host = crypt.labarge.dev) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    listen 80;
    server_name crypt.labarge.dev;
    return 404; # managed by Certbot
}
EOF'

# Enable the site
sudo ln -s /etc/nginx/sites-available/crypt.labarge.dev /etc/nginx/sites-enabled/

# Test nginx configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx

# Install Certbot
sudo apt-get install -y software-properties-common
sudo add-apt-repository universe
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d crypt.labarge.dev

# Run the application
python app.py