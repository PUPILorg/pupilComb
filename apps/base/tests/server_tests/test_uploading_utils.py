import os

from apps.base.tests.data_factory import SemesterCourseRecordingItemFactory
from apps.base.models.Media import Media

from django.core.files.storage import default_storage
from django.test import TransactionTestCase

from apps.base.utils.data_utils.uploading_utils import UploadToS3Threaded

from pupilComb.settings import BASE_DIR

class UploadingToS3ThreadedTestCase(TransactionTestCase):

    test_video_file = f'{BASE_DIR}/apps/base/tests/sample_test_videos/upload_utils_test_video/out_cam.mp4'


    def test_upload(self):
        #find a fix for this (and why is the data factory not working) # TODO: fix the data_factory.py
        scri = SemesterCourseRecordingItemFactory()
        media = Media.objects.create(
            semester_course_recording_item=scri,
            file='tests/threaded_upload.mp4',
            uploaded=False
        )

        upload_thread = UploadToS3Threaded(local_file= self.test_video_file,
                                           upload_path='tests/threaded_upload.mp4',
                                           media_id=media.id)

        upload_thread.start()
        upload_thread.join()

        self.assertTrue(default_storage.exists('tests/threaded_upload.mp4'))
        self.assertFalse(os.path.isfile(self.test_video_file))
        self.assertTrue(media.uploaded)