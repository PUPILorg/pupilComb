from factory.django import DjangoModelFactory
import factory.fuzzy

from django.utils import timezone


class RoomFactory(DjangoModelFactory):
    class Meta:
        model = 'base.Room'

    room_num = factory.Faker('pyint', min_value=0, max_value=1000)

class RecorderFactory(DjangoModelFactory):
    class Meta:
        model = 'base.Recorder'

    is_active = True
    room = factory.SubFactory(RoomFactory)

class CourseFactory(DjangoModelFactory):
    class Meta:
        model = 'base.Course'

    identifier = factory.fuzzy.FuzzyText(length=9)

class CourseSectionFactory(DjangoModelFactory):
    class Meta:
        model = 'base.CourseSection'

    course = factory.SubFactory(CourseFactory)
    section_num = factory.Faker('pyint', min_value=0, max_value=999)
    room = factory.SubFactory(RoomFactory)

class SemesterFactory(DjangoModelFactory):
    class Meta:
        model = 'base.Semester'

    semester = 'F21'

class ScheduleFactory(DjangoModelFactory):
    """
    sets up a Schedule instance with today's date for from_date and 10 days later for
    to_date
    """

    class Meta:
        model = 'base.Schedule'

    @staticmethod
    def set_date_10_days_later():
        return timezone.now().date() + timezone.timedelta(days=10)

    from_date = factory.LazyFunction(timezone.now().date)
    to_date = factory.LazyFunction(set_date_10_days_later)


class SemesterCourseFactory(DjangoModelFactory):
    class Meta:
        model = 'base.SemesterCourse'

    course_section = factory.SubFactory(CourseSectionFactory)
    semester = factory.SubFactory(SemesterFactory)
    schedule = factory.SubFactory(ScheduleFactory)


class SemesterCourseRecordingItem(DjangoModelFactory):
    class Meta:
        model = 'base.SemesterCourseRecordingItem'

    semester_course = factory.SubFactory(SemesterCourseFactory)
    date = factory.LazyFunction(timezone.now().date)

class SemesterCourseMeetingItemFactory(DjangoModelFactory):
    """
    make sure to set the day when instantiating the semester course
    """
    class Meta:
        model = 'base.SemesterCourseMeetingItem'

    @staticmethod
    def time_plus_one_hour():
        return  timezone.now() + timezone.timedelta(hours=1)

    semester_course = factory.SubFactory(SemesterCourseFactory)
    day = 1

    from_time = factory.LazyFunction(timezone.now)
    to_time = factory.LazyFunction(time_plus_one_hour)

class InputFactory(DjangoModelFactory):
    """
    make sure to set the path_for_input when creating the InputFactory
    """
    class Meta:
        model = 'base.Input'

    recorder = factory.SubFactory(RecorderFactory)
    path_to_input = factory.fuzzy.FuzzyText('/dev/video0')

    codec = factory.fuzzy.FuzzyChoice('h264')
    file_container = factory.fuzzy.FuzzyChoice('mp4')
    type_device = factory.Faker('pyint', min_value=0, max_value=1)

class MediaFactory(DjangoModelFactory):
    class Meta:
        model = 'base.Media'

    semester_course_recording_item = factory.SubFactory(SemesterCourseRecordingItem)
    file = factory.Faker('file_path', category='video')
    uploaded = False