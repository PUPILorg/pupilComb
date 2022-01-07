from django.db import models

from django.utils import timezone

class SemesterCourseRecordingItem(models.Model):

    semester_course = models.ForeignKey('base.SemesterCourse', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now().date)