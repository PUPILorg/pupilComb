from django.db import models
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from .SemesterCourse import SemesterCourse
from .SemesterCourseMeetingItem import SemesterCourseMeetingItem
from .Recorder import Recorder

class Semester(models.Model):

    FALL_21 = 'F21'
    SPRING_22 = 'S22'

    SEMESTER_CHOICES = [
        (FALL_21, 'Fall 21'),
        (SPRING_22, 'Spring 22')
    ]

    semester = models.CharField(max_length=3, choices=SEMESTER_CHOICES, default=FALL_21, unique=True)

    def __str__(self):
        return f'{self.semester}'

    def set_up_schedule(self):
        """
        sets up the crontab schedule for the recordings
        :return:
        """
        for semester_class in SemesterCourse.objects.filter(semester_id=self.id):
            for schedule_item in SemesterCourseMeetingItem.objects.filter(schedule_id=semester_class.schedule_id):
                schedule, _ = CrontabSchedule.objects.get_or_create(
                    minute=schedule_item.from_time.minute,
                    hour=schedule_item.from_time.hour,
                    day_of_week=schedule_item.day,
                    day_of_month='*'
                )

                room_recorder = Recorder.objects.get(room_id=semester_class.course.room_id)

                PeriodicTask.objects.get_or_create(
                    crontab = schedule,
                    name = f'{str(semester_class.course)} - {schedule_item.day}',
                    task = 'tasks.record_video',
                    kwargs = {
                        'file_path': f'{str(semester_class.course)}',
                        'id': room_recorder.id,
                        'stop_time': schedule_item.to_time,
                        'course_id': semester_class.id
                    },
                    queue = room_recorder.queue_name
                )
