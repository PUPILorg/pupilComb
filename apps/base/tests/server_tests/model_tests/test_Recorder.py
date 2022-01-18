import django.db

from apps.base.tests.TestCaseWithData import TestCaseWithData
from apps.base.models.Recorder import Recorder

class RecorderTestCase(TestCaseWithData):

    def test_queue_create(self):
        self.assertEqual(f'recorder_{self.recorder.id}', self.recorder.queue_name)

    def test_two_recorder_one_room_exception(self):
        with self.assertRaises(django.db.IntegrityError):
            Recorder.objects.create(
                room=self.room
            )

