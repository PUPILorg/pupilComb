from django.db import models

class CourseSection(models.Model):

    course = models.ForeignKey('base.Course', on_delete=models.CASCADE)
    section_num = models.IntegerField()

    room = models.ForeignKey('base.Room', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.section_num}'
