from datetime import timedelta, datetime

from django.db.models import Q
from rest_framework.generics import UpdateAPIView
from rest_framework.viewsets import ModelViewSet

from api_routine.models import Routine
from api_routine.responses import RoutineResponseModelMixin
from api_routine.serializers import (RoutineUpdateSerializer, RoutineSerializer, RoutineDeleteSerializer,
                                     RoutineResultSerializer)


class RoutineListViewsets(ModelViewSet, RoutineResponseModelMixin):
    def get_queryset(self):
        query = Q(account_id=self.request.user.id)

        date = self.request.GET.get("date")
        if date:
            end_date = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)
            query.add(Q(created_at__gte=date, created_at__lt=end_date), Q.AND)
        return Routine.objects.filter(query)

    def get_serializer_class(self):
        if self.action == "list":
            return RoutineSerializer
        if self.action == "create":
            return RoutineUpdateSerializer

    def list(self, request, *args, **kwargs):
        self.response = super().list(request, *args, **kwargs)
        return self.get_response_model_for_list()

    def create(self, request, *args, **kwargs):
        self.response = super().create(request, *args, **kwargs)
        return self.get_response_model_for_create()


class RoutineSingleViewsets(ModelViewSet, RoutineResponseModelMixin):
    queryset = Routine.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RoutineSerializer
        if self.action == "partial_update":
            return RoutineUpdateSerializer

    def retrieve(self, request, *args, **kwargs):
        self.response = super().retrieve(request, *args, **kwargs)
        return self.get_response_model_for_retrieve()

    def partial_update(self, request, *args, **kwargs):
        self.response = super().partial_update(request, *args, **kwargs)
        return self.get_response_model_for_update()


class RoutineDeleteAPI(UpdateAPIView, RoutineResponseModelMixin):
    queryset = Routine.objects.all()
    serializer_class = RoutineDeleteSerializer

    def partial_update(self, request, *args, **kwargs):
        self.response = super().partial_update(request, *args, **kwargs)
        return self.get_response_model_for_delete()


class RoutineResultAPI(UpdateAPIView, RoutineResponseModelMixin):
    queryset = Routine.objects.all()
    serializer_class = RoutineResultSerializer

    def partial_update(self, request, *args, **kwargs):
        self.response = super().partial_update(request, *args, **kwargs)
        return self.get_response_model_for_result()
