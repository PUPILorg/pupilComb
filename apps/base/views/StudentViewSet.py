from rest_framework.viewsets import ViewSet

from rest_framework.decorators import action

class StudentViewSet(ViewSet):

    @action(methods=['GET'], detail=False, url_path='courses')
    def courses(self, request):
        pass

