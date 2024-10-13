import json

from channels.generic.websocket import AsyncWebsocketConsumer

from .mixin import AsyncMixinMethods


class ChatConsumer(AsyncWebsocketConsumer, AsyncMixinMethods):
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

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
