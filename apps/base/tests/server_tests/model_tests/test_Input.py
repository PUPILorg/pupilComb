from apps.base.tests.TestCaseWithData import TestCaseWithData
import django.db.utils

from apps.base.utils.recording.enums import Codec, VideoContainer

from apps.base.models.Input import Input

class InputTestCase(TestCaseWithData):

    def test_unique(self):
        with self.assertRaises(django.db.utils.IntegrityError):
            Input.objects.create(
                recorder = self.recorder,
                path_to_input = '/dev/video0',
                codec = Codec.CODEC_H264,
                file_container = VideoContainer.MP4
            )

    def test_mismatch_h264_mov(self):
        with self.assertRaises(AttributeError):
            Input.objects.create(
                recorder=self.recorder,
                path_to_input='/dev/video1',
                codec=Codec.CODEC_H264,
                file_container=VideoContainer.MOV
            )

        self.assertFalse(
            Input.objects.filter(
                recorder=self.recorder,
                path_to_input='/dev/video1',
                codec=Codec.CODEC_H264,
                file_container=VideoContainer.MOV
            ).exists()
        )

    def test_mismatch_mjpeg_mp4(self):
        with self.assertRaises(AttributeError):
            Input.objects.create(
                recorder=self.recorder,
                path_to_input='/dev/video1',
                codec=Codec.CODEC_MJPEG,
                file_container=VideoContainer.MP4
            )

        self.assertFalse(
            Input.objects.filter(
                recorder=self.recorder,
                path_to_input='/dev/video1',
                codec=Codec.CODEC_MJPEG,
                file_container=VideoContainer.MP4
            ).exists()
        )
