from unittest import TestCase
from django.core.files.storage import default_storage

from apps.base.utils.data_utils.uploading_utils import UploadToS3Threaded

from pupilComb.settings import BASE_DIR

class UploadingToS3ThreadedTestCase(TestCase):

    test_video_file = f'{BASE_DIR}/apps/base/tests/sample_test_videos/out_cam.mp4'

    def test_upload(self):


        upload_thread = UploadToS3Threaded(local_file= self.test_video_file,
                                           upload_path='tests/threaded_upload.mp4')

        upload_thread.start()
        upload_thread.join()

        self.assertTrue(default_storage.exists('tests/threaded_upload.mp4'))