from django.urls import path

from api_routine.views import RoutineDeleteAPI, RoutineResultAPI, RoutineListViewSet, RoutineSingleViewSet
from danbi_project.urls import list_method, detail_method

urlpatterns = [
    path("", RoutineListViewSet.as_view(list_method)),
    path("/<int:pk>", RoutineSingleViewSet.as_view(detail_method)),
    path("/<int:pk>/delete", RoutineDeleteAPI.as_view()),
    path("/<int:pk>/result", RoutineResultAPI.as_view())
]
