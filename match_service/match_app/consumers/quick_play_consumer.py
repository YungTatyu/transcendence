from channels.generic.websocket import AsyncWebsocketConsumer


class QuickPlayConsumer(AsyncWebsocketConsumer):
    MATCHING_ROOM = "matching_room"
    ROOM_CAPACITY = 2

    async def connect(self):
        pass

    async def disconnect(self, _):
        pass
