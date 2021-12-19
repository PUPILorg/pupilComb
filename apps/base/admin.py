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

#inline models
class CourseItemInline(admin.TabularInline):
    model = CourseItems

class SemesterCourseMeetingItemInline(admin.TabularInline):
    model = SemesterCourseMeetingItem

class CourseSectionInline(admin.TabularInline):
    model = CourseSection

# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass

@admin.register(Recorder)
class RaspberryPiAdmin(admin.ModelAdmin):
    readonly_fields = ('queue_name',)

@admin.register(SemesterCourse)
class SemesterCourseAdmin(admin.ModelAdmin):
    inlines =  (SemesterCourseMeetingItemInline, CourseItemInline)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = (CourseSectionInline, )

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    pass

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):

    actions = ['set_schedule',]

    def set_schedule(self, request, queryset: Semester):
        for query in queryset:
            query.set_up_schedule()
