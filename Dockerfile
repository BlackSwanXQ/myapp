FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html

# Создаём файл hostname при старте контейнера
RUN echo '#!/bin/sh' > /docker-entrypoint.d/40-generate-hostname.sh && \
    echo 'echo $HOSTNAME > /usr/share/nginx/html/hostname.txt' >> /docker-entrypoint.d/40-generate-hostname.sh && \
    chmod +x /docker-entrypoint.d/40-generate-hostname.sh

# Настраиваем nginx
RUN echo 'server {' > /etc/nginx/conf.d/default.conf && \
    echo '    listen 80;' >> /etc/nginx/conf.d/default.conf && \
    echo '    server_name _;' >> /etc/nginx/conf.d/default.conf && \
    echo '    root /usr/share/nginx/html;' >> /etc/nginx/conf.d/default.conf && \
    echo '    index index.html;' >> /etc/nginx/conf.d/default.conf && \
    echo '    location /hostname {' >> /etc/nginx/conf.d/default.conf && \
    echo '        alias /usr/share/nginx/html/hostname.txt;' >> /etc/nginx/conf.d/default.conf && \
    echo '        add_header Content-Type text/plain;' >> /etc/nginx/conf.d/default.conf && \
    echo '    }' >> /etc/nginx/conf.d/default.conf && \
    echo '}' >> /etc/nginx/conf.d/default.conf

EXPOSE 80
