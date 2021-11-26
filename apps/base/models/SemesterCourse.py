from django.db import models

class SemesterCourse(models.Model):

    course = models.ForeignKey('base.Course', on_delete=models.CASCADE)
    semester = models.ForeignKey('base.Semester', on_delete=models.SET_NULL, null=True)
    schedule = models.ForeignKey('base.Schedule', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{str(self.course)} - {self.semester}'