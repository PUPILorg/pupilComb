from django.db import models

from django_celery_beat.models import CrontabSchedule, PeriodicTask
from django.utils import timezone

from .SemesterCourseMeetingItem import SemesterCourseMeetingItem
from .Recorder import Recorder

import json

class SemesterCourse(models.Model):

    course_section = models.ForeignKey('base.CourseSection', on_delete=models.CASCADE)
    semester = models.ForeignKey('base.Semester', on_delete=models.SET_NULL, null=True)
    schedule = models.ForeignKey('base.Schedule', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{str(self.course_section)} - {self.semester}'

    def set_schedule(self) -> None:
        """
        sets up the Crontab (if none exists)
        and the periodic task that schedules the recording for this SemesterCourse
        :return:
        """
        scmi_queryset = SemesterCourseMeetingItem.objects.filter(semester_course=self)
        days : list[int] = list(scmi_queryset.values_list('day', flat=True))
        from_time = scmi_queryset[0].from_time - timezone.timedelta(minutes=1)
        to_time = scmi_queryset[0].to_time + timezone.timedelta(minutes=1)
        recorder = Recorder.objects.get(
            room_id=self.course_section.room_id
        )

        # TODO: This is not a good solution make sure to fix this before committing it

        from_time -= timezone.timedelta(hours=7)
        to_time -= timezone.timedelta(hours=7)

        duration = (to_time - from_time).total_seconds()

        crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
            minute = str(from_time.minute),
            hour = str(from_time.hour),
            day_of_week = str(days)[1:-1],
            timezone='America/Denver'
        )

        PeriodicTask.objects.get_or_create(
            crontab = crontab_schedule,
            name=f"{self.id}-{self}",
            task="apps.base.tasks.record_video",
            kwargs=json.dumps({
                "file_folder": f"{self.semester.id}-{self.semester}/{self.id}-{self.course_section}/",
                "pk": recorder.id,
                "duration": duration,
                "semester_course_id": self.id
            }),
            enabled=True,
            queue=recorder.queue_name,
            expires=self.schedule.to_date
        )