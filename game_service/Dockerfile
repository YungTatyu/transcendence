FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt /app

RUN apk upgrade --no-cache \ 
    # apk add --no-cache \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . /app

# CMD ["sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
