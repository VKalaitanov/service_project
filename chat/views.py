from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .models import Message, Room
from django.views.generic import ListView


class GetAllViews(ListView):
    template_name = 'chat/all_chat.html'
    context_object_name = 'chat'

    def get_queryset(self):
        return Room.objects.all()


def is_manager(user):
    return user.groups.filter(name='Менеджеры').exists()


@user_passes_test(is_manager)
def index(request, id_room):
    messages = Message.objects.filter(room=id_room).order_by('timestamp').select_related('user')
    return render(request, 'chat/test.html', {
        'id_room': id_room,
        'messages': messages
    })
