from apps.base.tests.TestCaseWithData import TestCaseWithData

from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.status import HTTP_200_OK

from apps.base.views.SemesterCourseViewSet import SemesterCourseViewSet

import pandas as pd


class SemesterCourseViewSetTest(TestCaseWithData):

    maxDiff = None

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_get(self):
        request = self.factory.get(f'API/semester_course/{self.semester_course.id}')
        force_authenticate(request, self.professor.user)

        view = SemesterCourseViewSet.as_view({'get': 'get'})

        response = view(request, self.semester_course.id)

        expected = {
            'id': self.semester_course.id,
            'course_identifier': self.course.identifier,
            'section_num': self.semester_course.section_num,
            'description': self.course.description,
            'room': str(self.semester_course.room.room_num),
            'schedule_from_date': self.schedule.from_date,
            'schedule_to_date': self.schedule.to_date,
            'camera': self.semester_course.camera,
            'projector': self.semester_course.projector,
            'auto_publish': self.semester_course.auto_publish
        }

        meetings = pd.Series([pd.DataFrame([
            {
                'day': 1,
                'from_time': self.semester_course_meeting_M.from_time.time().strftime('%H:%M'),
                'to_time': self.semester_course_meeting_M.to_time.time().strftime('%H:%M')
            },
            {
                'day': 3,
                'from_time': self.semester_course_meeting_W.from_time.time().strftime('%H:%M'),
                'to_time': self.semester_course_meeting_W.to_time.time().strftime('%H:%M')
            },
            {
                'day': 5,
                'from_time': self.semester_course_meeting_F.from_time.time().strftime('%H:%M'),
                'to_time': self.semester_course_meeting_M.to_time.time().strftime('%H:%M')
            }
        ]).to_dict(orient='records')])

        expected_df = pd.DataFrame(expected, index=[0])
        expected_df['meetings'] = meetings


        print(expected_df.to_json(orient='records'))
        print(response.data)

        self.assertEqual(response.data, expected_df.to_json(orient='records'))
        self.assertEqual(response.status_code, HTTP_200_OK)
