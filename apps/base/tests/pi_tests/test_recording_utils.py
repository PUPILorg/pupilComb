import unittest
from apps.base.utils.recording_utils import Recording, Resolution, Encoding

from .utils import get_video_props

import os
from pupilComb.settings import BASE_DIR

class RecordingUtilTest(unittest.TestCase):

    test_video_folder = f'{BASE_DIR}/apps/base/pi_tests/recording_utils_test_videos/'

    @classmethod
    def setUpClass(cls) -> None:
        if not(os.path.exists(cls.test_video_folder) and os.path.isdir(cls.test_video_folder)):
            os.mkdir(cls.test_video_folder)

    @classmethod
    def tearDownClass(cls) -> None:
        os.rmdir(cls.test_video_folder)

    def test_raise_exception_0_time(self):
        with self.assertRaises(AttributeError):
            Recording(src='/dev/video0', output_file=f'{self.test_video_folder}output.mp4', duration=0)

    def test_raise_exception_wrong_file_container(self):
        with self.assertRaises(AttributeError):
            Recording(src='/dev/video0', output_file=f'{self.test_video_folder}output.avi', duration=0)

    def test_ten_second_video(self):
        r = Recording(src='/dev/video0', resolution=Resolution.RES_1920x1080, encoding=Encoding.ENCODING_H264,
                      output_file=f'{self.test_video_folder}output1080x1920.mp4', duration=10)
        r.start()

        height, width, fps, video_length = get_video_props(f'{self.test_video_folder}output.mp4')

        self.assertEqual(1920, height)
        self.assertEqual(1080, width)
        self.assertAlmostEqual(10, video_length)

    def test_lower_resolution(self):
        r = Recording(src='/dev/video0', resolution=Resolution.RES_640x480, encoding=Encoding.ENCODING_H264,
                      output_file=f'{self.test_video_folder}output640x480.mp4', duration=10)

        r.start()

        height, width, fps, video_length = get_video_props(f'{self.test_video_folder}output.mp4')

        self.assertEqual(640, height)
        self.assertEqual(480, width)
        self.assertAlmostEqual(10, video_length)