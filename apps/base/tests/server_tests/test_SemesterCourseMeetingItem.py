from datetime import datetime

from apps.base.tests.TestCaseWithData import TestCaseWithData

from apps.base.models.SemesterCourseMeetingItem import SemesterCourseMeetingItem
from django.utils import timezone

from django_celery_beat.models import CrontabSchedule, PeriodicTask

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

    def set_schedule_util(self, semester_course):
        days = list(SemesterCourseMeetingItem.objects.filter(semester_course=semester_course).values_list('day', flat=True))
        from_time: datetime = SemesterCourseMeetingItem.objects.filter(semester_course=semester_course)[0].from_time
        to_time: datetime = SemesterCourseMeetingItem.objects.filter(semester_course=semester_course)[0].to_time

        semester_course.set_schedule()

        self.assertTrue(
            CrontabSchedule.objects.filter(
                minute=from_time.minute,
                hour=from_time.hour,
                day_of_week=str(days)[1:-1],
                day_of_month='*'
            ).exists()
        )

        self.assertTrue(
            PeriodicTask.objects.filter(
                name=f'{semester_course.id}',
                task='tasks.record_video',
                kwargs = {
                    'file_path': f'{str(semester_course.course_section)}',
                    'id': self.recorder.id,
                    'stop_time': to_time,
                    'semester_course_id': semester_course.id
                },
                queue = self.recorder.queue_name
            ).exists()
        )

    def test_set_schedule(self):
       self.set_schedule_util(self.semester_course)