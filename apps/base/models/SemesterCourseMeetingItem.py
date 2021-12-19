from django.db import models

class SemesterCourseMeetingItem(models.Model):

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

    semester_course = models.ForeignKey('base.SemesterCourse', on_delete=models.CASCADE)

    day = models.IntegerField(choices=DAY_CHOICES)

    from_time = models.DateTimeField()
    to_time = models.DateTimeField()

    def __str__(self):
        return f'{self.DAY_CHOICES[self.day-1][-1]} ({self.from_time} - {self.to_time})'
    
    def save(self, *args, **kwargs):
        
        if self.from_time >= self.to_time:
            raise AttributeError(f'from_time {self.from_time} is >= then to_time {self.to_time}')
        
        super(SemesterCourseMeetingItem, self).save(*args, **kwargs)