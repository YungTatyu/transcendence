FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY wait-for-it.sh .
RUN chmod +x ./wait-for-it.sh

# アプリ全体をコピー
COPY . .

# default_image.png を一時領域に配置（volume上書きされるので）
COPY media/images/default/default_image.png /tmp/default_image.png

# entrypointスクリプトのコピーと実行権限
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# エントリポイント（マイグレーション + runserver を entrypoint.sh に移動）
ENTRYPOINT ["/entrypoint.sh"]
