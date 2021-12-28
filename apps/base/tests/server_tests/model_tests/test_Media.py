from apps.base.tests.TestCaseWithData import TestCaseWithData
from pupilComb.s3_utils import s3
from pupilComb.settings import BASE_DIR

class MediaTestCase(TestCaseWithData):

    test_video = f'{BASE_DIR}/apps/base/tests/sample_test_videos/out_cam.mp4'

    def test_create_media(self):
        pass
