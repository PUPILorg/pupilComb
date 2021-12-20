from apps.base.tests.TestCaseWithData import TestCaseWithData
import os
from pupilComb.settings import BASE_DIR
from django.utils import timezone
from apps.base.models.Media import Media
from apps.base.models.CourseItems import CourseItems

class RecorderOnDeviceTestCase(TestCaseWithData):

    test_video_folder = f'{BASE_DIR}/apps/base/pi_tests/recorder_onDevice_test_videos/'

    @classmethod
    def setUpClass(cls) -> None:
        if not(os.path.exists(cls.test_video_folder) and os.path.isdir(cls.test_video_folder)):
            os.mkdir(cls.test_video_folder)

    @classmethod
    def tearDownClass(cls) -> None:
        os.rmdir(cls.test_video_folder)

    def test_record(self):
        file_path =f'{self.test_video_folder}recorder_output.mp4'
        self.recorder.record(file_path=file_path,
                             end_time=timezone.now() + timezone.timedelta(seconds=15),
                             semester_course_id=self.semester_course.id)

        self.assertTrue(
            Media.objects.filter(
                file_path=file_path
            ).exists()
        )

        media = Media.objects.filter(file_path=file_path)

        self.assertTrue(
            CourseItems.objects.filter(
                media_id=media.id,
                semester_course_id=self.semester_course.id
            )
        )