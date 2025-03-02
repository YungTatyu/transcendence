FROM owasp/modsecurity-crs:4.11.0-nginx-202502270602

# for develpment
# USER root
# RUN apt update && \
#     apt install -y --no-install-recommends vim

COPY nginx/nginx.conf.template /etc/nginx/templates/nginx.conf.template
COPY nginx/conf.d/default.conf.template /etc/nginx/templates/conf.d/
COPY nginx/includes/ /etc/nginx/templates/includes/

COPY modsecurity.d/ /etc/nginx/templates/modsecurity.d/

CMD ["nginx", "-g", "daemon off;"]
