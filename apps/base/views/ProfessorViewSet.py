from rest_framework.viewsets import ViewSet

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from apps.base.models.Room import Room

class ProfessorViewSet(ViewSet):

    @action(methods=['GET'], detail=False, url_path='available_rooms')
    def available_rooms(self, request):

        return_data = list(Room.objects.all().values_list('room_num', flat=True))

        return Response(data=return_data, status=HTTP_200_OK)