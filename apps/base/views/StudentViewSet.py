from rest_framework.viewsets import ViewSet

import pandas as pd

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from apps.base.models.StudentSemesterCourseItem import StudentSemesterCourseItem

class StudentViewSet(ViewSet):

    @action(methods=['GET'], detail=False, url_path='courses')
    def courses(self, request):
        student = request.user.student

        ssci = pd.DataFrame.from_records(StudentSemesterCourseItem.objects.filter(student=student).values(
            'id',
            'semester_course__course__identifier',
            'semester_course__section_num',
            'semester_course__semester__semester',
            'semester_course__professor__user__first_name',
            'semester_course__professor__user__last_name',
            'semester_course__professor_id'
        ))

        rename_cols = {
            'semester_course__course__identifier': 'course_identifier',
            'semester_course__section_num': 'section_num',
            'semester_course__semester__semester': 'semester',
            'semester_course__professor__user__first_name': 'professor_first_name',
            'semester_course__professor__user__last_name': 'professor_last_name',
            'semester_course__professor_id': 'professor_id'
        }

        ssci.rename(columns=rename_cols, inplace=True)

        response_dict = {}

        for sem in ssci['semester'].unique():
            response_dict[sem] = ssci.loc[ssci['semester'] == sem].to_dict(orient='records')

        return Response(data=response_dict, status=HTTP_200_OK)
