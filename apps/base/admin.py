from django.contrib import admin

from .models.Room import Room
from .models.RaspberryPi import RaspberryPi
from .models.ScheduleItems import ScheduleItems
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

class ScheduleItemsInline(admin.TabularInline):
    model = ScheduleItems

class CourseSectionInline(admin.TabularInline):
    model = CourseSection

# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass

@admin.register(RaspberryPi)
class RaspberryPiAdmin(admin.ModelAdmin):
    pass

@admin.register(SemesterCourse)
class SemesterCourseAdmin(admin.ModelAdmin):
    pass

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = (CourseSectionInline, )

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    inlines = (ScheduleItemsInline, )

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    pass

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):

    actions = ['set_schedule',]

    def set_schedule(self, request, queryset: Semester):
        for query in queryset:
            query.set_up_schedule()