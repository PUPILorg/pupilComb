from apps.base.tests.TestCaseWithData import TestCaseWithData

from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

class StudentViewSetTest(TestCaseWithData):

    def setUp(self) -> None:
        self.client = APIClient()
        self.client_auth = APIClient()
        token = Token.objects.create(user=self.student.user)
        self.client_auth.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_student_courses_non_authenticated(self):
        response = self.client.get('/API/student/courses')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_student_courses(self):
        pass
