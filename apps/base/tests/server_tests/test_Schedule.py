from django.utils import timezone

from apps.base.tests.TestCaseWithData import TestCaseWithData

from apps.base.models.Schedule import Schedule

class ScheduleTestCase(TestCaseWithData):

    def test_raise_assertion_flipped_dates(self):
        with self.assertRaises(AttributeError):
            Schedule.objects.create(from_date = timezone.now().date() + timezone.timedelta(days=10),
                                    to_date = timezone.now().date())

    def test_raise_assertion_same_date(self):
        with self.assertRaises(AttributeError):
            Schedule.objects.create(from_date = timezone.now().date(),
                                    to_date = timezone.now().date())