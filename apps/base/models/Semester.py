from django.db import models

from .SemesterCourse import SemesterCourse

class Semester(models.Model):

    FALL_21 = 'F21'
    SPRING_22 = 'S22'

    SEMESTER_CHOICES = [
        (FALL_21, 'Fall 21'),
        (SPRING_22, 'Spring 22')
    ]

    semester = models.CharField(max_length=3, choices=SEMESTER_CHOICES, default=FALL_21, unique=True)

    def __str__(self) -> str:
        return f'{self.semester}'

    def set_up_schedule_semester(self) -> None:
        """
        sets up the schedule for all semesterCourses associated with this semester
        :return: None
        """
        for semester_course in SemesterCourse.objects.filter(semester=self):
            semester_course.set_schedule()
