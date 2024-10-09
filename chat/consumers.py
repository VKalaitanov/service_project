from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()
            return

        other_user_id = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = str(other_user_id)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Подгружаем историю сообщений при подключении
        messages = await self.get_message_history(self.room_group_name)
        for message in messages:
            await self.send(text_data=json.dumps({
                'message': f"{message['user']}: {message['content']}"
            }))

    @database_sync_to_async
    def get_message_history(self, room_name):
        messages = Message.objects.filter(room_name=room_name).order_by('timestamp')
        return [{'user': message.user, 'content': message.content} for message in messages]

    async def disconnect(self, close_code):
        # Отключаем пользователя от группы при разрыве соединения
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Получаем сообщение от WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = self.scope['user']

        # Сохраняем сообщение в базе данных
        await self.save_message(username, self.room_group_name, message)

        # Отправляем сообщение в комнату
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f"{'Менеджер' if username.is_manager else 'Пользователь'}: {message}"
            }
        )

    @database_sync_to_async
    def save_message(self, user, room_name, content):
        Message.objects.create(user=user, room_name=room_name, content=content)

    # Получаем сообщение из группы
    async def chat_message(self, event):
        message = event['message']

        # Отправляем сообщение обратно на WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
#
#
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         if self.scope['user'].is_anonymous:
#             await self.close()  # Закрываем соединение, если пользователь не авторизован
#             return
#
#         # Получаем ID другого пользователя из URL
#
#         other_user_id = self.scope['url_route']['kwargs']['room_name']
#
#         # Генерируем уникальное название комнаты для пары пользователей
#         self.room_group_name = str(other_user_id)
#
#         # Присоединяем пользователя к комнате
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         # Принимаем соединение
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         # Отключаем пользователя от группы при разрыве соединения
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     # Получаем сообщение от WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#
#         # Получаем имя пользователя
#         username = self.scope['user']
#
#         # Отправляем сообщение в комнату (только пользователю)
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': f"{'Менеджер' if username.is_manager else 'Пользователь'}: {message}"
#             }
#         )
#
#     # Получаем сообщение из группы
#     async def chat_message(self, event):
#         message = event['message']
#
#         # Отправляем сообщение обратно на WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
