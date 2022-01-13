from apps.base.models.Media import Media

from apps.base.tests.TestCaseWithData import TestCaseWithData
from pupilComb.settings import BASE_DIR

from django.core.files.storage import default_storage

class MediaTestCase(TestCaseWithData):

    test_video = f'{BASE_DIR}/apps/base/tests/sample_test_videos/out_cam.mp4'
    upload_location = 'tests/upload_media_test.mp4'

    def test_delete_media(self):

        if not (default_storage.exists(self.upload_location)):
            with open(self.test_video, 'rb') as f:
                default_storage.save(self.upload_location, f)

        m, _ = Media.objects.get_or_create(semester_course_recording_item=self.semester_course_recording_item,
                             file=self.upload_location)

        m.delete()

        self.assertFalse(default_storage.exists(self.upload_location))


