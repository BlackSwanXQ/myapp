FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
RUN echo 'echo $HOSTNAME' > /usr/share/nginx/html/hostname && chmod +x /usr/share/nginx/html/hostname
RUN echo 'location /hostname { alias /usr/share/nginx/html/hostname; add_header Content-Type text/plain; }' >> /etc/nginx/conf.d/default.conf
EXPOSE 80
