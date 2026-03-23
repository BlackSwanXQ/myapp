FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html

# Создаём скрипт для вывода hostname
RUN echo '#!/bin/sh' > /usr/share/nginx/html/hostname.sh && \
    echo 'echo $HOSTNAME' >> /usr/share/nginx/html/hostname.sh && \
    chmod +x /usr/share/nginx/html/hostname.sh

# Настраиваем nginx: для /hostname запускаем скрипт
RUN echo 'server {' > /etc/nginx/conf.d/default.conf && \
    echo '    listen 80;' >> /etc/nginx/conf.d/default.conf && \
    echo '    server_name _;' >> /etc/nginx/conf.d/default.conf && \
    echo '    root /usr/share/nginx/html;' >> /etc/nginx/conf.d/default.conf && \
    echo '    index index.html;' >> /etc/nginx/conf.d/default.conf && \
    echo '    location /hostname {' >> /etc/nginx/conf.d/default.conf && \
    echo '        alias /usr/share/nginx/html/hostname.sh;' >> /etc/nginx/conf.d/default.conf && \
    echo '        add_header Content-Type text/plain;' >> /etc/nginx/conf.d/default.conf && \
    echo '    }' >> /etc/nginx/conf.d/default.conf && \
    echo '}' >> /etc/nginx/conf.d/default.conf

EXPOSE 80
