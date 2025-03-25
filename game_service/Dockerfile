FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt /app

RUN apk upgrade --no-cache \ 
    # apk add --no-cache \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . /app

# CMD ["sh"]
# CMD ["python", "manage.py", "runserver_plus", "0.0.0.0:8001", "--cert-file", "server.crt", "--key-file", "server.key"]
CMD ["daphne", "-b", "0.0.0.0", "-e", "ssl:8001:privateKey=/app/server.crt:certKey=/app/server.key", "game_app.asgi:application"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
