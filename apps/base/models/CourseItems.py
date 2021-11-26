from django.db import models

class CourseItems(models.Model):

    semester_course = models.ForeignKey('base.SemesterCourse')

    date = models.DateField()
    media = models.ForeignKey('base.Media', on_delete=models.SET_NULL, null=True)