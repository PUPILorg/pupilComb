from apps.base.tests.TestCaseWithData import TestCaseWithData
import os
from pupilComb.settings import BASE_DIR
from django.utils import timezone
from apps.base.models.Media import Media
from apps.base.models.SemesterCourseRecordingItem import SemesterCourseRecordingItem

from django.core.files.storage import default_storage

class RecorderOnDeviceTestCase(TestCaseWithData):
    """
    ALL ACTUAL RECORDING UTILITY SHOULD BE TESTED IN test_recording_utils.py
    """

    test_video_folder = f'test/'

    def test_record(self):
        self.recorder.record(folder=self.test_video_folder,
                             end_time=timezone.now() + timezone.timedelta(seconds=30),
                             semester_course_id=self.semester_course.id)

        filepath_folder = f'{self.test_video_folder}{self.semester_course.id}/{timezone.now().date()}/'

        scri = SemesterCourseRecordingItem.objects.get(date=timezone.now().date())

        self.assertTrue(
            Media.objects.filter(
                semester_course_recording_item=scri,
                file=f'{filepath_folder}webcam.mp4'
            ).exists()
        )

        self.assertTrue(
            Media.objects.filter(
                semester_course_recording_item=scri,
                file=f'{filepath_folder}screen.mov'
            ).exists()
        )