from apps.base.tests.TestCaseWithData import TestCaseWithData

from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED, HTTP_200_OK
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.base.views.StudentViewSet import StudentViewSet

class StudentViewSetTest(TestCaseWithData):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_student_courses_non_authenticated(self):
        request = self.factory.get('/API/student/courses')
        view = StudentViewSet.as_view({'get': 'courses'})
        response = view(request)

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_student_courses_no_prof(self):
        request = self.factory.get('API/student/courses')
        force_authenticate(request, self.professor.user)
        view = StudentViewSet.as_view({'get': 'courses'})
        response = view(request)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_student_courses(self):
        request = self.factory.get('API/student/courses')
        force_authenticate(request, self.student.user)
        view = StudentViewSet.as_view({'get': 'courses'})
        response = view(request)

        expected = [{
            'semester': self.semester.semester,
            'id': self.semester.id,
            'courses': [
                {
                    'id': self.semester_course.id,
                    'course_name': f'{self.course.identifier} - {self.semester_course.section_num}',
                    'section_num': self.semester_course.section_num,
                    'professor_first_name': self.professor.user.first_name,
                    'semester': self.semester.semester,
                    'semester_id': self.semester.id,
                    'professor_last_name': self.professor.user.last_name,
                    'professor_id': self.professor.id
                }]
        }]

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, expected)