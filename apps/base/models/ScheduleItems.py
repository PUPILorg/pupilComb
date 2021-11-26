from django.db import models

class ScheduleItems(models.Model):

    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4

    DAY_CHOICES = [
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday')
    ]

    day = models.IntegerField(choices=DAY_CHOICES)

    from_time = models.TimeField()
    to_time = models.TimeField()

    def __str__(self):
        return f'{self.DAY_CHOICES[self.day][-1]} ({self.from_time} - {self.to_time})'