from apps.base.tests.TestCaseWithData import TestCaseWithData
import os
from pupilComb.settings import BASE_DIR
from django.utils import timezone
from apps.base.models.Media import Media
from apps.base.models.CourseItems import CourseItems

class RecorderOnDeviceTestCase(TestCaseWithData):
    """
    ALL ACTUAL RECORDING UTILITY SHOULD BE TESTED IN test_recording_utils.py
    """

    test_video_folder = f'{BASE_DIR}/apps/base/pi_tests/recorder_onDevice_test_videos/'

    @classmethod
    def setUpClass(cls) -> None:
        if not(os.path.exists(cls.test_video_folder) and os.path.isdir(cls.test_video_folder)):
            os.mkdir(cls.test_video_folder)

    @classmethod
    def tearDownClass(cls) -> None:
        os.rmdir(cls.test_video_folder)

    def test_record(self):
        self.recorder.record(folder=self.test_video_folder,
                             end_time=timezone.now() + timezone.timedelta(seconds=30),
                             semester_course_id=self.semester_course.id)

        filepath_folder = f'{self.test_video_folder}{self.semester_course.id}/{timezone.now().date()}/'

        self.assertTrue(
            Media.objects.filter(
                file=f'{filepath_folder}webcam.mp4'
            ).exists()
        )

        self.assertTrue(
            Media.objects.filter(
                file=f'{filepath_folder}screen.mov'
            ).exists()
        )

        media_webcam = Media.objects.get(file=f'{filepath_folder}webcam.mp4')
        media_screen = Media.objects.get(file=f'{filepath_folder}screen.mov')

        self.assertTrue(
            CourseItems.objects.filter(
                media_id=media_webcam.id,
                semester_course_id=self.semester_course.id
            ).exists()
        )

        self.assertTrue(
            CourseItems.objects.filter(
                media_id=media_screen.id,
                semester_course_id=self.semester_course.id
            ).exists()
        )