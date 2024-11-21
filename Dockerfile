FROM python:alpine

RUN apk --update-cache add \
    gcc \
    g++ \
    build-base \
    linux-headers \
    python3-dev \
    pcre-dev

WORKDIR /app
COPY ./conf/requirements.txt /app
RUN pip install --upgrade pip && \
	pip install -r requirements.txt

COPY ./srcs/websocket_demo/ /app
ENTRYPOINT ["/usr/local/bin/daphne", "-p", "8000", "-b", "0.0.0.0","websocket_demo.asgi:application"]

# WebSocketを使用しない場合は下記のようにUWSGIで起動する
# ENTRYPOINT ["/usr/local/bin/uwsgi", "/app/uwsgi.ini"]
