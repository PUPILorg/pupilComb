from django.db import models
from .SemesterCourseMeetingItem import SemesterCourseMeetingItem
from django_celery_beat.models import CrontabSchedule, PeriodicTask

class SemesterCourse(models.Model):

    course_section = models.ForeignKey('base.CourseSection', on_delete=models.CASCADE)
    semester = models.ForeignKey('base.Semester', on_delete=models.SET_NULL, null=True)
    schedule = models.ForeignKey('base.Schedule', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{str(self.course_section)} - {self.semester}'

    def set_schedule(self):
        """
        #TODO: this is not done yet
        :return:
        """
        for schedule_item in  SemesterCourseMeetingItem.objects.filter(semester_class=self):
            chron_schedule, _ = CrontabSchedule.object.get_or_create(
                minute=schedule_item.from_time.minute,
                hour=schedule_item.from_time.hour,
                day_of_week = schedule_item.day,
                day_of_month = '*'
            )