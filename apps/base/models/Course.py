from django.db import models

class Course(models.Model):

    identifier = models.CharField(max_length=10, unique=True)
    description = models.TextField()

    def __str__(self):
        return f'{self.identifier}'