from django.db import models
from django.utils import timezone

from apps.base.utils.recording.recording_utils import Recording
from .Media import Media
from .CourseItems import CourseItems


class Recorder(models.Model):

    is_active = models.BooleanField(default=True)
    camera_path = models.CharField(max_length=50)

    room = models.OneToOneField('base.Room', on_delete=models.CASCADE)

    queue_name = models.CharField(null=False, blank=True, max_length=100, unique=True, editable=False)

    def __str__(self):
        return f'{self.room}'

    def record(self, file_path :str, end_time: float, semester_course_id: int) -> None:
        """

        records the video on the pi and sets up the Media and CourseItems models

        :param file_path: filepath of the video
        :param end_time: end_time of the video in datetime format
        :param semester_course_id: id of the semester_course the video is associated with
        :return: None
        """
        duration = (end_time - timezone.now()).seconds
        recording = Recording(src=self.camera_path, duration=duration, file_path=file_path)
        recording.record()

        media = Media.objects.create(file=file_path)
        CourseItems.objects.create(semester_course_id=semester_course_id, media_id=media.id)


    def set_active(self) -> None:
        """
        sets the Recorder status to active
        :return: None
        """
        self.is_active = True
        self.save()