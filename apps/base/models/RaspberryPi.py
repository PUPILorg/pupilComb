from django.db import models
import cv2
from django.utils import timezone

class RaspberryPi(models.Model):

    is_active = models.BooleanField(default=False)
    video_input_port = models.IntegerField(default=0)

    room = models.ForeignKey('base.Room', on_delete=models.CASCADE)

    queue_name = models.CharField(null=False, blank=True, max_length=100)

    def save(self, *args, **kwargs):
        
        self.queue_name = f'pi_{self.id}'
        super(RaspberryPi, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.room}'

    def record(self, file_path :str, stop_time: timezone) -> None:
        """

        :TODO saving the video | setting up the Media and courseItem models

        records the video on the PI
        :param file_path: file where the recording should be stored
        :param stop_time: stop time for when the recording stops
        :return: nothing
        """

        vid_capture = cv2.VideoCapture(self.video_input_port)
        vid_code = cv2.VideoWriter_fourcc(*'XVID')
        output = cv2.VideoWriter(file_path, vid_code, 20.0, (1920, 1080))

        while timezone.now() < stop_time:

            ret, frame = vid_capture.read()
            output.write(frame)

        vid_capture.release()
        output.release()

    def set_active(self):
        self.is_active = True