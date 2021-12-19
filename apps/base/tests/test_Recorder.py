from .TestCaseWithData import TestCaseWithData

class RecorderTestCase(TestCaseWithData):

    def test_queue_create(self):
        self.assertEqual(f'pi_{self.recorder.id}', self.recorder.queue_name)