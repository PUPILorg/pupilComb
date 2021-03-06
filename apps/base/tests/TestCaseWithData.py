from django.test import TestCase

import apps.base.tests.data_factory as data_factory
from apps.base.utils.recording.enums import Codec, VideoContainer


class TestCaseWithData(TestCase):
    """
    Extension of the default django TestCase that sets up data in the DB that can be used for all the server_tests
    that inherit it

    any reference to today gets evaluated to the day the test is run

    ## TODO: update these models ##

    models that are set up:
        - Semester (F21)
        - Schedule (today -> 10 days + today)
        - Room (random room num)
        - Recorder (room from above, default camera path (/dev/video0))
        - Course (random identifier of length 9)
        - SemesterCourse (above course, above Semester, above Schedule)
        - Media (random video file)
        - CourseItem (above semesterCourse, above media, today's date)
        - SemesterCourseMeetingItem (above SemesterCourse, day, from_time, to_time) there will be a MWF one of these
    """

    @classmethod
    def setUpTestData(cls):
        cls.professor = data_factory.ProfessorFactory()
        cls.semester = data_factory.SemesterFactory()
        cls.schedule = data_factory.ScheduleFactory()
        cls.room = data_factory.RoomFactory()
        cls.recorder = data_factory.RecorderFactory(
            room=cls.room
        )
        cls.course = data_factory.CourseFactory()
        cls.semester_course = data_factory.SemesterCourseFactory(
            course = cls.course,
            room = cls.room,
            semester=cls.semester,
            schedule=cls.schedule,
            professor = cls.professor
        )
        cls.semester_course_recording_item = data_factory.SemesterCourseRecordingItemFactory(
            semester_course=cls.semester_course,
        )
        cls.media = data_factory.MediaFactory(
            semester_course_recording_item=cls.semester_course_recording_item,
            uploaded = False
        )
        cls.semester_course_meeting_M = data_factory.SemesterCourseMeetingItemFactory(
            day=1,
            semester_course=cls.semester_course
        )
        cls.semester_course_meeting_W = data_factory.SemesterCourseMeetingItemFactory(
            day=3,
            semester_course=cls.semester_course
        )
        cls.semester_course_meeting_F = data_factory.SemesterCourseMeetingItemFactory(
            day=5,
            semester_course=cls.semester_course
        )
        cls.camera_input = data_factory.InputFactory(
            recorder=cls.recorder,
            path_to_input='/dev/video2',
            codec=Codec.CODEC_H264,
            file_container=VideoContainer.MP4
        )
        cls.video_capture_input = data_factory.InputFactory(
            recorder=cls.recorder,
            path_to_input='/dev/video0',
            codec=Codec.CODEC_MJPEG,
            file_container=VideoContainer.MOV
        )
        cls.student = data_factory.StudentFactory()
        cls.student_semester_course_item = data_factory.StudentSemesterCourseItemFactory(
            student = cls.student,
            semester_course = cls.semester_course
        )