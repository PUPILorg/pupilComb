import django.db.utils

from apps.base.tests.TestCaseWithData import TestCaseWithData

from apps.base.models.StudentSemesterCourseItem import StudentSemesterCourseItem

class StudentSemesterCourseItemTest(TestCaseWithData):

    def test_unique_together(self):
        with self.assertRaises(django.db.utils.IntegrityError):
            # a student cannot be registered to the same semesterClass twice
            StudentSemesterCourseItem.objects.create(
                student=self.student,
                semester_course=self.semester_course
            )
