from django.urls import path

from api_routine.views import RoutinesViewsets
from danbi_project.urls import list_method

urlpatterns = [
    path("", RoutinesViewsets.as_view(list_method))
]
