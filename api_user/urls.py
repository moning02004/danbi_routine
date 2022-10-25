from django.urls import path

from api_user.views import UsersViewsets
from danbi_project.urls import list_method

urlpatterns = [
    path("", UsersViewsets.as_view(list_method))
]