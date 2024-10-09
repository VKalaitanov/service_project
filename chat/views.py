from django.db.models import OuterRef, Subquery
from django.shortcuts import render
from .models import Message
from django.views.generic import ListView


class GetAllViews(ListView):
    template_name = 'chat/all_chat.html'
    context_object_name = 'chat'

    def get_queryset(self):
        # Получаем все уникальные room_name
        unique_rooms = Message.objects.values('room_name').distinct()

        # Теперь для каждой уникальной комнаты получаем последнее сообщение
        latest_messages = Message.objects.filter(
            room_name=OuterRef('room_name')
        ).order_by('-timestamp')

        # Запрашиваем последние сообщения для каждой уникальной комнаты
        return Message.objects.filter(
            room_name__in=unique_rooms
        ).annotate(last_message=Subquery(latest_messages.values('content')[:1]))

def index(request, room_name):
    messages = Message.objects.filter(room_name=room_name).order_by('timestamp')
    return render(request, 'chat/test.html', {
        'room_name': room_name,
        'messages': messages
    })


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})
