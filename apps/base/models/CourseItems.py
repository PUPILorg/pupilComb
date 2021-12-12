from django.db import models

class CourseItems(models.Model):

    semester_course = models.ForeignKey('base.SemesterCourse', on_delete=models.CASCADE)

    date = models.DateField(auto_created=True)
    media = models.ForeignKey('base.Media', on_delete=models.SET_NULL, null=True)