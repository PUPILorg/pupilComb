from datetime import datetime
from django.utils import timezone

from apps.base.tests.TestCaseWithData import TestCaseWithData
from apps.base.models.SemesterCourseMeetingItem import SemesterCourseMeetingItem

from django_celery_beat.models import CrontabSchedule, PeriodicTask

import json

from pupilComb.settings import temporary_timezone
import pytz

class SemesterCourseTestCase(TestCaseWithData):

    def set_schedule_util(self, semester_course):
        tz = pytz.timezone(temporary_timezone)

        days = list(SemesterCourseMeetingItem.objects.filter(semester_course=semester_course).values_list('day', flat=True))
        from_time: datetime = SemesterCourseMeetingItem.objects.filter(semester_course=semester_course)[0].from_time - timezone.timedelta(minutes=1)
        to_time: datetime = SemesterCourseMeetingItem.objects.filter(semester_course=semester_course)[0].to_time + timezone.timedelta(minutes=1)

        semester_course.set_schedule()

        from_time = from_time.astimezone(tz)
        to_time = to_time.astimezone(tz)

        duration = (to_time - from_time).total_seconds()

        self.assertTrue(
            CrontabSchedule.objects.filter(
                minute=from_time.minute,
                hour=from_time.hour,
                day_of_week=str(days)[1:-1],
                day_of_month='*',
                timezone=temporary_timezone
            ).exists()
        )

        self.assertTrue(
            PeriodicTask.objects.filter(
                name=f"{semester_course.id}-{semester_course}",
                task="apps.base.tasks.record_video",
                kwargs=json.dumps({
                    "file_folder": f"{self.semester.id}-{self.semester}/{semester_course.id}-{semester_course.course_section}/",
                    "pk": self.recorder.id,
                    "duration": duration,
                    "semester_course_id": semester_course.id
                }),
                enabled=True,
                queue=self.recorder.queue_name,
                expires=self.schedule.to_date
            ).exists()
        )

    def test_set_schedule(self):
       self.set_schedule_util(self.semester_course)