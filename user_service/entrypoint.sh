#!/bin/sh

echo "🚀 entrypoint.sh started"

DEFAULT_IMAGE_PATH="/app/user_app/media/images/default/default_image.png"

# 初回のみ default 画像をコピー（既にあるならスキップ）
if [ ! -f "$DEFAULT_IMAGE_PATH" ]; then
    echo "📁 Copying default_image.png to volume..."
    mkdir -p $(dirname "$DEFAULT_IMAGE_PATH")
    cp /tmp/default_image.png "$DEFAULT_IMAGE_PATH"
else
    echo "✅ default_image.png already exists, skipping copy"
fi

# マイグレーションと起動
echo "⚙️ Running migrations and starting server..."
python manage.py makemigrations user_app
python manage.py migrate user_app

# 開発用runserver起動（gunicorn等に差し替え可能）
python manage.py runserver 0.0.0.0:9000
