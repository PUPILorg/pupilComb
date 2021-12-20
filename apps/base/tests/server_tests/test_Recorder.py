import django.db

from apps.base.tests.TestCaseWithData import TestCaseWithData
from apps.base.models.Recorder import Recorder

class RecorderTestCase(TestCaseWithData):

    def test_queue_create(self):
        self.assertEqual(f'pi_{self.recorder.id}', self.recorder.queue_name)

    def test_two_recorder_one_room_exception(self):
        with self.assertRaises(django.db.IntegrityError):
            Recorder.objects.create(
                camera_path='/dev/video0',
                room=self.room
            )
