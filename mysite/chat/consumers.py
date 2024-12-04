# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.score1 = 0
        self.score2 = 0
        self.paddle1 = 0
        self.paddle2 = 0

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get("type")

        if message_type == "score":
            # Handle score update message
            score1 = text_data_json.get("score1")
            score2 = text_data_json.get("score2")
            
            # Send the score data to the whole group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "score_update",  # This will be handled by the score_update method
                    "score1": score1,
                    "score2": score2
                }
            )
        elif message_type == "paddle_update":
            self.paddle1 = text_data_json.get("paddle1")
            self.paddle2 = text_data_json.get("paddle2")
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "paddle_update",
                    "paddle1": self.paddle1,
                    "paddle2": self.paddle2
                }
            )
        else:
            print(">>>")

    async def paddle_update(self, event):
        paddle1 = event["paddle1"]
        paddle2 = event["paddle2"]
        
        # Send the updated paddle to the WebSocket client
        await self.send(text_data=json.dumps({
            "type": "paddle_update",
            "paddle1": paddle1,
            "paddle2": paddle2
    }))

    async def score_update(self, event):
        score1 = event["score1"]
        score2 = event["score2"]
        
        # Send the updated score to the WebSocket client
        await self.send(text_data=json.dumps({
            "type": "score",
            "score1": score1,
            "score2": score2
    }))
    
    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))