FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY wait-for-it.sh .
RUN chmod +x ./wait-for-it.sh
COPY . .
CMD ["./wait-for-it.sh", "user_db:5432", "--", "sh", "-c", "python manage.py runserver 0.0.0.0:9000"]