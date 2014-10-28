#!/bin/sh
# @authors Kyle Baran, Liam Broza
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/ografy.io

# server {
# listen   443;

# ssl    on;
# ssl_certificate    /etc/ssl/your_domain_name.pem; (or bundle.crt)
# ssl_certificate_key    /etc/ssl/your_domain_name.key;

# server_name your.domain.com;
# access_log /var/log/nginx/nginx.vhost.access.log;
# error_log /var/log/nginx/nginx.vhost.error.log;
# location / {
# 	root   /home/www/public_html/your.domain.com/public/;
# 	index  index.html;
# 	}
# }
