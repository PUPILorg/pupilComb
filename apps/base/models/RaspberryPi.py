import time

from django.db import models

from apps.base.utils.ffmpeg_utils import FFMPEG
from .Media import Media
from .CourseItems import CourseItems


class RaspberryPi(models.Model):

    is_active = models.BooleanField(default=False)
    camera_path = models.CharField(max_length=50)

    room = models.ForeignKey('base.Room', on_delete=models.CASCADE)

    queue_name = models.CharField(null=False, blank=True, max_length=100)

    def save(self, *args, **kwargs):
        
        self.queue_name = f'pi_{self.id}'
        super(RaspberryPi, self).save(*args, **kwargs)
        self.set_active()

    def __str__(self):
        return f'{self.room}'

    def record(self, file_path :str, end_time: float, course_id: int) -> None:
        duration = end_time - time.time()
        ffmpeg = FFMPEG(src=self.camera_path, duration=duration, file_path=file_path)
        ffmpeg.start()

        media = Media.objects.create(file=file_path)
        CourseItems.objects.create(semester_course_id=course_id, media_id=media.id)


    def set_active(self):
        self.is_active = True