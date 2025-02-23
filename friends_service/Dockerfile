FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY wait-for-it.sh .
RUN chmod +x ./wait-for-it.sh
COPY . .

CMD ["sh", "-c", "./wait-for-it.sh friends_db:5432 -- python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:7500"]

