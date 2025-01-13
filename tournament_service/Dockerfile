FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y libpq-dev gcc curl
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD ["sh", "-c", "python3 manage.py runserver 0.0.0.0:8001"]
