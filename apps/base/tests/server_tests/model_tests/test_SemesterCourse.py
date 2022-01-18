from datetime import datetime

import django.db.utils
from django.utils import timezone

from apps.base.tests.TestCaseWithData import TestCaseWithData
from apps.base.models.SemesterCourseMeetingItem import SemesterCourseMeetingItem
from apps.base.models.SemesterCourse import SemesterCourse
from apps.base.models.Semester import Semester

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
                    "file_folder": f"{self.semester}/{semester_course.id}/",
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

    def test_unique_to_course_and_semester_raise(self):
       with self.assertRaises(django.db.utils.IntegrityError):
           SemesterCourse.objects.create(
               course=self.course,
               section_num=self.semester_course.section_num,
               room = self.room,
               semester=self.semester,
               schedule=self.schedule
           )

    def test_unique_to_course_and_semester_passes(self):
        s = Semester.objects.create(
            semester='F21'
        )

        try:
            SemesterCourse.objects.create(
                course=self.course,
                section_num=self.semester_course.section_num,
                room=self.room,
                semester=s,
                schedule=self.schedule
            )
        except django.db.utils.IntegrityError:
            self.fail('the semestercourse was not created')