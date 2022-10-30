from datetime import timedelta, datetime

from django.db.models import Q
from rest_framework.generics import UpdateAPIView
from rest_framework.viewsets import ModelViewSet

from api_routine.models import Routine
from api_routine.responses import (RoutineDeleteResponseModel, RoutineUpdateResponseModel, RoutineRetrieveResponseModel,
                                   RoutineCreateResponseModel, RoutineResultResponseModel, RoutineListResponseModel)
from api_routine.serializers import (RoutineUpdateSerializer, RoutineSerializer, RoutineDeleteSerializer,
                                     RoutineResultSerializer, RoutineDetailSerializer)


class RoutineListViewSet(ModelViewSet):
    response_model = None

    def get_queryset(self):
        query = Q(account_id=self.request.user.id, is_deleted=False)

        date = self.request.GET.get("date")
        if date:
            end_date = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)
            query.add(Q(created_at__gte=date, created_at__lt=end_date), Q.AND)
        return Routine.objects.filter(query)

    def get_serializer_class(self):
        if self.action == "list":
            self.response_model = RoutineListResponseModel
            return RoutineSerializer
        if self.action == "create":
            self.response_model = RoutineCreateResponseModel
            return RoutineUpdateSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return self.response_model(response).get_response()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return self.response_model(response).get_response()


class RoutineSingleViewSet(ModelViewSet):
    queryset = Routine.objects.filter(is_deleted=False)
    response_model = None

    def get_serializer_class(self):
        if self.action == "retrieve":
            self.response_model = RoutineRetrieveResponseModel
            return RoutineDetailSerializer
        if self.action == "partial_update":
            self.response_model = RoutineUpdateResponseModel
            return RoutineUpdateSerializer

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return self.response_model(response).get_response()

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return self.response_model(response).get_response()


class RoutineDeleteAPI(UpdateAPIView):
    queryset = Routine.objects.filter(is_deleted=False)
    serializer_class = RoutineDeleteSerializer
    response_model = RoutineDeleteResponseModel

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return self.response_model(response).get_response()


class RoutineResultAPI(UpdateAPIView):
    queryset = Routine.objects.filter(is_deleted=False)
    serializer_class = RoutineResultSerializer
    response_model = RoutineResultResponseModel

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return self.response_model(response).get_response()
