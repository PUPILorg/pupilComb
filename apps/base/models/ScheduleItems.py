from django.db import models

class ScheduleItems(models.Model):

    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5

    DAY_CHOICES = [
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday')
    ]

    schedule = models.ForeignKey('base.Schedule', on_delete=models.CASCADE)

    day = models.IntegerField(choices=DAY_CHOICES)

    from_time = models.TimeField()
    to_time = models.TimeField()

    def __str__(self):
        return f'{self.DAY_CHOICES[self.day][-1]} ({self.from_time} - {self.to_time})'