from rest_framework.viewsets import ViewSet

import pandas as pd

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from apps.base.models.Room import Room
from apps.base.models.SemesterCourse import SemesterCourse

class ProfessorViewSet(ViewSet):

    @action(methods=['GET'], detail=False, url_path='available_rooms')
    def available_rooms(self, request):

        return_data = list(Room.objects.all().values_list('room_num', flat=True))

        return Response(data=return_data, status=HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path='courses')
    def courses(self, request):

        prof = request.user.professor
        df_sc = pd.DataFrame.from_records(SemesterCourse.objects.filter(professor=prof).values(
            'id',
            'course__identifier',
            'section_num',
            'semester_id',
            'semester__semester',
            'professor__user__first_name',
            'professor__user__last_name',
            'professor_id'
        ))
        
        rename_cols = {
            'course__identifier': 'course_name',
            'section_num': 'section_num',
            'semester_id': 'semester_id',
            'semester__semester': 'semester',
            'professor__user__first_name': 'professor_first_name',
            'professor__user__last_name': 'professor_last_name',
            'professor_id': 'professor_id'
        }
        
        rename_cols = {
            'course__identifier': 'course_name',
            'section_num': 'section_num',
            'semester_id': 'semester_id',
            'semester__semester': 'semester',
            'professor__user__first_name': 'professor_first_name',
            'professor__user__last_name': 'professor_last_name',
            'professor_id': 'professor_id'
        }

        df_sc.rename(columns=rename_cols, inplace=True)

        # function to merge the course_identifier and the section number
        def merger_ident_section_num(row):
            return f'{row["course_name"]} - {row["section_num"]}'

        df_sc['course_name'] = df_sc.apply(merger_ident_section_num, axis=1)


        response_list = []

        #splitting the semester courses into their respective semester for easier consumption on the frontend
        for sem in df_sc['semester'].unique():
            semester_dict = {}
            semester_dict['semester'] = sem
            semester_dict['courses'] = df_sc.loc[df_sc['semester'] == sem].to_dict(orient='records')
            semester_dict['id'] = semester_dict['courses'][0]['semester_id']

            response_list.append(semester_dict)

        return Response(data=response_list, status=HTTP_200_OK)