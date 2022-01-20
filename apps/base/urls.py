from django.urls import include, path

from rest_framework import routers

from .views.StudentViewSet import StudentViewSet

router = routers.DefaultRouter()
router.register(r'student', StudentViewSet, basename='StudentViewSet')

urlpatterns = [
    path('', include(router.urls))
]