FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
RUN echo 'echo $HOSTNAME' > /usr/share/nginx/html/hostname && chmod +x /usr/share/nginx/html/hostname
RUN echo 'server { listen 80; location /hostname { alias /usr/share/nginx/html/hostname; add_header Content-Type text/plain; } }' > /etc/nginx/conf.d/hostname.conf
