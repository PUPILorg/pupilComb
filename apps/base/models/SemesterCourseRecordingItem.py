from django.db import models

class SemesterCourseRecordingItem(models.Model):

    semester_course = models.ForeignKey('base.SemesterCourse', on_delete=models.CASCADE)
    date = models.DateField(auto_created=True)