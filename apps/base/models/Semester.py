from django.db import models

class Semester(models.Model):

    FALL_21 = 'F21'
    SPRING_22 = 'S22'

    SEMESTER_CHOICES = [
        (FALL_21, 'Fall 21'),
        (SPRING_22, 'Spring 22')
    ]

    semester = models.CharField(max_length=3, choices=SEMESTER_CHOICES, default=FALL_21)

    def __str__(self):
        return f'{self.semester}'