FROM node:22-alpine

RUN apk update && apk add bash \
    py3-pip

RUN pip install ruff --break-system-packages; \
    npm install -g --save-exact @biomejs/biome

WORKDIR /app

COPY . /app

CMD ["./linters/check.sh"]

# debug
# CMD ["bash"]
