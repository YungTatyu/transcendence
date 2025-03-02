FROM owasp/modsecurity-crs:4.11.0-nginx-202502270602

USER root
RUN apt update && \
    apt install -y --no-install-recommends vim

COPY conf/nginx.conf /etc/nginx/nginx.conf
COPY conf/defalut.conf /etc/nginx/conf.d/defalut.conf
COPY conf/modsecurity.conf /etc/modsecurity.d/modsecurity.conf
ENTRYPOINT ["bash"]
