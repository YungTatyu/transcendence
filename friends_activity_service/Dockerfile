# ベースイメージ
FROM python:3.10

# 作業ディレクトリ
WORKDIR /app

# 必要なパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションファイルをコピー
COPY . .

# サーバー起動
CMD ["daphne", "-b", "0.0.0.0", "-p", "10000", "friends_activity_app.asgi:application"]
