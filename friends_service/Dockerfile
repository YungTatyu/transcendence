FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt
COPY wait-for-it.sh .
RUN chmod +x ./wait-for-it.sh
COPY . .

CMD ["./wait-for-it.sh", "friends_db:5432", "--", "sh", "-c", "\
python manage.py makemigrations && \
python manage.py migrate && \
gunicorn auth_app.wsgi:application --bind 0.0.0.0:7500"]
