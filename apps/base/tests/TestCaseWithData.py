from django.test import TestCase

import apps.base.tests.data_factory as data_factory

class TestCaseWithData(TestCase):
    """
    Extension of the default django TestCase that sets up data in the DB that can be used for all the server_tests
    that inherit it

    any reference to today gets evaluated to the day the test is run

    models that are set up:
        - Semester (F21)
        - Schedule (today -> 10 days + today)
        - Room (random room num)
        - Recorder (room from above, default camera path (/dev/video0))
        - Course (random identifier of length 9)
        - CourseSection (with above course, random section num, above room)
        - SemesterCourse (above courseSection, above Semester, above Schedule)
        - Media (random video file)
        - CourseItem (above semesterCourse, above media, today's date)
        - SemesterCourseMeetingItem (above SemesterCourse, day, from_time, to_time) there will be a MWF one of these
    """

    @classmethod
    def setUpTestData(cls):
        cls.semester = data_factory.SemesterFactory()
        cls.schedule = data_factory.ScheduleFactory()
        cls.room = data_factory.RoomFactory()
        cls.recorder = data_factory.RecorderFactory(
            room = cls.room
        )
        cls.course = data_factory.CourseFactory()
        cls.course_section = data_factory.CourseSectionFactory(
            course = cls.course,
            room = cls.room
        )
        cls.semester_course = data_factory.SemesterCourseFactory(
            semester = cls.semester,
            course_section = cls.course_section,
            schedule = cls.schedule
        )
        cls.media = data_factory.MediaFactory()
        cls.course_item = data_factory.CourseItemsFactory(
            semester_course = cls.semester_course,
            media = cls.media
        )
        cls.semester_course_meeting_M = data_factory.SemesterCourseMeetingItemFactory(
            day = 1,
            semester_course = cls.semester_course
        )
        cls.semester_course_meeting_W = data_factory.SemesterCourseMeetingItemFactory(
            day = 3,
            semester_course = cls.semester_course
        )
        cls.semester_course_meeting_F = data_factory.SemesterCourseMeetingItemFactory(
            day = 5,
            semester_course = cls.semester_course
        )