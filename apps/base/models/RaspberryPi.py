from time import sleep

import cv2
from django.db import models
from django.utils import timezone

from apps.base.utils.CamUtils import WebCam, VideoWriter
from queue import Queue

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

    def record(self, file_path :str, end_time: float) -> None:
        frame_queue = Queue()

        wc = WebCam(src=0, width=640, height=480, queue=frame_queue, end_time=end_time)
        wc.start()
        fourcc = cv2.VideoWriter_fourcc(*'XVID')

        sleep(5)
        fps = frame_queue.qsize() / 5

        vw = VideoWriter(filepath=file_path, width=640, height=480, queue=frame_queue, fps=fps, fourcc=fourcc)
        vw.start()

        wc.join()
        vw.join()

    def set_active(self):
        self.is_active = True