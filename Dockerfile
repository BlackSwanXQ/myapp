FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html

# Создаём простой endpoint для hostname через perl
RUN apk add --no-cache perl && \
    echo '#!/usr/bin/perl' > /usr/share/nginx/html/hostname.pl && \
    echo 'print $ENV{"HOSTNAME"};' >> /usr/share/nginx/html/hostname.pl && \
    chmod +x /usr/share/nginx/html/hostname.pl

# Настраиваем nginx
RUN echo 'server {' > /etc/nginx/conf.d/default.conf && \
    echo '    listen 80;' >> /etc/nginx/conf.d/default.conf && \
    echo '    server_name _;' >> /etc/nginx/conf.d/default.conf && \
    echo '    root /usr/share/nginx/html;' >> /etc/nginx/conf.d/default.conf && \
    echo '    index index.html;' >> /etc/nginx/conf.d/default.conf && \
    echo '    location /hostname {' >> /etc/nginx/conf.d/default.conf && \
    echo '        alias /usr/share/nginx/html/hostname.pl;' >> /etc/nginx/conf.d/default.conf && \
    echo '        add_header Content-Type text/plain;' >> /etc/nginx/conf.d/default.conf && \
    echo '    }' >> /etc/nginx/conf.d/default.conf && \
    echo '}' >> /etc/nginx/conf.d/default.conf

EXPOSE 80
