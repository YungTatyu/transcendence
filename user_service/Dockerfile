FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY wait-for-it.sh .
RUN chmod +x ./wait-for-it.sh
COPY . .
# CMD ["sh"]
RUN mkdir -p images/uploads
RUN mkdir -p images/default
COPY images/default_image.png /app/user_app/media/images/default/default_image.png

CMD ["./wait-for-it.sh", "user_db:5432", "--", "sh", "-c", "\
python manage.py makemigrations user_app && \
python manage.py migrate user_app && \
gunicorn user_app.wsgi:application --bind 0.0.0.0:9000"]