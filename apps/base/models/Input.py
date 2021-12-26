from django.db import models

from apps.base.utils.recording.enums import Codec, VideoContainer

class Input(models.Model):

    TYPE_webcam = 0
    TYPE_video_capture = 1

    TYPE_CHOICES = [
        (TYPE_webcam, 'webcam'),
        (TYPE_video_capture, 'video_capture')
    ]

    recorder = models.ForeignKey('base.Recorder', on_delete=models.CASCADE)
    path_to_input = models.CharField(max_length=20)
    codec = models.CharField(
        max_length=255,
        choices=Codec.choices()
    )
    file_container = models.CharField(
        max_length=255,
        choices=VideoContainer.choices()
    )
    type_device = models.IntegerField(
        default=0,
        choices=TYPE_CHOICES
    )

    class Meta:
        unique_together = ['recorder', 'path_to_input']

    def __str__(self) -> str:
        return f'{self.recorder.id} -- {self.path_to_input}'

    def save(self, *args, **kwargs):
        if self.file_container == VideoContainer.MOV and self.codec == Codec.CODEC_H264 or \
                self.file_container == VideoContainer.MP4 and self.codec == Codec.CODEC_MJPEG:
            raise AttributeError('container codec mismatch')

        super(Input, self).save(*args, **kwargs)