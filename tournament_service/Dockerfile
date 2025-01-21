FROM python:3.9-slim

WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev gcc curl

COPY requirements.txt .
RUN pip install --upgrade pip && \
	pip install -r requirements.txt

COPY . /app

CMD ["sh", "-c", "python3 manage.py runserver 0.0.0.0:8002"]
