from rest_framework.test import APIRequestFactory, force_authenticate

from apps.base.models.Room import Room
from apps.base.tests.TestCaseWithData import TestCaseWithData
from apps.base.views.ProfessorViewSet import ProfessorViewSet


class ProfessorViewSetTest(TestCaseWithData):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_available_rooms(self):
        request = self.factory.get('API/Professor/available_rooms')
        force_authenticate(request, self.professor.user)
        view = ProfessorViewSet.as_view({'get': 'available_rooms'})

        expected = list(Room.objects.all().values_list('room_num', flat=True))

        response = view(request)

        self.assertEqual(expected, response.data)
        self.assertEqual(200, response.status_code)

    def test_available_rooms_unauth(self):
        request = self.factory.get('API/Professor/available_rooms')
        view = ProfessorViewSet.as_view({'get': 'available_rooms'})

        response = view(request)

        self.assertEqual(401, response.status_code)

    def test_available_rooms_no_student(self):
        request = self.factory.get('API/Professor/available_rooms')
        force_authenticate(request, self.student.user)
        view = ProfessorViewSet.as_view({'get': 'available_rooms'})

        expected = list(Room.objects.all().values_list('room_num', flat=True))

        response = view(request)

        self.assertEqual(403, response.status_code)

    def test_courses_unauth(self):
        request = self.factory.get('API/Professor/courses')
        view = ProfessorViewSet.as_view({'get': 'courses'})

        response = view(request)

        self.assertEqual(401, response.status_code)

    def test_courses_no_student(self):
        request = self.factory.get('API/Professor/courses')
        view = ProfessorViewSet.as_view({'get': 'courses'})
        force_authenticate(request, self.student.user)

        response = view(request)

        self.assertEqual(403, response.status_code)

    def test_courses(self):
        request = self.factory.get('API/Professor/courses')
        force_authenticate(request, self.professor.user)

        view = ProfessorViewSet.as_view({'get': 'courses'})

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

        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected, response.data)
