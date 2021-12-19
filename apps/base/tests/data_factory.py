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

    camera_path = '/dev/video0'
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

class MediaFactory(DjangoModelFactory):
    class Meta:
        model = 'base.Media'

    file = factory.Faker('file_path', category='video')

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


class CourseItemsFactory(DjangoModelFactory):
    class Meta:
        model = 'base.CourseItems'

    semester_course = factory.SubFactory(SemesterCourseFactory)
    date = factory.LazyFunction(timezone.now().date)
    media = factory.SubFactory(MediaFactory)

class SemesterCourseMeetingItemFactory(DjangoModelFactory):
    class Meta:
        model = 'base.SemesterCourseMeetingItem'

    @staticmethod
    def time_plus_one_hour():
        return  timezone.now() + timezone.timedelta(hours=1)

    semester_course = factory.SubFactory(SemesterCourseFactory)
    day = 1

    from_time = factory.LazyFunction(timezone.now)
    to_time = factory.LazyFunction(time_plus_one_hour)
