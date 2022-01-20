from django.contrib import admin

from .models.Room import Room
from .models.Recorder import Recorder
from .models.SemesterCourseMeetingItem import SemesterCourseMeetingItem
from .models.SemesterCourse import SemesterCourse
from .models.Course import Course
from .models.Schedule import Schedule
from .models.Media import Media
from .models.SemesterCourseRecordingItem import SemesterCourseRecordingItem
from .models.Semester import Semester
from .models.Input import Input
from .models.StudentSemesterCourseItem import StudentSemesterCourseItem
from .models.Student import Student
from .models.Professor import Professor

class AllFieldsAdmin(admin.ModelAdmin):
    """
    parent class that shows all fields in the list display
    """
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        self.list_display.insert(0, '__str__')
        super(AllFieldsAdmin, self).__init__(model, admin_site)

#inline models
class SemesterCourseRecordingItemInLine(admin.TabularInline):
    model = SemesterCourseRecordingItem


class SemesterCourseMeetingItemInline(admin.TabularInline):
    model = SemesterCourseMeetingItem

class SemesterCourseSectionInline(admin.TabularInline):
    model = SemesterCourse

class InputsInLine(admin.TabularInline):
    model = Input

class MediaInLine(admin.TabularInline):
    model = Media

class StudentSemesterCourseItemInline(admin.TabularInline):
    model = StudentSemesterCourseItem

# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass

@admin.register(Recorder)
class RecorderAdmin(AllFieldsAdmin):
    readonly_fields = ('queue_name',)
    inlines = [InputsInLine, ]

@admin.register(SemesterCourse)
class SemesterCourseAdmin(AllFieldsAdmin):
    inlines =  (SemesterCourseMeetingItemInline, SemesterCourseRecordingItemInLine)

@admin.register(SemesterCourseRecordingItem)
class SemesterCourseRecordingAdmin(AllFieldsAdmin):
    inlines = (MediaInLine, )

@admin.register(Course)
class CourseAdmin(AllFieldsAdmin):
    inlines = (SemesterCourseSectionInline, )

@admin.register(Schedule)
class ScheduleAdmin(AllFieldsAdmin):
    pass

@admin.register(Semester)
class SemesterAdmin(AllFieldsAdmin):

    actions = ['set_schedule',]

    def set_schedule(self, request, queryset: Semester):
        for query in queryset:
            query.set_up_schedule_semester()

@admin.register(Professor)
class ProfessorAdmin(AllFieldsAdmin):
    pass

@admin.register(Student)
class StudentAdmin(AllFieldsAdmin):
    inlines = (StudentSemesterCourseItemInline, )
