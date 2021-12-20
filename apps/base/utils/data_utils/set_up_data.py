import apps.base.tests.data_factory as data_factory

if __name__ == "__main__":
    semester = data_factory.SemesterFactory()
    schedule = data_factory.ScheduleFactory()
    room = data_factory.RoomFactory()
    recorder = data_factory.RecorderFactory(
        room=room
    )
    course = data_factory.CourseFactory()
    course_section = data_factory.CourseSectionFactory(
        course=course,
        room=room
    )
    semester_course = data_factory.SemesterCourseFactory(
        semester=semester,
        course_section=course_section,
        schedule=schedule
    )
    media = data_factory.MediaFactory()
    course_item = data_factory.CourseItemsFactory(
        semester_course=semester_course,
        media=media
    )
    semester_course_meeting_M = data_factory.SemesterCourseMeetingItemFactory(
        day=1,
        semester_course=semester_course
    )
    semester_course_meeting_W = data_factory.SemesterCourseMeetingItemFactory(
        day=3,
        semester_course=semester_course
    )
    semester_course_meeting_F = data_factory.SemesterCourseMeetingItemFactory(
        day=5,
        semester_course=semester_course
    )
