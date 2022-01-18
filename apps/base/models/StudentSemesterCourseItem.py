from django.db import models

class StudentSemesterCourseItem(models.Model):

    student = models.ForeignKey('base.Student', on_delete=models.CASCADE)
    semester_course = models.ForeignKey('base.SemesterCourse', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'semester_course')