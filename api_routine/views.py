from rest_framework.viewsets import ModelViewSet

from api_routine.models import Routine
from api_routine.serializers import RoutineUpdateSerializer, RoutinesSerializer


class RoutinesViewsets(ModelViewSet):
    response_data = None
    response_message = None

    def get_queryset(self):
        return Routine.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return RoutinesSerializer
        if self.action == "create":
            return RoutineUpdateSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        self.response_data = response.data
        self.response_message = {
            "msg": "Routine lookup was successful.",
            "status": "ROUTINE_LIST_OK"
        }
        response.data = self.get_response_model()
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        self.response_data = {
            "routine_id": response.data["routine_id"]
        }
        self.response_message = {
            "msg": "You have successfully created the routine.",
            "status": "ROUTINE_CREATE_OK"
        }
        response.data = self.get_response_model()
        return response

    def get_response_model(self):
        return {
            "data": self.response_data,
            "message": self.response_message
        }
