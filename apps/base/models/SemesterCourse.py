from django.db import models
from .SemesterCourseMeetingItem import SemesterCourseMeetingItem
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from .Recorder import Recorder

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
        from_time = scmi_queryset[0].from_time
        to_time = scmi_queryset[0].to_time
        recorder = Recorder.objects.get(
            room_id=self.course_section.room_id
        )

        crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
            minute = str(from_time.minute),
            hour = str(from_time.hour),
            day_of_week = str(days)[1:-1]
        )

        PeriodicTask.objects.get_or_create(
            crontab = crontab_schedule,
            name=f'{self.id}',
            task='tasks.record_video',
            kwargs={
                'file_path': f'{str(self.course_section)}',
                'id': recorder.id,
                'stop_time': to_time,
                'semester_course_id': self.id
            },
            queue=recorder.queue_name
        )