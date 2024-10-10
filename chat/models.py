from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Room(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='room')
    managers = models.ManyToManyField(User, related_name='managed_rooms')

    def get_absolute_url(self):
        return reverse('index', kwargs={'id_room': self.pk})

    def __str__(self):
        return f"Room {self.id} for {self.user.username}"


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"
