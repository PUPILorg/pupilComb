import django.db.utils
from apps.base.models.Room import Room
from .TestCaseWithData import TestCaseWithData

class RoomTestCase(TestCaseWithData):

    def test_unique(self):
        with self.assertRaises(django.db.utils.IntegrityError):
            Room.objects.create(room_num=self.room.room_num)