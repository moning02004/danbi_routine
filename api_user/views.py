from rest_framework.viewsets import ModelViewSet

from api_user.serializers import UserUpdateSerializer


class UsersViewsets(ModelViewSet):
    def get_serializer_class(self):
        if self.action == "create":
            return UserUpdateSerializer
