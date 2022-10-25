from rest_framework.viewsets import ModelViewSet

from api_routine.serializers import RoutineUpdateSerializer


class RoutinesViewsets(ModelViewSet):

    def get_serializer_class(self):
        if self.action == "create":
            return RoutineUpdateSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response_model = {
            "data": {
                "routine_id": response.data["routine_id"]
            },
            "message": {
                "msg": "You have successfully created the routine.",
                "status": "ROUTINE_CREATE_OK"
            }
        }
        response.data = response_model
        return response
