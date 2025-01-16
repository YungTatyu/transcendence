FROM python:3.9-alpine

WORKDIR /app

COPY . /app

RUN apk upgrade --no-cache \ 
    # apk add --no-cache \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

CMD ["sh"]
# CMD ["python manage.py runserver"]
