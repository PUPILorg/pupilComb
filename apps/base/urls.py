from django.urls import include, path

from rest_framework.authtoken import views
from rest_framework import routers

from .views.StudentViewSet import StudentViewSet
from .views.ProfessorViewSet import ProfessorViewSet
from .views.SemesterCourseViewSet import SemesterCourseViewSet

router = routers.DefaultRouter()
router.register(r'student', StudentViewSet, basename='StudentViewSet')
router.register(r'professor', ProfessorViewSet, basename='ProfessorViewSet')
router.register(r'semester_course', SemesterCourseViewSet, basename='SemesterCourseViewSet')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token)
]