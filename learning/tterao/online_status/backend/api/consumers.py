import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.core.cache import cache
from channels.layers import get_channel_layer


class UserStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # ユーザー名をセッションやスコープから取得
        self.username = (
            self.scope["user"].username
            if self.scope["user"].is_authenticated
            else "anonymous"
        )

        # 接続を受け入れる
        await self.accept()

        # 接続数をインクリメントし、アクティブ状態を更新
        await self.increment_connection_count()

        # 全ユーザーの状態を送信
        await self.notify_all_statuses()

        # グループに参加
        await self.channel_layer.group_add("user_status_group", self.channel_name)

    async def disconnect(self, close_code):
        # 接続数をデクリメントし、必要に応じて非アクティブ状態を更新
        await self.decrement_connection_count()

        # グループから削除
        await self.channel_layer.group_discard("user_status_group", self.channel_name)
        await self.notify_all_statuses()

    async def receive(self, text_data):
        # クライアントからのリクエストを処理（必要に応じて）
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({"message": f"Received: {data}"}))

    @sync_to_async
    def increment_connection_count(self):
        """接続数をインクリメント"""
        count_key = f"user_connection_count_{self.username}"
        status_key = f"user_status_{self.username}"

        # 現在の接続数を取得しインクリメント
        connection_count = cache.get(count_key, 0) + 1
        cache.set(count_key, connection_count, timeout=None)

        # 初回接続ならアクティブ状態に設定
        if connection_count == 1:
            cache.set(status_key, "active", timeout=None)
            self.notify_status_change("active")

    @sync_to_async
    def decrement_connection_count(self):
        """接続数をデクリメント"""
        count_key = f"user_connection_count_{self.username}"
        status_key = f"user_status_{self.username}"

        # 現在の接続数を取得しデクリメント
        connection_count = max(cache.get(count_key, 1) - 1, 0)
        cache.set(count_key, connection_count, timeout=None)

        # 接続がゼロになったら非アクティブ状態に設定
        if connection_count == 0:
            cache.set(status_key, "inactive", timeout=None)
            self.notify_status_change("inactive")

    @sync_to_async
    def get_all_user_statuses(self):
        """全ユーザーのアクティブ状態を取得"""
        keys = cache.keys("user_status_*")
        return {key.replace("user_status_", ""): cache.get(key) for key in keys}

    async def notify_all_statuses(self):
        all_statuses = await self.get_all_user_statuses()
        await self.send(
            text_data=json.dumps({"type": "all_statuses", "statuses": all_statuses})
        )

    def notify_status_change(self, status):
        """ステータス変更を通知"""
        channel_layer = get_channel_layer()
        channel_layer.group_send(
            "user_status_group",
            {
                "type": "user_status_update",
                "username": self.username,
                "status": status,
            },
        )

    async def user_status_update(self, event):
        """他のクライアントに状態変更を通知"""
        await self.send(
            text_data=json.dumps(
                {
                    "type": "status_update",
                    "username": event["username"],
                    "status": event["status"],
                }
            )
        )
