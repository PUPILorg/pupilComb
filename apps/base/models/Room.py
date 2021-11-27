from django.db import models

class Room(models.Model):

    room_num = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.room_num}'