from apps.base.tests.TestCaseWithData import TestCaseWithData

from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.utils import timezone

from apps.base.models.SemesterCourseMeetingItem import SemesterCourseMeetingItem
from apps.base.models.SemesterCourse import SemesterCourse

import datetime

import apps.base.tests.data_factory as data_factory

import json
import pytz
from pupilComb.settings import temporary_timezone


class SemesterTestCase(TestCaseWithData):

    def set_schedule_utils(self, semester_course):
        tz = pytz.timezone(temporary_timezone)
        days = list(
            SemesterCourseMeetingItem.objects.filter(semester_course=semester_course).values_list('day', flat=True))
        from_time: datetime = SemesterCourseMeetingItem.objects.filter(semester_course=semester_course)[0].from_time \
                              - timezone.timedelta(minutes=1)
        to_time: datetime = SemesterCourseMeetingItem.objects.filter(semester_course=semester_course)[0].to_time \
                            + timezone.timedelta(minutes=1)

        duration = (to_time - from_time).total_seconds()

        from_time = from_time.astimezone(tz)
        to_time = to_time.astimezone(tz)

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


def test_set_schedule_semester(self):
    course_section = data_factory.CourseSectionFactory(
        room=self.room
    )

    semester_course = data_factory.SemesterCourseFactory(
        semester=self.semester,
        schedule=self.schedule,
        course_section=course_section
    )

    data_factory.SemesterCourseMeetingItemFactory(
        day=1,
        semester_course=semester_course
    )
    data_factory.SemesterCourseMeetingItemFactory(
        day=3,
        semester_course=semester_course
    )
    data_factory.SemesterCourseMeetingItemFactory(
        day=5,
        semester_course=semester_course
    )

    self.semester.set_up_schedule_semester()

    for semester_course in SemesterCourse.objects.filter(semester=self.semester):
        self.set_schedule_utils(semester_course)
