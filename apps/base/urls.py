from django.urls import include, path

from rest_framework.authtoken import views
from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from .views.StudentViewSet import StudentViewSet
from .views.ProfessorViewSet import ProfessorViewSet
from .views.SemesterCourseViewSet import SemesterCourseViewSet

router = routers.DefaultRouter()
router.register(r'student', StudentViewSet, basename='StudentViewSet')
router.register(r'professor', ProfessorViewSet, basename='ProfessorViewSet')
router.register(r'semester_course', SemesterCourseViewSet, basename='SemesterCourseViewSet')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh')
]