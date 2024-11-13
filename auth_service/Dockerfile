FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir -p auth_app/keys && \
    apt-get update && \
    apt-get install -y openssl && \
    openssl genpkey -algorithm RSA -out auth_app/keys/private.pem -pkeyopt rsa_keygen_bits:2048 && \
    openssl rsa -pubout -in auth_app/keys/private.pem -out auth_app/keys/public.pem
COPY . .
CMD ["python", "manage.py", "runserver", "0:8000"]