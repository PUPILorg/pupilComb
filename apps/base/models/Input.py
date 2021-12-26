from django.db import models

from apps.base.utils.recording.enums import Codec, VideoContainer

class Input(models.Model):

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

    class Meta:
        unique_together = ['recorder', 'path_to_input']

    def __str__(self) -> str:
        return f'{self.recorder.id} -- {self.path_to_input}'