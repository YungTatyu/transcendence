FROM owasp/modsecurity-crs:4.11.0-nginx-202502270602

# for develpment
# USER root
# RUN apt update && \
#     apt install -y --no-install-recommends vim

COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/conf.d/ /etc/nginx/conf.d/
COPY modsecurity.d/ /etc/modsecurity.d/

# 環境変数を使用する場合は、以下を使用する
# COPY docker-entrypoint.sh /
# RUN chmod +x /docker-entrypoint.sh
# ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["nginx", "-g", "daemon off;"]
