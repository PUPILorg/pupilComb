from apps.base.models.Media import Media

from apps.base.tests.TestCaseWithData import TestCaseWithData
from pupilComb.settings import BASE_DIR

from django.core.files.storage import default_storage

from apps.base.utils.data_utils.uploading_utils import UploadToS3Threaded

class MediaTestCase(TestCaseWithData):

    test_video = f'{BASE_DIR}/apps/base/tests/sample_test_videos/out_cam.mp4'
    upload_location = 'tests/upload_media_test.mp4'

    def test_create_with_upload_media(self):
        if default_storage.exists(self.upload_location):
            default_storage.delete(self.upload_location)

        media = Media.objects.create(semester_course_recording_item=self.semester_course_recording_item,
                             file = self.upload_location)

        upload_thread = UploadToS3Threaded(local_file = self.test_video,
                                           upload_path = self.upload_location,
                                           media_id = media.id)
        upload_thread.start()
        upload_thread.join()

        self.assertTrue(default_storage.exists(self.upload_location))
        self.assertTrue(
            Media.objects.filter(
                semester_course_recording_item = self.semester_course_recording_item,
                file = self.upload_location,
                uploaded=True
            ).exists()
        )

    def test_delete_media(self):

        if not (default_storage.exists(self.upload_location)):
            with open(self.test_video, 'rb') as f:
                default_storage.save(self.upload_location, f)

        m, _ = Media.objects.get_or_create(semester_course_recording_item=self.semester_course_recording_item,
                             file=self.upload_location)

        m.delete()

        self.assertFalse(default_storage.exists(self.upload_location))


