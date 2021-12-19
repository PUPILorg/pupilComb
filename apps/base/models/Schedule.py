from django.db import models

class Schedule(models.Model):

    from_date = models.DateField()
    to_date = models.DateField()

    def __str__(self):
        return f'{self.from_date} - {self.to_date}'

    def save(self, *args, **kwargs):

        if self.to_date <= self.from_date:
            raise AttributeError(f'end date: {self.to_date} is smaller then from date: {self.from_date}')

        super(Schedule, self).save(*args, **kwargs)