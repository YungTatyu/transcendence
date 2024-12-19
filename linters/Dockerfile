FROM node:22-alpine

RUN apk update && apk add --no-cache bash \
    py3-pip

RUN pip install ruff --break-system-packages; \
    npm install -g --save-exact @biomejs/biome

WORKDIR /app

ENTRYPOINT ["./linters/entrypoint.sh"]

# debug
# ENTRYPOINT ["bash"]
