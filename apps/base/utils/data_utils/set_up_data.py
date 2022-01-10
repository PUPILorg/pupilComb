import apps.base.tests.data_factory as data_factory

from apps.base.utils.recording.enums import Codec, VideoContainer


def set_up_data():
    '''
    run this from the python console
    :return:
    '''
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
    semester_course_recording_item = data_factory.SemesterCourseRecordingItemFactory(
        semester_course=semester_course
    )
    media = data_factory.MediaFactory(
        semester_course_recording_item=semester_course_recording_item
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
    camera_input = data_factory.InputFactory(
        recorder=recorder,
        path_to_input='/dev/video2',
        codec=Codec.CODEC_H264,
        file_container=VideoContainer.MP4,
        type_device = 0
    )
    video_capture_input = data_factory.InputFactory(
        recorder=recorder,
        path_to_input='/dev/video0',
        codec=Codec.CODEC_MJPEG,
        file_container=VideoContainer.MOV,
        type_device = 1
    )
