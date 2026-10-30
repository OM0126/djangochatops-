from django.db import models
from django.utils import timezone


class Room(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Message(models.Model):
    value = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    user = models.CharField(max_length=100)
    room = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user}: {self.value[:50]}"