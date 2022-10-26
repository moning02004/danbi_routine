from django.urls import path

from api_routine.views import RoutineListViewsets, RoutineSingleViewsets, RoutineDeleteAPI,RoutineResultAPI
from danbi_project.urls import list_method, detail_method

urlpatterns = [
    path("", RoutineListViewsets.as_view(list_method)),
    path("/<int:pk>", RoutineSingleViewsets.as_view(detail_method)),
    path("/<int:pk>/delete", RoutineDeleteAPI.as_view()),
    path("/<int:pk>/complete", RoutineResultAPI.as_view())
]
