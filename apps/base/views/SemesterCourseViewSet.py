from rest_framework.viewsets import ViewSet

import pandas as pd

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from apps.base.models.SemesterCourse import SemesterCourse
from apps.base.models.SemesterCourseMeetingItem import SemesterCourseMeetingItem


class SemesterCourseViewSet(ViewSet):

    @action(methods=['GET'], detail=False, url_path='(?P<pk>[0-9]+)')
    def get(self, request, pk):
        df_semester_course = pd.DataFrame.from_records(SemesterCourse.objects.filter(id=pk).values(
            'id',
            'course__identifier',
            'course__description',
            'section_num',
            'room__room_num',
            'camera',
            'projector',
            'auto_publish',
            'schedule__from_date',
            'schedule__to_date'
        ))

        df_semester_course_meeting_item = pd.DataFrame.from_records(
            SemesterCourseMeetingItem.objects.filter(semester_course_id=pk).values(
                'day',
                'from_time',
                'to_time'
            ))

        if not df_semester_course_meeting_item.empty:
            df_semester_course_meeting_item['from_time'] = df_semester_course_meeting_item['from_time'].map(
                lambda x: x.time().strftime('%H:%M'))

            df_semester_course_meeting_item['to_time'] = df_semester_course_meeting_item['to_time'].map(
                lambda x: x.time().strftime('%H:%M'))

        df_semester_course['meetings'] = pd.Series([df_semester_course_meeting_item.to_dict(orient='records')])

        rename_dict = {
            'course__identifier': 'course_identifier',
            'room__room_num': 'room',
            'schedule__from_date': 'schedule_from_date',
            'schedule__to_date': 'schedule_to_date',
            'course__description': 'description'
        }

        df_semester_course.rename(columns=rename_dict, inplace=True)

        return Response(data=df_semester_course.to_json(orient='records'), status=HTTP_200_OK)
