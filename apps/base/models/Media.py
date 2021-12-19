from django.db import models

class Media(models.Model):

    file = models.FileField()

    def __str__(self):
        return f'{self.file.name}'