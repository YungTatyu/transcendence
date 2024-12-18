FROM python:3.13-slim

# RUN apt-get update && apt-get install -y 

RUN pip install ruff

WORKDIR /app

COPY . /app

# CMD ["./linters/check.sh"]
# debug
CMD ["bash"]
