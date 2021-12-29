from apps.base.models.Media import Media

from apps.base.tests.TestCaseWithData import TestCaseWithData
from pupilComb.settings import BASE_DIR

from django.core.files.storage import default_storage

class MediaTestCase(TestCaseWithData):

    test_video = f'{BASE_DIR}/apps/base/tests/sample_test_videos/out_cam.mp4'
    upload_location = 'tests/upload_media_test.mp4'

    def test_create_with_upload_media(self):
        Media.objects.create_with_upload(semester_course_recording_item=self.semester_course_recording_item,
                             file=self.test_video, upload_location = self.upload_location)
        # TODO: Fish this test to make sure files actually get uploaded to the correct path
        self.assertTrue(default_storage.exists(self.upload_location))

    def test_delete_media(self):
        m = Media.objects.create(semester_course_recording_item=self.semester_course_recording_item,
                             file=self.upload_location)

        m.delete()

        self.assertFalse(default_storage.exists(self.upload_location))


