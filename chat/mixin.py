from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from .models import Message, Room


class AsyncMixinMethods:
    """Класс для асинхронных методов для Consumers"""
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

    @database_sync_to_async
    def save_message(self, user, room, content):
        """Асинхронный метод сохраняет сообщение"""
        Message.objects.create(user=user, room=room, content=content)

    @database_sync_to_async
    def is_manager(self, user):
        """Асинхронный метод проверяет наличия пользователя в группе менеджеров"""
        return user.groups.filter(name='Менеджеры').exists()

    @database_sync_to_async
    def get_or_create_room(self, other_user_id):
        """Асинхронный метод создает комнату для общения"""
        other_user = get_user_model().objects.get(id=other_user_id)
        room, created = Room.objects.get_or_create(user=other_user)
        return room
