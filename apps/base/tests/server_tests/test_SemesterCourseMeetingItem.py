from apps.base.tests.TestCaseWithData import TestCaseWithData

from apps.base.models.SemesterCourseMeetingItem import SemesterCourseMeetingItem
from django.utils import timezone

class SemesterCourseMeetingItemTestCase(TestCaseWithData):

    def test_same_time_raises(self):
        with self.assertRaises(AttributeError):

            time = timezone.now()

            SemesterCourseMeetingItem.objects.create(semester_course=self.semester_course,
                                                     day=1,
                                                     from_time=time,
                                                     to_time=time)

    def test_flipped_time_raises(self):
        with self.assertRaises(AttributeError):

            from_time = timezone.now() + timezone.timedelta(hours=2)
            to_time = timezone.now()

            SemesterCourseMeetingItem.objects.create(semester_course=self.semester_course,
                                                     day=1,
                                                     from_time=from_time,
                                                     to_time=to_time)
