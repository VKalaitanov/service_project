from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth import get_user_model

from .models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Метод подключает пользователя к чату"""
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
        """Асинхронный метод создает комнату для общения"""
        other_user = get_user_model().objects.get(id=other_user_id)
        room, created = Room.objects.get_or_create(user=other_user)
        return room

    @database_sync_to_async
    def get_message_history(self, room):
        """Асинхронный метод выдает историю чата"""
        messages = room.messages.order_by('timestamp')
        return [
            {'user': 'Менеджер' if message.user.groups.filter(name='Менеджеры') else "Пользователь",
             'content': message.content,
             'time': message.timestamp}
            for message in messages
        ]

    async def disconnect(self, close_code):
        """Метод отключения пользователя от чата"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Метод для отправки сообщения в чат"""
        text_data_json = json.loads(text_data)

        message = text_data_json['message']
        user = self.scope['user']

        room = await self.get_or_create_room(self.scope['url_route']['kwargs']['id_room'])
        await self.save_message(user, room, message)

        # Отправляем сообщение в комнату
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f"{'Менеджер' if await self.is_manager(user) else 'Пользователь'}: {message}"
            }
        )

    @database_sync_to_async
    def save_message(self, user, room, content):
        """Асинхронный метод сохраняет сообщение"""
        Message.objects.create(user=user, room=room, content=content)

    @database_sync_to_async
    def is_manager(self, user):
        """Асинхронный метод проверяет наличия пользователя в группе менеджеров"""
        return user.groups.filter(name='Менеджеры').exists()

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
