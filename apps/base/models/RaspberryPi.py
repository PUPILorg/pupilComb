from django.db import models
import cv2
from django.utils import timezone

class RaspberryPi(models.Model):

    is_active = models.BooleanField(default=False)
    room_number = models.IntegerField(default=-1)
    video_input_port = models.IntegerField(default=0)

    room = models.ForeignKey('base.Room', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.room_number}'

    def record(self, file_path :str, stop_time: timezone) -> None:

        vid_capture = cv2.VideoCapture(self.video_input_port)
        vid_code = cv2.VideoWriter_fourcc(*'XVID')
        output = cv2.VideoWriter(file_path, vid_code, 20.0, (1920, 1080))

        while True:

            ret, frame = vid_capture.read()
            output.write(frame)

            if timezone.now() < stop_time:
                break

        vid_capture.release()
        output.release()
