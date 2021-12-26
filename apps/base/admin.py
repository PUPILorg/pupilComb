from django.contrib import admin

from .models.Room import Room
from .models.Recorder import Recorder
from .models.SemesterCourseMeetingItem import SemesterCourseMeetingItem
from .models.SemesterCourse import SemesterCourse
from .models.CourseSection import CourseSection
from .models.Course import Course
from .models.Schedule import Schedule
from .models.Media import Media
from .models.CourseItems import CourseItems
from .models.Semester import Semester
from .models.Input import Input

class AllFieldsAdmin(admin.ModelAdmin):
    """
    parent class that shows all fields in the list display
    """
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        self.list_display.insert(0, '__str__')
        super(AllFieldsAdmin, self).__init__(model, admin_site)

#inline models
class CourseItemInline(admin.TabularInline):
    model = CourseItems

class SemesterCourseMeetingItemInline(admin.TabularInline):
    model = SemesterCourseMeetingItem

class CourseSectionInline(admin.TabularInline):
    model = CourseSection

class InputsInLine(admin.TabularInline):
    model = Input

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
    inlines =  (SemesterCourseMeetingItemInline, CourseItemInline)

@admin.register(Course)
class CourseAdmin(AllFieldsAdmin):
    inlines = (CourseSectionInline, )

@admin.register(Schedule)
class ScheduleAdmin(AllFieldsAdmin):
    pass

@admin.register(Media)
class MediaAdmin(AllFieldsAdmin):
    pass

@admin.register(Semester)
class SemesterAdmin(AllFieldsAdmin):

    actions = ['set_schedule',]

    def set_schedule(self, request, queryset: Semester):
        for query in queryset:
            query.set_up_schedule_semester()
