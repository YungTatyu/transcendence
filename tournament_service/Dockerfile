FROM python:3.9-slim

WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev gcc curl

COPY requirements.txt .
RUN pip install --upgrade pip && \
	pip install -r requirements.txt

COPY . /app
RUN chmod +x ./wait-for-it.sh

CMD ["sh", "-c", "./wait-for-it.sh tournament_db:5432 -- \
python3 manage.py makemigrations && \
python3 manage.py migrate && \
daphne -b 0.0.0.0 -p 8002 config.asgi:application"]
