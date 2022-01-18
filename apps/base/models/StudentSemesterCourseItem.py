from django.db import models

class StudentSemesterCourseItem(models.Model):

    student = models.ForeignKey('base.Student', on_delete=models.CASCADE)
    semester_course = models.ForeignKey('base.SemesterCourse', on_delete=models.CASCADE)

