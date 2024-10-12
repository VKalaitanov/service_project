from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth import get_user_model

from .models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()
            return

        other_user_id = self.scope['url_route']['kwargs']['id_room']
        room = await self.get_or_create_room(other_user_id)

        self.room_group_name = f"chat_{room.id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        messages = await self.get_message_history(room)
        for message in messages:
            await self.send(text_data=json.dumps({
                'message': f"{message['user']}: {message['content']}"
            }))

    @database_sync_to_async
    def get_or_create_room(self, other_user_id):
        other_user = get_user_model().objects.get(id=other_user_id)
        room, created = Room.objects.get_or_create(user=other_user)
        return room

    @database_sync_to_async
    def get_message_history(self, room):
        messages = room.messages.order_by('timestamp')[:5]
        return [
            {'user': 'Менеджер' if message.user.is_manager else "Пользователь",
             'content': message.content,
             'time': message.timestamp}
            for message in messages
        ]

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        # Получаем сообщение и сохраняем его
        message = text_data_json['message']
        username = self.scope['user']

        room = await self.get_or_create_room(self.scope['url_route']['kwargs']['id_room'])
        await self.save_message(username, room, message)

        # Отправляем сообщение в комнату
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f"{'Менеджер' if username.is_manager else 'Пользователь'}: {message}"
            }
        )

    @database_sync_to_async
    def save_message(self, user, room, content):
        Message.objects.create(user=user, room=room, content=content)

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
