import time

from django.db import models

from apps.base.utils.recording_utils import Recording
from .Media import Media
from .CourseItems import CourseItems


class Recorder(models.Model):

    is_active = models.BooleanField(default=True)
    camera_path = models.CharField(max_length=50)

    room = models.ForeignKey('base.Room', on_delete=models.CASCADE)

    queue_name = models.CharField(null=False, blank=True, max_length=100, unique=True, editable=False)

    def __str__(self):
        return f'{self.room}'

    def record(self, file_path :str, end_time: float, semester_course_id: int) -> None:
        duration = end_time - time.time()
        recording = Recording(src=self.camera_path, duration=duration, file_path=file_path)
        recording.start()

        media = Media.objects.create(file=file_path)
        CourseItems.objects.create(semester_course_id=semester_course_id, media_id=media.id)


    def set_active(self):
        self.is_active = True
        self.save()