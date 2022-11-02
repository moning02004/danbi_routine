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
    def get_queryset(self):
        query = Q(account_id=self.request.user.id, is_deleted=False)

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

    def get_renderers(self):
        if self.action == "list":
            self.renderer_classes = [RoutineListResponseModel]
        if self.action == "create":
            self.renderer_classes = [RoutineCreateResponseModel]
        return super().get_renderers()


class RoutineSingleViewSet(ModelViewSet):
    queryset = Routine.objects.filter(is_deleted=False)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RoutineDetailSerializer
        if self.action == "partial_update":
            return RoutineUpdateSerializer

    def get_renderers(self):
        if self.action == "retrieve":
            self.renderer_classes = [RoutineRetrieveResponseModel]
        if self.action == "partial_update":
            self.renderer_classes = [RoutineUpdateResponseModel]
        return super().get_renderers()


class RoutineDeleteAPI(UpdateAPIView):
    queryset = Routine.objects.filter(is_deleted=False)
    serializer_class = RoutineDeleteSerializer
    renderer_classes = [RoutineDeleteResponseModel]


class RoutineResultAPI(UpdateAPIView):
    queryset = Routine.objects.filter(is_deleted=False)
    serializer_class = RoutineResultSerializer
    renderer_classes = [RoutineResultResponseModel]
