FROM owasp/modsecurity-crs:4.11.0-nginx-202502270602

# for develpment
# USER root
# RUN apt update && \
#     apt install -y --no-install-recommends vim

COPY docker-entrypoint.sh /
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/conf.d/ /etc/nginx/conf.d/
COPY modsecurity.d/ /etc/modsecurity.d/

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
