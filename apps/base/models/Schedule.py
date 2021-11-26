from django.db import models

class Schedule(models.Model):

    from_date = models.DateField()
    to_date = models.DateField()

    def __str__(self):
        return f'{self.from_date} - {self.to_date}'