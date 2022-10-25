from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from api_routine.serializers import RoutineUpdateSerializer


class RoutinesViewsets(ModelViewSet):

    def get_serializer_class(self):
        if self.action == "create":
            return RoutineUpdateSerializer