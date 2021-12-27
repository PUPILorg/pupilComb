import unittest
from apps.base.utils.recording.recording_utils import Recording, Resolution, Codec

from .utils import get_props

import os
from pupilComb.settings import BASE_DIR

class RecordingUtilTest(unittest.TestCase):

    test_video_folder = f'{BASE_DIR}/apps/base/pi_tests/recording_utils_test_videos/'
    test_webcam_file = f'{test_video_folder}webcam.mp4'
    test_video_capture_file = f'{test_video_folder}videocapure.mov'

    duration = 60
    min_fps = 25


    # before each test check these and make sure they are right
    webcam_source = '/dev/video2'
    video_capture_src = '/dev/video0'

    ################################# SET UP #####################################

    @classmethod
    def setUpClass(cls) -> None:
        if not(os.path.exists(cls.test_video_folder) and os.path.isdir(cls.test_video_folder)):
            os.mkdir(cls.test_video_folder)

    @classmethod
    def tearDownClass(cls) -> None:
        os.rmdir(cls.test_video_folder)

    def setUp(self) -> None:
        """
        sets up a working recorder with a duration of 60 seconds
        :return:
        """

        self.working_recorder = Recording(webcam_src=self.video_capture_source, video_capture_src=self.webcam_source,
                                     webcam_output_file=f'{self.test_webcam_file}',
                                     video_capture_output_file=f'{self.test_video_capture_file}',
                                     webcam_codec=Codec.CODEC_H264, video_capture_codec=Codec.CODEC_MJPEG,
                                     resolution=Resolution.RES_640x480, duration=self.suration)

    def tearDown(self) -> None:
        if os.path.exists(self.test_webcam_file):
            os.remove(self.test_webcam_file)

        if os.path.exists(self.test_video_capture_file):
            os.remove(self.test_video_capture_file)

    ################################ SET UP DONE ####################################

    def test_raise_exception_0_time(self):
        with self.assertRaises(AttributeError):
            Recording(webcam_src=self.video_capture_source, video_capture_src=self.webcam_source,
                    webcam_output_file=f'{self.test_webcam_file}',
                    video_capture_output_file=f'{self.test_video_capture_file}',
                    webcam_codec=Codec.CODEC_H264, video_capture_codec=Codec.CODEC_MJPEG,
                    resolution=Resolution.RES_640x480, duration=0)

    def test_raise_exception_neg_time(self):
        with self.assertRaises(AttributeError):
            Recording(webcam_src=self.video_capture_source, video_capture_src=self.webcam_source,
                     webcam_output_file=f'{self.test_webcam_file}',
                     video_capture_output_file=f'{self.test_video_capture_file}',
                     webcam_codec=Codec.CODEC_H264, video_capture_codec=Codec.CODEC_MJPEG,
                     resolution=Resolution.RES_640x480, duration=-10)

    def test_raise_exception_wrong_file_container(self):
        with self.assertRaises(AttributeError):
            Recording(webcam_src=self.video_capture_source, video_capture_src=self.webcam_source,
                    webcam_output_file=f'{self.test_webcam_file}',
                    video_capture_output_file=f'{self.test_video_capture_file}',
                    webcam_codec=Codec.CODEC_MJPEG, video_capture_codec=Codec.CODEC_H264,
                    resolution=Resolution.RES_640x480, duration=self.suration)

    def test_raises_duplicate_video(self):
        self.working_recorder.record()
        with self.assertRaises(AttributeError):
            self.working_recorder.record()

    def test_one_minute_video(self):
        self.working_recorder.record()

        webcam_file_props = get_props(self.test_webcam_file)
        video_capture_prop = get_props(self.test_video_capture_file)

        self.assertEqual(webcam_file_props.height, 1920)
        self.assertEqual(webcam_file_props.width, 1080)
        self.assertEqual(webcam_file_props.codec, Codec.CODEC_H264)
        self.assertAlmostEqual(webcam_file_props.duration, self.duration)
        self.assertTrue(webcam_file_props.fps - self.min_fps > 0)

        self.assertEqual(video_capture_prop.height, 1920)
        self.assertEqual(video_capture_prop.width, 1080)
        self.assertEqual(video_capture_prop.codec, Codec.CODEC_MJPEG)
        self.assertAlmostEqual(video_capture_prop.duration, self.duration)
        self.assertTrue(video_capture_prop.fps - self.min_fps > 0)

    def test_unplug_hdmi(self):
        attentive = input("unplug the hdmi after 20 seconds: "
                          "(any input is fine just need to make sure there is someone to unplug the hdmi)")

        self.working_recorder.record()

        webcam_file_props = get_props(self.test_webcam_file)
        video_capture_prop = get_props(self.test_video_capture_file)

        self.assertEqual(webcam_file_props.height, 1920)
        self.assertEqual(webcam_file_props.width, 1080)
        self.assertEqual(webcam_file_props.codec, Codec.CODEC_H264)
        self.assertAlmostEqual(webcam_file_props.duration, self.duration)
        self.assertTrue(webcam_file_props.fps - self.min_fps > 0)

        self.assertEqual(video_capture_prop.height, 1920)
        self.assertEqual(video_capture_prop.width, 1080)
        self.assertEqual(video_capture_prop.codec, Codec.CODEC_MJPEG)
        self.assertAlmostEqual(video_capture_prop.duration, self.duration)
        self.assertTrue(video_capture_prop.fps - self.min_fps > 0)

    def test_plug_in_hdmi(self):
        attentive = input("unplug the hdmi and plug it in after 20s "
                          "(any input is fine just need to make sure there is someone to plug in the hdmi)")

        self.working_recorder.record()

        webcam_file_props = get_props(self.test_webcam_file)
        video_capture_prop = get_props(self.test_video_capture_file)

        self.assertEqual(webcam_file_props.height, 1920)
        self.assertEqual(webcam_file_props.width, 1080)
        self.assertEqual(webcam_file_props.codec, Codec.CODEC_H264)
        self.assertAlmostEqual(webcam_file_props.duration, self.duration)
        self.assertTrue(webcam_file_props.fps - self.min_fps > 0)

        self.assertEqual(video_capture_prop.height, 1920)
        self.assertEqual(video_capture_prop.width, 1080)
        self.assertEqual(video_capture_prop.codec, Codec.CODEC_MJPEG)
        self.assertAlmostEqual(video_capture_prop.duration, self.duration)
        self.assertTrue(video_capture_prop.fps - self.min_fps > 0)

    def test_no_hdmi(self):
        attentive = input("unplug the hdmi "
                          "(any input is fine just need to make sure there is someone to unplug the hdmi)")

        self.working_recorder.record()

        webcam_file_props = get_props(self.test_webcam_file)
        video_capture_prop = get_props(self.test_video_capture_file)

        self.assertEqual(webcam_file_props.height, 1920)
        self.assertEqual(webcam_file_props.width, 1080)
        self.assertEqual(webcam_file_props.codec, Codec.CODEC_H264)
        self.assertAlmostEqual(webcam_file_props.duration, self.duration)
        self.assertTrue(webcam_file_props.fps - self.min_fps > 0)

        self.assertEqual(video_capture_prop.height, 1920)
        self.assertEqual(video_capture_prop.width, 1080)
        self.assertEqual(video_capture_prop.codec, Codec.CODEC_MJPEG)
        self.assertAlmostEqual(video_capture_prop.duration, self.duration)
        self.assertTrue(video_capture_prop.fps - self.min_fps > 0)
