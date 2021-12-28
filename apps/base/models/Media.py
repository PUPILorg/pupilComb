from django.db import models

class Media(models.Model):

    semester_course_recording_item = models.ForeignKey('base.SemesterCourseRecordingItem', on_delete=models.CASCADE)
    file = models.FileField()

    def __str__(self):
        return f'{self.file.name}'