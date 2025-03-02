FROM owasp/modsecurity-crs:4.11.0-nginx-202502270602

USER root
RUN apt update && \
    apt install -y --no-install-recommends vim

COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf
COPY modsecurity.d/ /etc/modsecurity.d/
ENTRYPOINT ["nginx", "-g", "daemon off;"]
